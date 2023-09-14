import pandas as pd
import requests

from .model import DashboardResponse, GraphData, Datapoint, Unit

class DataRefresher:
    async def run(self):
        self.goals = pd.read_csv("data/goal_kwh.csv", index_col=0)
        self.monthly = pd.read_csv("data/monthly.csv", index_col=0)

        self.daily = pd.read_csv("data/sept_daily.csv", index_col=0)
        self.daily.index = pd.to_datetime(self.daily.index)

        self.hourly = pd.read_csv("data/lol.csv", index_col=0)
        self.hourly.index = pd.to_datetime(self.hourly.index)

    def get_daily_goal(self, column_name: str) -> float:
        current_month = pd.Timestamp.now().month
        goal = self.goals.loc[current_month, column_name]
        return round(goal * 1000, 2)
    
    def get_monthly_goal(self) -> float:
        current_month = pd.Timestamp.now().month
        goal = self.monthly.loc[current_month, "netto"]
        return round(goal, 2)
    
    def get_hourly_history(self, column_name: str) -> list[Datapoint]:
        now = pd.Timestamp.now()
        start = now.floor("D")
        end = now.floor("H") - pd.Timedelta(hours=1)

        data = self.hourly.loc[start:end, column_name]
        return [
            Datapoint(
                timestamp=ts.to_pydatetime(),
                value=round(val * 1000, 2)
            )
            for ts, val in data.items()
        ]
    
    def get_monthly_history(self) -> list[Datapoint]:
        now = pd.Timestamp.now()
        end = now.floor("D") - pd.Timedelta(days=1)

        data = self.daily.loc[:end, "netto"]
        return [
            Datapoint(
                timestamp=ts.to_pydatetime(),
                value=round(val, 2)
            )
            for ts, val in data.items()
        ]
    
    def get_power_reading(self) -> float:
        url = "http://10.1.0.41/api/remote/data/now"
        auth = {'Authorization': 'Bearer ba884eea-ceee-4921-baba-3ae63496d482'}
        reading = requests.get(url, headers=auth).json()
        return reading["active_power_w"] / 10
    
    def get_current_slope(self, is_levering: bool) -> float:
        value = self.get_power_reading()
        if is_levering:
            return max(0, value)
        else:
            return min(0, value)
    
    def get_monthly_slope(self) -> float:
        today = pd.Timestamp.now().floor("D")
        start = today - pd.Timedelta(days=7)
        end = today - pd.Timedelta(days=1)

        slope = self.daily.loc[start:end, "netto"].mean()
        return round(slope, 2)

    def get_daily_usage(self, is_levering: bool) -> GraphData:
        column_name = "levering" if is_levering else "teruglevering"

        return GraphData(
            goal=self.get_daily_goal(column_name=column_name),
            slope=self.get_current_slope(is_levering=is_levering),
            history=self.get_hourly_history(column_name=column_name),
            unit=Unit.Wh
        )
    
    def get_monthly_total(self):
        return GraphData(
            goal=self.get_monthly_goal(),
            slope=self.get_monthly_slope(),
            history=self.get_monthly_history(),
            unit=Unit.kWh
        )

    def get_data(self) -> DashboardResponse:
        return DashboardResponse(
            daily_usage=self.get_daily_usage(is_levering=True),
            daily_generation=self.get_daily_usage(is_levering=False),
            monthly_total=self.get_monthly_total()
        )

    async def stop(self):
        pass