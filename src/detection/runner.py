import cv2
import os
import time
import datetime
from typing import Dict

from detection.engine import DetectionEngine
from tracking.tracker import Tracker
from utils.timer import timed
from utils.memory import get_memory_mb
from metrics.logger import MetricsLogger

class PipelineRunner:
    def __init__(self, video_path: str, config: Dict):
        self.video_path = video_path
        self.config = config
        self.frame_index = 0
        self.fps_window = []
        self.window_size = config.get("performance", {}).get("fps_window", 30)
        
        # Initialize components
        print("Initializing Pipeline...")
        self.detector = DetectionEngine(
            model_path=config.get("model_path", "models/yolov8n.pt"),
            conf_threshold=config.get("conf_threshold", 0.5),
            device=config.get("device", "auto")
        )
        print(f"Running on device: {self.detector.device}")
        self.tracker = Tracker(
            max_age=config.get("max_age", 30),
            iou_threshold=config.get("iou_threshold", 0.3)
        )
        
        # Initialize Logger
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"logs/run_{timestamp}.jsonl"
        self.logger = MetricsLogger(log_path=log_path)

    def run(self):
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {self.video_path}")

        print(f"Starting processing: {self.video_path}")

        try:
            while True:
                timings = {}
                
                # 1. Decode
                with timed("decode", timings):
                    ret, frame = cap.read()
                
                # Handle end of video or read failure
                if not ret:
                    print("End of video stream or read error.")
                    break
                
                # Handle corrupt/empty frames
                if frame is None or frame.size == 0:
                    print(f"Warning: Empty frame at index {self.frame_index}")
                    self.logger.log_dropped()
                    self.frame_index += 1
                    continue

                # 2. Detection
                with timed("inference", timings):
                    detections = self.detector.detect(frame)
                
                # 3. Tracking
                with timed("tracking", timings):
                    tracks = self.tracker.update(detections)
                
                # 4. Post-process / Validation
                with timed("postprocess", timings):
                    self._validate_outputs(detections, tracks)

                # Calculate E2E latency
                timings["e2e"] = (
                    timings["decode"]
                    + timings["inference"]
                    + timings["tracking"]
                    + timings["postprocess"]
                )
                
                # Calculate Rolling FPS
                self.fps_window.append(timings["e2e"])
                if len(self.fps_window) > self.window_size:
                    self.fps_window.pop(0)
                
                avg_latency = sum(self.fps_window) / len(self.fps_window)
                current_fps = 1000.0 / (avg_latency + 1e-6) if self.fps_window else 0.0

                # 5. Logging
                memory_mb = (
                    round(get_memory_mb(), 2)
                    if self.config.get("performance", {}).get("measure_memory", True)
                    else None
                )

                log_data = {
                    "frame": self.frame_index,
                    "fps": round(current_fps, 2),
                    "latency_ms": {k: round(v, 2) for k, v in timings.items()},
                    "memory_mb": memory_mb,
                    "detections": len(detections),
                    "tracks": len(tracks)
                }
                self.logger.log(log_data)

                if self.frame_index % self.config.get("performance", {}).get("log_every_n_frames", 10) == 0:
                    print(f"[Frame {self.frame_index}] FPS: {current_fps:.1f} | E2E: {timings['e2e']:.1f}ms | Tracks: {len(tracks)}")

                self.frame_index += 1

        except KeyboardInterrupt:
            print("\nPipeline stopped by user.")
        except Exception as e:
            print(f"\nCRITICAL ERROR: Pipeline crashed at frame {self.frame_index}")
            print(f"Error: {e}")
            raise e
        finally:
            cap.release()
            self.logger.close()
            print("Pipeline finished.")

    def _validate_outputs(self, detections, tracks):
        """Ensure data contracts are met."""
        for d in detections:
            assert len(d['bbox']) == 4, "Detection bbox malformed"
            assert 0.0 <= d['confidence'] <= 1.0, "Confidence out of range"
        
        for t in tracks:
            assert 'track_id' in t, "Track missing ID"
            assert isinstance(t['track_id'], int), "Track ID must be integer"
