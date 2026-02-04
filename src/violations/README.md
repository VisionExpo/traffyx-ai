# 🚨 Violations & Reasoning Module

The Violations module is responsible for **interpreting tracked object behavior over time** and converting it into **meaningful traffic violations**.

This module performs **spatio-temporal reasoning** using object trajectories, timestamps, and contextual rules.

---

## 🎯 Responsibilities

This module:
- Consumes tracked objects with persistent IDs
- Analyzes motion and behavior across time
- Detects traffic violations
- Emits structured violation events

This module does **NOT**:
- Perform object detection
- Perform object tracking
- Render dashboards
- Store raw video data

---

## 🧠 Core Principle

> Violations are detected from **patterns over time**, not single frames.

---

## 📥 Input

```json
{
  "frame_id": 245,
  "tracks": [
    {
      "track_id": 42,
      "class": "motorcycle",
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.91,
      "trajectory": [[x, y, t], ...]
    }
  ]
}
````

---

## 📤 Output (Violation Events)

```json
{
  "event_type": "overspeeding",
  "track_id": 42,
  "value": 68,
  "unit": "kmph",
  "timestamp": "2026-02-03T10:14:22",
  "confidence": 0.87
}
```

Events are **append-only** and stateless once emitted.

---

## 🚓 Supported Violations (Phase-wise)

### 🚗 Speeding

* Estimated using object trajectory
* Requires camera calibration
* Per-lane speed limits supported

### 🪖 Helmet Non-Compliance

* Rider + pillion detection
* Helmet presence classification
* Temporal smoothing to reduce false positives

### 🔜 Planned

* Lane violation
* Signal jumping
* Wrong-way driving

---

## 🔄 Processing Flow

1. Receive updated tracks
2. Maintain rolling history per `track_id`
3. Apply rule-based / learned logic
4. Generate violation events
5. Emit structured output to event store

---

## ⚙️ Configuration

| Parameter              | Description                          |
| ---------------------- | ------------------------------------ |
| `speed_limit_kmph`     | Maximum allowed speed                |
| `pixel_to_meter_ratio` | Camera calibration value             |
| `min_frames`           | Frames required to confirm violation |
| `cooldown_frames`      | Prevent duplicate events             |

---

## 📌 Design Notes

* Stateful per track
* Deterministic rule execution
* Explainable violation logic
* Independent of UI and storage layers

---

## 🔐 Privacy Considerations

* No face recognition
* No license plate identification
* Only metadata is persisted
* Raw frames discarded after processing

---

## 🔮 Future Extensions

* ML-based behavior classification
* Near-miss detection
* Risk scoring
* Accident prediction models

---

**Module Status:** Planned
**Owner:** Intelligence Pipeline