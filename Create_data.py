import random
import json
from datetime import datetime, timedelta

def create_flight(existing_flights):
    destinations = ["Paris", "New York", "Tokyo", "Sydney", "Moscow", "Rio de Janeiro", "Cape Town", "Dubai", "Rome", "Shanghai", "London", "Berlin", "Beijing", "Brasília", "Cairo", "Canberra", "Oslo", "Bangkok", "Dublin", "Wellington", "Stockholm", "Athens", "Madrid", "Hanoi"]
    airline_companies = ["VietNam Airline", "Vietjet Air", "Korean Airline", "Emirates", "American Airlines", "Qatar Airways", "Singapore Airlines", "Bangkok Airline", "Laos Airline", "Metaverse Airline", "Trump Airline"]
    start_time = datetime.now() + timedelta(days=random.randint(1, 365))
    stop_time = start_time + timedelta(hours=random.randint(2, 24), minutes=random.randint(0, 59))

    while True:
        new_flight = {
            "Id_flight": random.choice(airline_companies),
            "Name_flight": f"{' - '.join(random.sample(airline_companies, 2))} - {random.choice(destinations)}",
            "Time_start": start_time.strftime("%d/%m/%Y at %H:%M %p"),
            "Time_stop": stop_time.strftime("%d/%m/%Y at %H:%M %p"),
            "image": "https://up-anh.vi-vn.vn/img/1714472726_793df46dc62672cdeb3295dca94e55d5.jpg",
        }

        # Kiểm tra xem chuyến bay mới có trùng với các chuyến bay hiện có không
        if new_flight not in existing_flights:
            return new_flight

existing_flights = []

for _ in range(1000):
    new_flight = create_flight(existing_flights)
    existing_flights.append(new_flight)

with open("flights.json", "w") as f:
    json.dump(existing_flights, f, indent=4)
