from marshmallow_dataclass import dataclass

@dataclass
class CVAModel:
  camera_id: str
  camera_source: str
  camera_fps: int