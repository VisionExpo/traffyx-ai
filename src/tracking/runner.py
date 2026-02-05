import cv2
import os
import time
from typing import Dict

from detection.engine import DetectionEngine
from tracking.tracker import Tracker

class PipelineRunner:
    def __init__(self, video_path: str, config: Dict):
        self.video_path = video_path
        self.config = config
        self.frame_index = 0
        
        # Initialize components
        print("Initializing Pipeline...")
        self.detector = DetectionEngine(
            model_path=config.get("model_path", "models/yolov8n.pt"),
            conf_threshold=config.get("conf_threshold", 0.5),
            device=config.get("device", "cpu")
        )
        self.tracker = Tracker(
            max_age=config.get("max_age", 30),
            iou_threshold=config.get("iou_threshold", 0.3)
        )

    def run(self):
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {self.video_path}")

        print(f"Starting processing: {self.video_path}")

        try:
            while True:
                ret, frame = cap.read()
                
                # Handle end of video or read failure
                if not ret:
                    print("End of video stream or read error.")
                    break
                
                # Handle corrupt/empty frames
                if frame is None or frame.size == 0:
                    print(f"Warning: Empty frame at index {self.frame_index}")
                    self.frame_index += 1
                    continue

                # 1. Detection
                detections = self.detector.detect(frame)
                
                # 2. Tracking
                tracks = self.tracker.update(detections)
                
                # 3. Validation
                self._validate_outputs(detections, tracks)

                # 4. Logging
                if self.frame_index % 10 == 0:
                    print(f"[Frame {self.frame_index}] Detections: {len(detections)} | Tracks: {len(tracks)}")

                self.frame_index += 1

        except KeyboardInterrupt:
            print("\nPipeline stopped by user.")
        except Exception as e:
            print(f"\nCRITICAL ERROR: Pipeline crashed at frame {self.frame_index}")
            print(f"Error: {e}")
            raise e
        finally:
            cap.release()
            print("Pipeline finished.")

    def _validate_outputs(self, detections, tracks):
        """Ensure data contracts are met."""
        for d in detections:
            assert len(d['bbox']) == 4, "Detection bbox malformed"
            assert 0.0 <= d['confidence'] <= 1.0, "Confidence out of range"
        
        for t in tracks:
            assert 'track_id' in t, "Track missing ID"
            assert isinstance(t['track_id'], int), "Track ID must be integer"
