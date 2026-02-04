# 🔍 Vehicle Re-Identification (Re-ID) Module

The Re-ID module is responsible for **matching the same vehicle across time gaps and multiple cameras** using visual feature embeddings.

It enables long-term traffic intelligence beyond single-camera tracking.

---

## 🎯 Responsibilities

This module:
- Extracts visual feature embeddings from tracked vehicles
- Stores and queries embeddings using vector similarity
- Matches vehicles across time and camera boundaries
- Assigns a global or session-level identity

This module does **NOT**:
- Perform object detection
- Track objects frame-to-frame
- Detect traffic violations
- Make enforcement decisions

---

## 🧠 Re-ID Strategy

UrbanEye uses an **appearance-based re-identification approach**:

1. Crop vehicle images from tracked bounding boxes
2. Extract feature embeddings using a CNN
3. Store embeddings in a vector database
4. Perform similarity search for matching

---

## 📥 Input

```json
{
  "track_id": 42,
  "camera_id": "cam_01",
  "frame_id": 312,
  "vehicle_crop": "np.ndarray",
  "timestamp": "2026-02-03T10:15:04"
}
````

---

## 📤 Output

```json
{
  "global_vehicle_id": "veh_9af3c1",
  "track_id": 42,
  "similarity_score": 0.92,
  "matched": true
}
```

If no confident match is found, a new global ID is created.

---

## 🧠 Feature Embeddings

* Fixed-length dense vectors (e.g., 256 / 512 dims)
* L2-normalized
* Appearance-focused (shape, color, texture)

---

## 🗄️ Vector Store

* FAISS (CPU initially)
* Cosine or L2 similarity
* Metadata stored alongside vectors:

  * camera_id
  * timestamp
  * vehicle class

---

## 🔄 Processing Flow

1. Receive cropped vehicle image from tracking
2. Preprocess and normalize input
3. Extract feature embedding
4. Query vector database
5. Apply similarity threshold
6. Assign or create global identity

---

## ⚙️ Configuration

| Parameter              | Description                   |
| ---------------------- | ----------------------------- |
| `embedding_dim`        | Feature vector size           |
| `similarity_threshold` | Match acceptance threshold    |
| `max_history`          | Stored embeddings per vehicle |
| `camera_id`            | Source camera identifier      |

---

## 📌 Design Notes

* Stateless per inference
* State maintained in vector database
* IDs are **soft identities** (probabilistic)
* Optimized for precision over recall

---

## 🔐 Privacy Considerations

* No license plate OCR required
* No facial recognition
* Embeddings are non-reversible
* Cropped images not persisted by default

---

## 🔮 Future Extensions

* Multi-view embedding fusion
* Temporal consistency constraints
* Vehicle attribute classifiers
* Cross-city re-identification research

---

**Module Status:** Planned
**Owner:** Re-Identification Pipeline
