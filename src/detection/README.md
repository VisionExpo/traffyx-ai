# 🚗 Detection Module

The Detection module is responsible for **frame-level object detection** in Traffyx-AI.

It converts raw video frames into structured object detections that can be consumed by downstream modules such as tracking and intelligence.

---

## 🎯 Responsibilities

This module:
- Performs object detection on individual frames
- Identifies vehicles, pedestrians, riders, and helmets
- Outputs bounding boxes with class labels and confidence scores

This module does **NOT**:
- Track objects across frames
- Assign persistent IDs
- Perform speed estimation or violation logic
- Store events or analytics

---

## 🧠 Model

- YOLOv8 (Ultralytics)
- PyTorch-based inference
- GPU-accelerated (CPU fallback optional)

---

## 📥 Input

```python
frame: np.ndarray  # Single video frame (H x W x C)
````

Optional metadata:

```python
{
  "frame_id": int,
  "timestamp": float
}
```

---

## 📤 Output

```json
{
  "frame_id": 120,
  "detections": [
    {
      "class": "motorcycle",
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.91
    },
    {
      "class": "person",
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.88
    }
  ]
}
```

---

## 🔄 Processing Flow

1. Receive frame from video ingestion layer
2. Preprocess frame (resize, normalize)
3. Run YOLOv8 inference
4. Post-process detections
5. Emit structured detection output

---

## ⚙️ Configuration

| Parameter        | Description                    |
| ---------------- | ------------------------------ |
| `model_path`     | YOLOv8 weights file            |
| `conf_threshold` | Detection confidence threshold |
| `img_size`       | Inference resolution           |
| `device`         | CPU / CUDA                     |

---

## 📌 Design Notes

* Stateless by design
* Deterministic per-frame behavior
* Optimized for real-time inference
* Output format is **contractually stable**

---

## 🔮 Future Extensions

* Class-specific confidence thresholds
* Quantized / TensorRT models
* Region-of-interest filtering
* Model hot-swapping

---

**Module Status:** Planned
**Owner:** Detection Pipeline