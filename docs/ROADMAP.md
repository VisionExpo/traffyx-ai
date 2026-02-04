# 🗺️ UrbanEye — Project Roadmap

This roadmap outlines the phased development of **UrbanEye**, from a core computer vision pipeline to a full-fledged, edge-deployable traffic intelligence system.

The roadmap is designed to:
- Enable incremental, testable progress
- Maintain architectural clarity
- Balance research depth with real-world deployment needs

---

## 🚀 Phase 0 — Foundation (Current)

**Status:** ✅ In Progress

### Objectives
- Establish clear product vision and scope
- Define system architecture and modular boundaries
- Prepare the repository for scalable development

### Deliverables
- Project README with problem framing
- High-level system architecture
- Modular folder structure
- Documentation-first workflow

### Outcome
A solid foundation that allows the system to scale without major refactors.

---

## 🧠 Phase 1 — Core Vision Pipeline

**Status:** 🔄 Planned

### Objectives
- Build a reliable real-time detection and tracking pipeline
- Ensure stable object identities across frames
- Validate performance on real traffic footage

### Key Features
- YOLOv8-based vehicle and pedestrian detection
- Multi-object tracking using ByteTrack
- Support for video files and RTSP streams
- Basic visualization of detections and tracks

### Milestones
- [ ] Implement detection inference module
- [ ] Integrate tracking with persistent IDs
- [ ] Optimize inference for edge GPUs
- [ ] Validate FPS and latency targets

### Success Criteria
- Stable tracking IDs across frames
- Real-time performance (>25 FPS on edge GPU)
- Robust detection in dense, mixed traffic

---

## 🚓 Phase 2 — Violation Detection & Reasoning

**Status:** ⏳ Planned

### Objectives
- Convert tracked motion into meaningful traffic violations
- Move from frame-level detection to temporal reasoning

### Key Features
- Vehicle speed estimation using trajectory analysis
- Helmet non-compliance detection (rider + pillion)
- Rule-based violation classification
- Structured violation event generation

### Milestones
- [ ] Camera calibration and distance mapping
- [ ] Speed estimation logic
- [ ] Helmet detection module
- [ ] Violation event schema

### Success Criteria
- Speed estimation error within acceptable range
- Reliable helmet detection in varied lighting
- Clean, queryable violation logs

---

## 🔍 Phase 3 — Vehicle Re-Identification (Re-ID)

**Status:** ⏳ Planned

### Objectives
- Enable cross-frame and cross-camera vehicle matching
- Support long-term traffic behavior analysis

### Key Features
- Feature embedding extraction for vehicles
- Vector similarity search using FAISS
- Cross-camera vehicle matching
- Repeat offender identification

### Milestones
- [ ] Re-ID model integration
- [ ] Vector database setup
- [ ] Similarity threshold calibration
- [ ] Re-ID evaluation metrics

### Success Criteria
- High precision vehicle matching
- Low false-positive rate
- Efficient embedding search at scale

---

## 📊 Phase 4 — Analytics & Visualization

**Status:** ⏳ Planned

### Objectives
- Provide actionable insights to traffic authorities
- Move from raw events to decision-support tools

### Key Features
- Real-time violation dashboards
- Traffic flow and density analytics
- Time-based and location-based reports
- Exportable reports

### Milestones
- [ ] FastAPI backend for event APIs
- [ ] Dash / Plotly dashboard (Phase 1)
- [ ] React-based UI (Phase 2)
- [ ] Role-based access (planned)

### Success Criteria
- Intuitive dashboards
- Near real-time data refresh
- Clear visualization of trends and hotspots

---

## 🔐 Phase 5 — Privacy, Optimization & Deployment

**Status:** 🔮 Planned

### Objectives
- Prepare UrbanEye for real-world deployment
- Ensure ethical, privacy-aware usage

### Key Features
- Face and license plate masking
- Edge deployment optimization (TensorRT)
- Dockerized deployments
- Multi-camera scalability

### Milestones
- [ ] Privacy filtering pipeline
- [ ] TensorRT optimization
- [ ] Docker-based deployment
- [ ] Multi-camera orchestration

### Success Criteria
- Sub-100 ms latency
- Minimal resource footprint
- Privacy-compliant operation

---

## 🔮 Phase 6 — Predictive Intelligence (Long-Term)

**Status:** 🧪 Research

### Objectives
- Move from reactive enforcement to proactive safety
- Predict accidents before they occur

### Research Directions
- Near-miss detection
- Trajectory conflict analysis
- Risk scoring for intersections
- Traffic signal optimization (future)

### Success Criteria
- Early warning signals for risky behavior
- Actionable insights for urban planners
- Measurable reduction in accident-prone zones

---

## 📌 Roadmap Philosophy

UrbanEye follows a **research-driven, production-aware** roadmap:
- Build simple → validate → scale
- Favor explainable logic over black-box predictions
- Prioritize real-world constraints over benchmarks

> The goal is not just to detect traffic —  
> but to **understand and improve it**.

---

**Roadmap Version:** v0.1.0  
**Last Updated:** Feb 2026
