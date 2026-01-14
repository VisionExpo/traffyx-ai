# UrbanEye: Intelligent Anomaly Detection 👁️🚦

![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange) ![Tech](https://img.shields.io/badge/Tech-YOLOv8%20%7C%20PyTorch-purple)

> **⚠️ Project Status:** This repository hosts the computer vision pipeline for detecting anomalies in industrial and urban environments. Currently migrating the core logic from the "Solar Panel Fault Detection" prototype to a generalized Video Analytics pipeline.

## 📋 Overview
UrbanEye uses deep learning to identify structural faults and traffic anomalies in real-time.

## 🧠 Core Features
* **Real-Time Detection:** Optimized inference pipeline (<150ms latency).
* **Multi-Class Classification:** Capable of distinguishing 6+ fault types.
* **Scalable API:** Asynchronous FastAPI backend.

## 🛠️ Tech Stack
* **Vision:** PyTorch, OpenCV, YOLOv8
* **Backend:** FastAPI
* **Deployment:** Docker
