"""Check which N.html pages overflow their A5 page and how much room is left.

Usage: python check_fit.py [first [last]]
Renders the pages in one headless Chrome session (no PDFs written) and prints,
for each page, the number of PDF pages it produces and the free space at the
bottom in mm (negative = overflow).
"""
import base64
import io
import os
import sys

from pypdf import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PX_PER_MM = 96 / 25.4
# @page in styles.css: 148x210 mm, margins 5/2 mm top/bottom, 16.5 mm left/right
CONTENT_W_MM = 148 - 2 * 16.5
CONTENT_H_MM = 210 - 5 - 2


def main():
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    last = int(sys.argv[2]) if len(sys.argv) > 2 else None

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    try:
        i = first
        while os.path.exists(f"{i}.html") and (last is None or i <= last):
            driver.get("file://" + os.path.abspath(f"{i}.html"))
            driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {"media": "print"})
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": round(CONTENT_W_MM * PX_PER_MM), "height": 400,
                "deviceScaleFactor": 1, "mobile": False,
            })
            height_px = driver.execute_script(
                "return document.documentElement.scrollHeight;")
            free_mm = CONTENT_H_MM - height_px / PX_PER_MM

            pdf = driver.execute_cdp_cmd("Page.printToPDF", {
                "printBackground": True, "preferCSSPageSize": True,
            })
            pages = len(PdfReader(io.BytesIO(base64.b64decode(pdf["data"]))).pages)

            status = "OK" if pages == 1 else "OVERFLOW"
            print(f"{i:>3}.html  pages={pages}  free≈{free_mm:6.1f} mm  {status}", flush=True)
            i += 1
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
