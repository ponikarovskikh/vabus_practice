from dataclasses import dataclass, field
from typing import Union
import time

@dataclass
class Event:
    name: str
    value: Union[int, float]
    agg_func: str
    timestamp: float = field(default_factory=lambda: time.time())  # Unix timestamp в секундах

    def __post_init__(self):
        """
        проверка корректности.
        """
        self._validate_agg_func()

    def _validate_agg_func(self):
        """
        ППРОВЕРЯЕМ НА АГРЕГАЦИЮ.
        """
        valid_agg_funcs = ["sum", "avg", "min", "max"]
        if self.agg_func not in valid_agg_funcs:
            raise ValueError(f"Invalid aggregation function: {self.agg_func}. Must be one of {valid_agg_funcs}.")

    def to_dict(self) -> dict:
        """
        ИВЕНТ В СЛОВАРЬ
        """
        return {
            "name": self.name,
            "value": self.value,
            "agg_func": self.agg_func,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        """
        Создание ивЕНТА
        """
        return cls(
            name=data["name"],
            value=data["value"],
            agg_func=data["agg_func"],
            timestamp=data["timestamp"]
        )

