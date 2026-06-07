from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        "https://e-seimas.lrs.lt/portal/documentSearch/lt"
    )

    page.wait_for_timeout(10000)

    print("URL:", page.url)
    print("Título:", page.title())

    page.screenshot(
        path="screenshot.png",
        full_page=True
    )

    with open(
        "page.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(page.content())

    browser.close()
