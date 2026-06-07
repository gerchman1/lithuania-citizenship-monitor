from playwright.sync_api import sync_playwright
import requests
import os
import json
import re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

STATE_FILE = "last_result.json"

SEARCH_URL = "https://e-seimas.lrs.lt/portal/documentSearch/lt"

TITLE_TEXT = "Dėl Lietuvos Respublikos pilietybės atkūrimo"


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True
        }
    )


def load_last():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_last(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(SEARCH_URL, wait_until="networkidle")

    page.fill(
        "#searchCompositeComponent\\:contentForm\\:searchParamPane\\:j_id_30\\:paramAdoptionNo",
        "1V"
    )

    page.fill(
        "#searchCompositeComponent\\:contentForm\\:searchParamPane\\:j_id_30\\:j_id_55\\:autoComplete_input",
        "Lietuvos Respublikos vidaus reikalų ministerija"
    )

    page.fill(
        "#searchCompositeComponent\\:contentForm\\:searchParamPane\\:j_id_30\\:paramContent",
        "pilietybės"
    )

    page.click(
        "#searchCompositeComponent\\:contentForm\\:searchParamPane\\:searchButton"
    )

    page.wait_for_timeout(5000)

    links = page.locator("a").all()

    target_link = None

    for link in links:

        text = link.inner_text().strip()

        if TITLE_TEXT in text:
            target_link = link
            break

    if not target_link:
        raise Exception(
            "Nenhum decreto de cidadania encontrado."
        )

    href = target_link.get_attribute("href")

    if href.startswith("/"):
        href = "https://e-seimas.lrs.lt" + href

    current = {
        "url": href
    }

    previous = load_last()

    if previous.get("url") != current["url"]:

        send_telegram(
            "🚨 Novo decreto de restauração de cidadania encontrado:\n\n"
            + href
        )

        save_last(current)

    browser.close()
