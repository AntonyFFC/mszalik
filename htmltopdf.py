import json
import os
from pypdf import PdfWriter
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def save_html_as_pdf(html_file_path, output_pdf_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Must be headless for print commands
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        import os
        absolute_path = "file://" + os.path.abspath(html_file_path)
        driver.get(absolute_path)

        print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,

        }

        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

        with open(output_pdf_path, "wb") as f:
            f.write(base64.b64decode(result['data']))

        print(f"PDF saved to: {output_pdf_path}")

    finally:
        driver.quit()


# Usage
if __name__ == "__main__":
    i = 1
    merger = PdfWriter()
    ready = []
    # ready = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    while os.path.exists("{}.html".format(i)):
        if i not in ready:
            save_html_as_pdf("{}.html".format(i), "{}.pdf".format(i))
        merger.append("{}.pdf".format(i))
        i += 1
    merger.write("missale_ready.pdf")
    print("All merged!")
