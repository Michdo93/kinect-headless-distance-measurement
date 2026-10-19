# Kinect Headless Distance Measurement

A lightweight, web-based utility designed for a **headless Raspberry Pi** connected to an **Xbox 360 Kinect (v1)**. This tool allows you to stream the live camera feed and click anywhere on the image via a web browser to instantly retrieve the exact pixel coordinates ($X, Y$) and the precise depth/distance in meters.

It serves as a practical helper tool for mapping and calibrating spatial zones for projects like the *Invisible Spatial Switch*.

---

## Features

* **Headless Operation:** Run it on a Raspberry Pi without an attached monitor, keyboard, or mouse.
* **Browser-Based Interface:** Access the live stream from any PC, tablet, or smartphone in the same local network.
* **Interactive Point-and-Click:** Click on any object (e.g., a wall, table, or hand) in the video stream to instantly read out its real-world distance.
* **Easy Configuration Helper:** Quickly find the exact coordinates and depth thresholds needed for spatial automation projects.

---

## Hardware & System Requirements

* **Hardware:** Raspberry Pi (3 or 4 recommended) + Xbox 360 Kinect v1 (with a dedicated power supply).
* **OS:** Raspberry Pi OS (or compatible Linux distribution).

---

## Installation

### 1. Install System Dependencies

Before installing the Python packages, ensure the `libfreenect` development libraries are installed on your system:

```bash
sudo apt-get update
sudo apt-get install libfreenect-dev -y
```

### 2. Install Python Packages

Install the required Python modules via `pip`:

```bash
pip install flask opencv-python freenect
```

---

## Usage

1. Save the measurement script on your Raspberry Pi as `distance_measurement.py`.
2. Run the script:
```bash
python3 distance_measurement.py
```

3. Open a web browser on any device connected to your local network and navigate to:
```text
http://<RASPBERRY_PI_IP>:5000
```


4. Click anywhere on the live video stream. The measured distance in meters will appear below the image, and the exact coordinates will be processed.

---

## How It Helps with Spatial Switch Projects

When setting up spatial interaction zones (such as virtual buttons or sliders in an *Invisible Spatial Switch*), guessing coordinates and depth boundaries (`z_min` / `z_max`) in a `config.json` can be tedious.

With this tool:

1. Place your hand or object at the target location.
2. Click on it in the web browser.
3. Use the reported depth value (e.g., convert meters to millimeters) and pixel positions to precisely define your zone ranges in your configuration file.

---

## ⚠️ Important Limitations of the Xbox 360 Kinect (v1)

While the Kinect v1 is powerful for indoor prototyping, it has clear physical limitations that you should keep in mind:

* **Operational Range:** The Kinect v1 is designed for a sweet spot between **0.8 meters and 4.0 meters**. Attempting to measure distances beyond 4 meters (such as a distant wall at 10 meters) will result in missing data, invalid depth values, or complete failure, as the infrared projector's signal fades out.
* **Resolution:** The depth stream operates at a resolution of `640x480` pixels. Very small or thin objects might span only a few pixels, reducing measurement precision.
* **Environmental & Material Constraints:**
* Direct sunlight or strong infrared interference can disrupt the sensor.
* Highly reflective, glossy, or completely transparent surfaces (like glass vases) can absorb or scatter the infrared light, causing "holes" (invalid 0-values) in the depth map.
