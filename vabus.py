from aiohttp import ClientSession
from event import Event
from metric import Metric
import json

class VaBus:
    # подключаемся
    def __init__(self, url: str):
        self.url = url
        self._session = ClientSession(base_url=url)

    # вход
    async def __aenter__(self) -> "VaBus":
        await self._session.__aenter__()
        return self
    # выход
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
    # получение ивента
    async def get_event(self) -> Event:
        async with self._session.get(f"{self.url}/events") as response:
            if response.status == 200:
                data = await response.json()
                return Event.from_dict(data)
            else:
                response.raise_for_status()
    # ОТПРАВКА МЕТРИК
    async def send_metric(self, metric: Metric):
        async with self._session.post(f"{self.url}/metrics", json=metric.to_dict()) as response:
            if response.status != 200:
                response.raise_for_status()