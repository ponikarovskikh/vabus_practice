from collections import defaultdict
from typing import List, Dict
from event import Event

from collections import defaultdict
from typing import List, Dict, Callable, Union, Tuple
from event import Event

class Aggregator:
    # на основе параметров введем интервал
    def __init__(self, aggregation_interval: int):
        self.aggregation_interval = aggregation_interval
        self.events: Dict[str, List[Event]] = defaultdict(list)

    def aggregate(self, event: Event):
        """
        здесь по названию проведим агрегацию
        """
        self.events[event.name].append(event)

    def get_aggregated_events(self) -> List[Event]:
        """
       здесь  Возвращаем  агрегированные события.
        """
        aggregated_events = []
        for name, events in self.events.items():
            if events:
                func = self._get_aggregation_function(events[0].agg_func)
                aggregated_value = func([event.value for event in events])
                aggregated_event = Event(name=name, value=aggregated_value, agg_func=events[0].agg_func, timestamp=events[-1].timestamp)
                aggregated_events.append(aggregated_event)
        return aggregated_events

    def _get_aggregation_function(self, agg_func: str) -> Callable[[List[Union[int, float]]], Union[int, float]]:
        """
         основе строки agg_func получим то на основе чего агрегируем
        """
        if agg_func == "sum":
            return sum
        elif agg_func == "avg":
            return self._average
        elif agg_func == "min":
            return min
        elif agg_func == "max":
            return max
        else:
            raise ValueError(f"Неизвестная функция агрегации: {agg_func}")

    def _average(self, values: List[Union [int, float]]) -> float:
        """
         среднее значение
        """
        return sum(values) / len(values) if values else 0
