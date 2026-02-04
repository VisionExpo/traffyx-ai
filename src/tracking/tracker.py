"""
UrbanEye Multi-Object Tracking Skeleton
---------------------------------------
Maintains persistent identities across frames.
"""

from typing import List, Dict


class Tracker:
    def __init__(self):
        self.tracks = []

    def update(self, detections: List[Dict]) -> List[Dict]:
        """
        Update tracker with current frame detections.

        Args:
            detections (List[Dict]): Output from detection module

        Returns:
            List[Dict]: Active tracks with IDs
        """
        # TODO: Integrate ByteTrack here
        tracks = []

        for idx, det in enumerate(detections):
            tracks.append({
                "track_id": idx,
                "class": det.get("class"),
                "bbox": det.get("bbox"),
                "confidence": det.get("confidence")
            })

        return tracks