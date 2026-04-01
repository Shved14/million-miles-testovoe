from parser.config import CarPayload

import httpx


async def save_to_db(api_base_url: str, cars: list[CarPayload]) -> int:
    created = 0
    async with httpx.AsyncClient(base_url=api_base_url, timeout=30) as client:
        for car in cars:
            try:
                resp = await client.post("/cars", json=car.model_dump())
                resp.raise_for_status()
                created += 1
            except Exception:
                continue
    return created
