# 🌾 ZINO AgroVision Engine

![C++](https://img.shields.io/badge/Language-C%2B%2B17-blue.svg)
![OpenCV](https://img.shields.io/badge/Library-OpenCV%204.x-green.svg)
![Computer Vision](https://img.shields.io/badge/Domain-Computer%20Vision-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

> An embedded computer vision processing engine built with C++ and OpenCV, optimized for real-time visual analysis and feature extraction on resource-constrained edge devices.

---

## 📸 Quick Visual Demo

![AgroVision Demo Preview](./assets/demo_preview.gif)

🎬 **[Watch High-Resolution Demo Video](https://github.com/IsmailHasasna)** | 📄 **[Read Technical Overview](./docs/TECHNICAL_REPORT.pdf)**

---

## 🔑 Core Features & Engineering Highlights

- **Embedded Image Processing:** High-performance spatial filtering and frame processing using pure C++ and OpenCV for ultra-low latency.
- **Resource-Constrained Efficiency:** Optimized memory allocation and frame pipelines built to execute smoothly on edge compute units.
- **Contour Analysis & Segmentation:** Automated thresholding and feature extraction algorithms tailored for visual diagnostics.
- **Real-Time Data Pipeline:** Multi-threaded frame capture and ingestion architecture for continuous camera feed processing.

---

## 🛠️ Tech Stack & Requirements

- **Languages:** C++17 / C++20
- **Libraries:** OpenCV 4.x
- **Build System:** CMake
- **Target Hardware:** Embedded Linux / ARM SBCs

---

## 🚀 Quick Execution Guide

```bash
# Clone repository
git clone https://github.com/IsmailHasasna/ZINO-AgroVision-Engine.git
cd ZINO-AgroVision-Engine

# Build and run project
mkdir build && cd build
cmake ..
make
./ZinoAgroVision --input ../samples/test_image.jpg
