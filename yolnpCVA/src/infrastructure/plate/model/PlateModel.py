from marshmallow_dataclass import dataclass

@dataclass
class Plate:
    tracking_id: int
    camera_id: str
    image_id: str
    content: str or None
    in_frames: float or None
    duration: float or None
    datetime: str