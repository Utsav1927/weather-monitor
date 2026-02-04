"""
Weather Simulator (Refactored)
------------------------------
- Modular & testable design
- Configuration-driven alert rules
- Deterministic mode for CI/testing
- Clean separation of concerns
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import random


# =========================
# Configuration
# =========================

ALERT_RULES = {
    "EXTREME_HEAT": {
        "temp_min": 38,
        "message": "Extreme heat alert"
    },
    "FREEZING": {
        "temp_max": 0,
        "message": "Freezing temperature alert"
    },
    "HIGH_WIND": {
        "wind_min": 15,
        "message": "High wind alert"
    },
    "RAIN_STORM": {
        "conditions": ["Rain", "Storm"],
        "message": "Rain/Storm alert"
    },
}

WEATHER_CONDITIONS = ["Clear", "Cloudy", "Rain", "Storm"]


# =========================
# Data Model
# =========================

@dataclass
class WeatherData:
    temperature: int
    humidity: int
    wind_speed: int
    condition: str


# =========================
# Validation
# =========================

def validate_city(city: str) -> str:
    city = city.strip()
    if not city:
        raise ValueError("City name cannot be empty")
    if len(city) < 2:
        raise ValueError("City name is too short")
    return city


# =========================
# Weather Generation
# =========================

def generate_weather(seed: Optional[int] = None) -> WeatherData:
    """
    Generate simulated weather data.
    Optional seed enables deterministic behavior for tests.
    """
    if seed is not None:
        random.seed(seed)

    return WeatherData(
        temperature=random.randint(-5, 45),
        humidity=random.randint(20, 90),
        wind_speed=random.randint(0, 20),
        condition=random.choice(WEATHER_CONDITIONS),
    )


# =========================
# Alert Engine
# =========================

def generate_alerts(weather: WeatherData) -> List[str]:
    """
    Generate alerts based on configured rules.
    """
    alerts = []

    for rule in ALERT_RULES.values():
        if "temp_min" in rule and weather.temperature >= rule["temp_min"]:
            alerts.append(rule["message"])

        elif "temp_max" in rule and weather.temperature <= rule["temp_max"]:
            alerts.append(rule["message"])

        elif "wind_min" in rule and weather.wind_speed >= rule["wind_min"]:
            alerts.append(rule["message"])

        elif "conditions" in rule and weather.condition in rule["conditions"]:
            alerts.append(rule["message"])

    return alerts


# =========================
# Report Formatting
# =========================

def format_report(city: str, weather: WeatherData, alerts: List[str]) -> str:
    """
    Create a formatted weather report string.
    """
    lines = []
    lines.append("Weather Report")
    lines.append("-" * 14)
    lines.append(f"City: {city}")
    lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"Temperature: {weather.temperature}°C")
    lines.append(f"Humidity: {weather.humidity}%")
    lines.append(f"Wind Speed: {weather.wind_speed} km/h")
    lines.append(f"Condition: {weather.condition}")

    if alerts:
        lines.append("\nAlerts:")
        for alert in alerts:
            lines.append(f"- {alert}")
    else:
        lines.append("\nNo alerts. Weather is normal.")

    return "\n".join(lines)


# =========================
# Application Entry Point
# =========================

def main() -> None:
    try:
        city_input = input("Enter city name: ")
        city = validate_city(city_input)

        weather = generate_weather()
        alerts = generate_alerts(weather)

        report = format_report(city, weather, alerts)
        print("\n" + report)
