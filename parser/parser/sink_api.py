import requests

from parser.config import CarPayload


def push_to_api(api_base_url: str, cars: list[CarPayload]) -> int:
    created = 0
    for car in cars:
        resp = requests.post(f"{api_base_url}/cars", json=car.model_dump(), timeout=30)
        resp.raise_for_status()
        created += 1
    return created
