from optparse import Values
from webook import selectors
from webook.urls import URL
from playwright.sync_api import sync_playwright, TimeoutError

def save_as_pdf(links: list[URL], tempdir: str, options: Values) -> list[str]:
    pdfs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=options.headless)
        page = browser.new_page()
        for link in links:
            page_selectors = selectors.for_url(link.url, options.delete_element_file)
            try:
                page.goto(link.url, timeout=options.wait_seconds * 1000)
            except TimeoutError:
                if not options.ignore_wait_error:
                    raise
            # page.wait_for_event('domcontentloaded')
            # remove elemtents
            for selector in page_selectors:
                if selector:
                    for elem in page.query_selector_all(selector):
                        elem.evaluate('e => e.remove()')

            if options.js_file:
                with open(options.js_file, 'r') as f:
                    js = f.read()
                    page.evaluate(js)

            # save as PDF
            pdf = f'{tempdir}/{link.title}.pdf'
            page.pdf(path=pdf, outline=True, tagged=True)
            pdfs.append(pdf)
    return pdfs