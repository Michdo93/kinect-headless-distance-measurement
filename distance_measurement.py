import cv2
import numpy as np
import freenect
from flask import Flask, render_template_string, Response, jsonify, request

app = Flask(__name__)

# Global variables for frames and the current depth map
current_depth_map = None

def get_video_frame():
    """Retrieves the RGB color image from the Kinect and converts it for the browser (JPEG)."""
    video, _ = freenect.sync_get_video()
    video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
    return video

def get_depth_frame():
    """Retrieves the depth map in millimeters from the Kinect."""
    depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
    return depth

# Simple HTML template with built-in JavaScript for mouse clicks
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Kinect Web Distance Measurement</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #222; color: #fff; margin-top: 20px; }
        #video-container { position: relative; display: inline-block; cursor: crosshair; }
        img { border: 3px solid #444; border-radius: 8px; max-width: 100%; }
        #result { margin-top: 15px; font-size: 20px; color: #00ffcc; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Kinect v1 - Real-Time Distance Measurement</h1>
    <p>Click on an object in the image (e.g., vase, table, wall) to measure the distance.</p>
    
    <div id="video-container">
        <!-- The Live Video Stream -->
        <img id="video-stream" src="{{ url_for('video_feed') }}" onclick="handleClick(event)">
    </div>

    <div id="result">Ready to measure...</div>

    <script>
        function handleClick(event) {
            const img = event.target;
            const rect = img.getBoundingClientRect();
            
            // Determine the click position relative to the image
            const clickX = event.clientX - rect.left;
            const clickY = event.clientY - rect.top;
            
            // The actual image size on the server (Kinect outputs 640x480)
            const scaleX = img.naturalWidth / img.clientWidth;
            const scaleY = img.naturalHeight / img.clientHeight;
            
            const realX = Math.round(clickX * scaleX);
            const realY = Math.round(clickY * scaleY);

            // Send to the Flask server
            fetch(`/measure?x=${realX}&y=${realY}`)
                .then(response => response.json())
                .then(data => {
                    const resDiv = document.getElementById("result");
                    if (data.success) {
                        resDiv.innerHTML = `📍 Distance at X=${realX}, Y=${realY}: <span style="color: #ff9900;">${data.distance_m} meters</span>`;
                    } else {
                        resDiv.innerHTML = `⚠️ No valid measurement value at this location.`;
                    }
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

def generate_frames():
    """Generator for the MJPEG video stream to the browser."""
    global current_depth_map
    while True:
        frame = get_video_frame()
        current_depth_map = get_depth_frame()
        
        # Compress an image to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Send a stream chunk to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/measure')
def measure():
    """Called when the user clicks in the browser."""
    global current_depth_map
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        
        if current_depth_map is not None:
            # Read the depth value at the clicked coordinate
            depth_value = current_depth_map[y, x]
            
            if depth_value > 0:
                distance_meters = round(depth_value / 1000.0, 2)
                return jsonify({"success": True, "distance_m": distance_meters})
        
        return jsonify({"success": False})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Host '0.0.0.0' makes the server accessible throughout the local network
    app.run(host='0.0.0.0', port=5000, debug=False)
