from __future__ import annotations

import re
from typing import Any

from playwright.async_api import Error as PlaywrightError, Page, async_playwright

from parser.config import CarPayload, ParserSettings


def _to_int(text: str) -> int:
    digits = re.sub(r"[^0-9]", "", text or "")
    return int(digits) if digits else 0


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _extract_brand_model(title: str) -> tuple[str, str]:
    title = _normalize_whitespace(title)
    if not title:
        return "Unknown", "Unknown"

    parts = title.split(" ")
    if len(parts) == 1:
        return parts[0], "Unknown"
    return parts[0], " ".join(parts[1:])


def _extract_year(text: str) -> int:
    m = re.search(r"\b(19\d{2}|20\d{2})\b", text or "")
    return int(m.group(1)) if m else 0


def _extract_price(text: str) -> int:
    return _to_int(text)


def _extract_mileage(text: str) -> int:
    return _to_int(text)


async def _goto_and_wait(page: Page, url: str) -> None:
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    try:
        await page.wait_for_load_state("networkidle", timeout=15000)
    except PlaywrightError:
        pass
    await page.wait_for_timeout(1500)


async def _extract_cards(page: Page) -> list[Any]:
    candidates = [
        "li[data-index]",
        "li:has(a[href*='dc_cardetailview'])",
        "div:has(a[href*='dc_cardetailview'])",
        "a[href*='dc_cardetailview']",
    ]

    for sel in candidates:
        try:
            loc = page.locator(sel)
            cnt = await loc.count()
            if cnt >= 5:
                return [loc.nth(i) for i in range(cnt)]
        except PlaywrightError:
            continue

    loc = page.locator("a")
    cnt = await loc.count()
    return [loc.nth(i) for i in range(min(cnt, 200))]


async def _extract_from_card(card: Any) -> dict[str, Any]:
    try:
        title = ""
        for sel in [
            "[class*='title']",
            "[class*='name']",
            "[class*='car'] [class*='name']",
            "strong",
            "h3",
            "h2",
        ]:
            try:
                loc = card.locator(sel).first
                if await loc.count() > 0:
                    title = _normalize_whitespace(await loc.inner_text(timeout=1000))
                    if title:
                        break
            except PlaywrightError:
                continue

        if not title:
            try:
                title = _normalize_whitespace(await card.inner_text(timeout=1000))
            except PlaywrightError:
                title = ""

        img_url = ""
        for attr in ["src", "data-src", "data-original"]:
            try:
                loc = card.locator("img").first
                if await loc.count() == 0:
                    break
                img_url = ((await loc.get_attribute(attr, timeout=1000)) or "").strip()
                if img_url:
                    break
            except PlaywrightError:
                continue

        raw_text = title
        try:
            raw_text = _normalize_whitespace(await card.inner_text(timeout=1000))
        except PlaywrightError:
            pass

        year = _extract_year(raw_text)

        price_text = raw_text
        mileage_text = raw_text

        brand, model = _extract_brand_model(title)

        if brand == "Unknown" and model == "Unknown":
            brand, model = _extract_brand_model(raw_text)

        return {
            "brand": brand,
            "model": model,
            "year": year,
            "mileage": _extract_mileage(mileage_text),
            "price": _extract_price(price_text),
            "image_url": img_url or None,
        }
    except Exception:
        return {}


async def scrape_encar(settings: ParserSettings, max_items: int = 20) -> list[CarPayload]:
    url = settings.list_url

    items: list[CarPayload] = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=settings.run_headless)
            context = await browser.new_context(
                user_agent=settings.user_agent,
                viewport={"width": 1400, "height": 900},
            )
            page = await context.new_page()
            page.on("pageerror", lambda _: None)

            await _goto_and_wait(page, url)

            cards = await _extract_cards(page)

            for card in cards:
                if len(items) >= max_items:
                    break

                data = await _extract_from_card(card)
                if not data:
                    continue

                if not data.get("brand") or not data.get("model"):
                    continue

                items.append(CarPayload(**data))

            await context.close()
            await browser.close()

    except Exception:
        return items

    return items
