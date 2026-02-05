"""
UrbanEye Multi-Object Tracking Skeleton
---------------------------------------
Maintains persistent identities across frames.
"""

from typing import List, Dict
import numpy as np

class Track:
    """Internal track state."""
    def __init__(self, track_id, bbox, class_id, confidence):
        self.track_id = track_id
        self.bbox = bbox
        self.class_id = class_id
        self.confidence = confidence
        self.misses = 0
        self.age = 0

    def update(self, bbox, confidence):
        self.bbox = bbox
        self.confidence = confidence
        self.misses = 0
        self.age += 1

    def mark_missed(self):
        self.misses += 1
        self.age += 1

class Tracker:
    def __init__(self, max_age: int = 30, iou_threshold: float = 0.3):
        self.max_age = max_age
        self.iou_threshold = iou_threshold
        self.tracks: List[Track] = []
        self.next_track_id = 1
        self.frame_count = 0

    def update(self, detections: List[Dict]) -> List[Dict]:
        """
        Update tracker with current frame detections.

        Args:
            detections (List[Dict]): Output from detection module

        Returns:
            List[Dict]: Active tracks with IDs
        """
        self.frame_count += 1
        
        # 1. Match existing tracks to new detections using IOU
        matches, unmatched_tracks, unmatched_detections = self._match(detections)

        # 2. Update matched tracks
        for t_idx, d_idx in matches:
            self.tracks[t_idx].update(
                detections[d_idx]['bbox'],
                detections[d_idx]['confidence']
            )

        # 3. Create new tracks for unmatched detections
        for d_idx in unmatched_detections:
            det = detections[d_idx]
            new_track = Track(
                track_id=self.next_track_id,
                bbox=det['bbox'],
                class_id=det['class_id'],
                confidence=det['confidence']
            )
            self.tracks.append(new_track)
            self.next_track_id += 1

        # 4. Handle unmatched tracks (aging)
        for t_idx in unmatched_tracks:
            self.tracks[t_idx].mark_missed()

        # 5. Remove dead tracks
        self.tracks = [t for t in self.tracks if t.misses <= self.max_age]

        # 6. Format output
        output_tracks = []
        for t in self.tracks:
            output_tracks.append({
                "track_id": t.track_id,
                "class_id": t.class_id,
                "bbox": t.bbox,
                "confidence": t.confidence
            })

        return output_tracks

    def _match(self, detections):
        """Greedy IOU matching."""
        matches = []
        unmatched_tracks = list(range(len(self.tracks)))
        unmatched_detections = list(range(len(detections)))

        if len(self.tracks) == 0 or len(detections) == 0:
            return matches, unmatched_tracks, unmatched_detections

        # Calculate IOU matrix
        iou_matrix = np.zeros((len(self.tracks), len(detections)))
        for t, track in enumerate(self.tracks):
            for d, det in enumerate(detections):
                iou_matrix[t, d] = self._calculate_iou(track.bbox, det['bbox'])

        # Greedy assignment based on highest IOU
        if iou_matrix.size > 0:
            # Sort indices by IOU descending
            indices = np.dstack(np.unravel_index(np.argsort(iou_matrix.ravel())[::-1], iou_matrix.shape))[0]
            
            used_tracks = set()
            used_detections = set()

            for t_idx, d_idx in indices:
                if t_idx in used_tracks or d_idx in used_detections:
                    continue
                
                if iou_matrix[t_idx, d_idx] >= self.iou_threshold:
                    matches.append((t_idx, d_idx))
                    used_tracks.add(t_idx)
                    used_detections.add(d_idx)

            unmatched_tracks = [t for t in range(len(self.tracks)) if t not in used_tracks]
            unmatched_detections = [d for d in range(len(detections)) if d not in used_detections]

        return matches, unmatched_tracks, unmatched_detections

    def _calculate_iou(self, boxA, boxB):
        # box: [x1, y1, x2, y2]
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        
        return interArea / float(boxAArea + boxBArea - interArea + 1e-6)