import asyncio
import os
import time
from vabus import VaBus
from aggregator import Aggregator
from storage import Storage
from metric import Metric
from event import Event


async def main():
    url = os.getenv("VABUS_URL", "http://localhost:8000")
    aggregation_interval = int(os.getenv("AGGREGATION_INTERVAL", 60))
    storage_type = os.getenv("STORAGE_TYPE", "kafka")

    async with VaBus(url) as bus:
        aggregator = Aggregator(aggregation_interval)
        storage = Storage(storage_type)

        while True:
            try:
                event_dict = await bus.get_event()

                # преобразовать надо Event из словаря
                event = Event.from_dict(event_dict)

                print(f"Received event: {event}")

                aggregator.aggregate(event)

                current_time = time.time()
                if current_time % aggregation_interval < 1:
                    aggregated_events = aggregator.get_aggregated_events()

                    await storage.send_to_storage(aggregated_events)
                    print("Aggregated events sent to storage")

                    metric = Metric(name="aggregated_events_count", value=len(aggregated_events))
                    await bus.send_metric(metric)
                    print("МЕТРИКИ ОТПРАВЛЕНЫ ")

            except Exception as e:
                print(f"ошибка следующая: {e}")

            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
