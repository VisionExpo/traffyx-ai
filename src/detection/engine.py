import numpy as np
from typing import List, Dict
from ultralytics import YOLO

class DetectionEngine:
    """
    Frame-level object detection engine using YOLOv8.
    Stateless by design.
    """
    def __init__(self, model_path: str, conf_threshold: float = 0.5, device: str = "cpu"):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.device = device
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load model and perform warm-up inference."""
        try:
            print(f"Loading YOLOv8 model from {self.model_path} to {self.device}...")
            self.model = YOLO(self.model_path)
            
            # Warm-up run (1 dummy frame)
            print("Running warm-up inference...")
            dummy_frame = np.zeros((640, 640, 3), dtype=np.uint8)
            self.model(dummy_frame, device=self.device, verbose=False)
            print("Model loaded and warmed up.")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def detect(self, frame: np.ndarray) -> List[Dict]:
        """
        Run inference on a single frame.
        
        Returns:
            List[Dict]: [
              {
                "bbox": [x1, y1, x2, y2],
                "confidence": float,
                "class_id": int,
                "class_name": str
              }
            ]
        """
        if frame is None:
            return []

        # Run inference
        results = self.model(frame, conf=self.conf_threshold, device=self.device, verbose=False)
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Extract data (ensure CPU and float types)
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                cls_name = self.model.names[cls_id]

                detections.append({
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "confidence": conf,
                    "class_id": cls_id,
                    "class_name": cls_name
                })

        return detections
