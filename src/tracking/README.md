# 🧍 Multi-Object Tracking Module

The Tracking module is responsible for **maintaining persistent identities** for detected objects across consecutive video frames.

It converts frame-level detections into **temporally consistent tracks**, enabling motion analysis and higher-level reasoning.

---

## 🎯 Responsibilities

This module:
- Associates detections across frames
- Assigns stable `track_id`s to objects
- Maintains object trajectories over time
- Handles object entry, exit, and occlusion

This module does **NOT**:
- Perform object detection
- Classify violations
- Estimate speed or behavior
- Store long-term analytics

---

## 🧠 Tracking Algorithm

- **ByteTrack**
  - IoU-based matching
  - Confidence-aware association
  - Robust to missed detections

---

## 📥 Input

```json
{
  "frame_id": 120,
  "detections": [
    {
      "class": "car",
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.93
    }
  ]
}
````

---

## 📤 Output

```json
{
  "frame_id": 120,
  "tracks": [
    {
      "track_id": 42,
      "class": "car",
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.93
    }
  ]
}
```

Additionally, each track internally maintains:

```json
{
  "track_id": 42,
  "trajectory": [[x, y, t], ...],
  "age": 87,
  "last_seen": 0.03
}
```

---

## 🔄 Processing Flow

1. Receive detections for current frame
2. Predict existing track positions
3. Associate detections with tracks
4. Initialize new tracks if needed
5. Remove stale tracks
6. Emit updated track set

---

## ⚙️ Configuration

| Parameter       | Description                      |
| --------------- | -------------------------------- |
| `iou_threshold` | Minimum IoU for association      |
| `max_age`       | Frames before track removal      |
| `min_hits`      | Frames before track confirmation |
| `fps`           | Input video frame rate           |

---

## 📌 Design Notes

* Stateful across frames
* Deterministic given same input stream
* Optimized for real-time throughput
* Tracking IDs are **local to a camera**

---

## 🔮 Future Extensions

* Kalman filter tuning
* Appearance-based association
* Cross-camera ID stitching (via Re-ID)
* Occlusion reasoning

---

**Module Status:** Planned
**Owner:** Tracking Pipeline