
from dataclasses import dataclass, field
from typing import Union
import time

@dataclass
class Metric:
    name: str
    value: Union[int, float]
    timestamp: float = field(default_factory=lambda: time.time())  # Unix timestamp в секундах

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Metric":
        return cls(
            name=data["name"],
            value=data["value"],
            timestamp=data["timestamp"]
        )