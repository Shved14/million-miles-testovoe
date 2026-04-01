from __future__ import annotations

import re
from typing import Iterable

from playwright.sync_api import Page, sync_playwright

from parser.config import CarPayload, ParserSettings


def _to_int(text: str) -> int:
    digits = re.sub(r"[^0-9]", "", text or "")
    return int(digits) if digits else 0


def _safe_text(page: Page, selector: str) -> str:
    el = page.query_selector(selector)
    return (el.inner_text().strip() if el else "").strip()


def _safe_attr(page: Page, selector: str, attr: str) -> str:
    el = page.query_selector(selector)
    return (el.get_attribute(attr) or "").strip() if el else ""


def scrape_encar(settings: ParserSettings, max_items: int = 20) -> list[CarPayload]:
    url = "https://www.encar.com"

    items: list[CarPayload] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.run_headless)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        page.wait_for_timeout(2000)
        cards = page.query_selector_all("a")

        for a in cards:
            if len(items) >= max_items:
                break

            href = (a.get_attribute("href") or "").strip()
            text = (a.inner_text() or "").strip()

            if not href or not text:
                continue

            # Heuristic: skip too short
            if len(text) < 10:
                continue

            # Defaults
            brand = "Unknown"
            model = "Unknown"
            year = 0
            mileage = 0
            price = 0
            image_url = None

            # Very rough parsing attempt from visible text
            m_year = re.search(r"(19\d{2}|20\d{2})", text)
            if m_year:
                year = int(m_year.group(1))

            # try to infer price / mileage if present
            mileage = _to_int(text)  # fallback
            price = 0

            items.append(
                CarPayload(
                    brand=brand,
                    model=model,
                    year=year,
                    mileage=mileage,
                    price=price,
                    image_url=image_url,
                )
            )

        browser.close()

    return items
