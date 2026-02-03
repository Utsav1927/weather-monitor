"""
Advanced Weather Simulation System
----------------------------------
MAJOR REFACTOR VERSION (PR TEST)

Changes introduced:
- Object-oriented design
- Data validation layer
- Weather history tracking
- Severity scoring
- Alert priority system
- Structured reporting

No external APIs used.
"""

from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict
import random
import json
import statistics


# =========================
# DATA MODELS
# =========================
@dataclass
class WeatherData:
    temperature: int
    humidity: int
    wind_speed: int
    condition: str
    timestamp: str


@dataclass
class Alert:
    message: str
    severity: int   # 1 = low, 5 = critical


# =========================
# WEATHER ENGINE
# =========================
class WeatherEngine:
    CONDITIONS = ["Clear", "Cloudy", "Rain", "Storm", "Heatwave", "Cold Wave"]

    def generate(self) -> WeatherData:
        return WeatherData(
            temperature=random.randint(-10, 50),
            humidity=random.randint(10, 95),
            wind_speed=random.randint(0, 30),
            condition=random.choice(self.CONDITIONS),
            timestamp=datetime.utcnow().isoformat()
        )


# =========================
# ALERT ENGINE
# =========================
class AlertEngine:

    def evaluate(self, weather: WeatherData) -> List[Alert]:
        alerts = []

        if weather.temperature >= 40:
            alerts.append(Alert("Extreme heat alert", 5))

        if weather.temperature <= -2:
            alerts.append(Alert("Severe cold alert", 4))

        if weather.wind_speed >= 20:
            alerts.append(Alert("High wind alert", 3))

        if weather.condition in ["Storm", "Heatwave", "Cold Wave"]:
            alerts.append(Alert(f"{weather.condition} warning", 4))

        return alerts


# =========================
# ANALYTICS
# =========================
class WeatherAnalytics:
    def calculate_severity_score(self, alerts: List[Alert]) -> int:
        if not alerts:
            return 0
        return max(alert.severity for alert in alerts)

    def calculate_temperature_trend(self, history: List[WeatherData]) -> float:
        if len(history) < 2:
            return 0.0
        temps = [w.temperature for w in history]
        return statistics.mean(temps)


# =========================
# STORAGE
# =========================
class WeatherStorage:
    FILE = "weather_history.json"

    def save(self, weather: WeatherData, alerts: List[Alert]) -> None:
        record = {
            "weather": asdict(weather),
            "alerts": [asdict(a) for a in alerts]
        }

        with open(self.FILE, "a") as f:
            f.write(json.dumps(record) + "\n")


# =========================
# REPORTING
# =========================
class WeatherReporter:

    def print_report(
        self,
        city: str,
        weather: WeatherData,
        alerts: List[Alert],
        severity_score: int,
        avg_temp: float
    ) -> None:

        print("\n🌦 WEATHER REPORT")
        print("================")
        print(f"City: {city}")
        print(f"Time: {weather.timestamp}")

        print("\nCurrent Conditions")
        print("------------------")
        print(f"Temperature : {weather.temperature} °C")
        print(f"Humidity    : {weather.humidity} %")
        print(f"Wind Speed  : {weather.wind_speed} km/h")
        print(f"Condition   : {weather.condition}")

        print("\nAnalytics")
        print("---------")
        print(f"Severity Score     : {severity_score}")
        print(f"Average Temp Trend : {round(avg_temp, 2)} °C")

        print("\nAlerts")
        print("------")
        if alerts:
            for alert in alerts:
                print(f"[Severity {alert.severity}] {alert.message}")
        else:
            print("No alerts detected.")


# =========================
# APPLICATION
# =========================
class WeatherApplication:

    def __init__(self):
        self.engine = WeatherEngine()
        self.alert_engine = AlertEngine()
        self.analytics = WeatherAnalytics()
        self.storage = WeatherStorage()
        self.reporter = WeatherReporter()
        self.history: List[WeatherData] = []

    def run(self):
        city = input("Enter city name: ").strip()

        if not city:
            print("City name is required")
            return

        weather = self.engine.generate()
        self.history.append(weather)

        alerts = self.alert_engine.evaluate(weather)
        severity = self.analytics.calculate_severity_score(alerts)
        avg_temp = self.analytics.calculate_temperature_trend(self.history)

        self.storage.save(weather, alerts)

        self.reporter.print_report(
            city=city,
            weather=weather,
            alerts=alerts,
            severity_score=severity,
            avg_temp=avg_temp
        )


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    app = WeatherApplication()
    app.run()
