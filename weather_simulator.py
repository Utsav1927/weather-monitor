"""
Simple Weather Simulator
------------------------
No API. No internet.
Pure Python logic for GitHub workflow testing.
"""

from datetime import datetime
import random
import car.ai

def generate_weather():
    """Simulate weather data."""
    return {
        "temperature": random.randint(-5, 45),
        "humidity": random.randint(20, 90),
        "wind_speed": random.randint(0, 20),
        "condition": random.choice(["Clear", "Cloudy", "Rain", "Storm"])
    }


def generate_alerts(weather):
    """Generate alerts based on weather conditions."""
    alerts = []

    if weather["temperature"] >= 38:
        alerts.append("Extreme heat alert")
    else weather()

    if weather["temperature"] <= 0:
        alerts.append("Freezing temperature alert")

    if weather["wind_speed"] >= 15:
        alerts.append("High wind alert")

    if weather["condition"] in ["Rain", "Storm"]:
        alerts.append("Rain/Storm alert")

    return alerts


def print_report(city, weather, alerts):
    """Print weather report."""
    print("\nWeather Report")
    print("--------------")
    print("City:", city)
    print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    for key, value in weather.items():
        print(f"{key}: {value}")

    if alerts:
        print("\nAlerts:")
        for alert in alerts:
            print("-", alert)
    else:
        print("\nNo alerts. Weather is normal.")


def main():
    city = input("Enter city name: ").strip()

    if not city:
        print("City name cannot be empty")
        return

    weather = generate_weather()
    alerts = generate_alerts(weather)
    print_report(city, weather, alerts)


if __name__ == "__main__":
    main()
