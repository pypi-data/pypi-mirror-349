from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class CatOptions:
    format: Optional[Literal["jpeg", "png", "webp", "gif"]] = None
    blur: Optional[float] = None  # 0–10
    saturation: Optional[int] = None  # 0–100
    brightness: Optional[float] = None  # 0–10
    text: Optional[str] = None
    text_color: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    greyscale: Optional[bool] = None
    tint: Optional[str] = None
    id: Optional[str] = None
    json: Optional[bool] = None
    base64: Optional[bool] = None
    html: Optional[bool] = None

    def to_params(self) -> dict:
        return {
            k: str(v).lower() if isinstance(v, bool) else v
            for k, v in self.__dict__.items() if v is not None
        }
