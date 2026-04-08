import json
import os
import base64
from pypdf import PdfWriter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_html_as_pdf(html_file_path, output_pdf_path):
    chrome_options = Options()
    # Required flags for running Chrome in GitHub Actions (Linux CI)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # CRITICAL: Passing the options into the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Convert relative path to absolute file URL
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

        # Use Chrome DevTools Protocol to generate PDF
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

        with open(output_pdf_path, "wb") as f:
            f.write(base64.b64decode(result['data']))

        print(f"✅ PDF saved to: {output_pdf_path}")

    except Exception as e:
        print(f"❌ Failed to generate PDF for {html_file_path}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    i = 1
    merger = PdfWriter()
    
    # If a file is in 'ready', it won't be re-generated.
    # NOTE: On GitHub Actions, these files won't exist unless you committed them to the repo.
    ready = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20]
    
    # Loop through all HTML files named 1.html, 2.html, etc.
    while os.path.exists("{}.html".format(i)):
        html_file = "{}.html".format(i)
        pdf_file = "{}.pdf".format(i)
        
        if i not in ready:
            save_html_as_pdf(html_file, pdf_file)
        
        # Only merge if the PDF actually exists to avoid FileNotFoundError
        if os.path.exists(pdf_file):
            merger.append(pdf_file)
            print(f"➕ Merged {pdf_file}")
        else:
            print(f"⚠️ Skipping {pdf_file} (File not found)")
            
        i += 1

    # Final output
    output_filename = "missale_ready.pdf"
    with open(output_filename, "wb") as f:
        merger.write(f)
    
    merger.close()
    print(f"🏁 Done! Final file: {output_filename}")
    
