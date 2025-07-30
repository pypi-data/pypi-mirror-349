from .constant import Constant
from .response import Response


import json
import os


class DellCalendar(Constant):
    def get(self, conditions={}):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(script_dir, "year_quar_week.json"), "r", encoding="utf-8") as f:
            data = json.load(f)

        # conditions={"week_new": "WK09","updatetime": "2024-01-02"}

        def filter_data(data, conditions):
            return [item for item in data if all(item.get(k) == v for k, v in conditions.items())]

        filtered = filter_data(data, conditions)

        return Response(data=filtered)
