import os
from typing import List
from event import Event
import asyncio
import json

class Storage:
    def __init__(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "kafka")
        self.postgres_dsn = os.getenv("POSTGRES_DSN", "")
        self.kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
        self.kafka_topic = os.getenv("KAFKA_TOPIC", "aggregated_events")

    async def send_to_storage(self, events: List[Event]):
        """
        Асинхронно отправить агрегированные события в указанное хранилище (Kafka или Postgres).
        """
        if self.storage_type == "kafka":
            await self._send_to_kafka(events)
        elif self.storage_type == "postgres":
            await self._send_to_postgres(events)

    async def _send_to_kafka(self, events: List[Event]):

        from aiokafka import AIOKafkaProducer

        producer = AIOKafkaProducer(bootstrap_servers=self.kafka_bootstrap_servers)
        await producer.start()
        try:
            for event in events:
                # Преобразование события в формат JSON
                value = json.dumps(event.__dict__).encode('utf-8')
                await producer.send_and_wait(self.kafka_topic, value=value)
        finally:
            await producer.stop()
        pass

    async def _send_to_postgres(self, events: List[Event]):



        import asyncpg

        conn = await asyncpg.connect(self.postgres_dsn)
        try:
            for event in events:
                await conn.execute(
                    "INSERT INTO events (name, value, agg_func, timestamp) VALUES($1, $2, $3, $4)",
                    event.name, event.value, event.agg_func, event.timestamp
                )
        finally:
            await conn.close()
        pass