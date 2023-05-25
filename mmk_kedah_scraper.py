from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib import parse
import time
from datetime import datetime
import csv

options = Options()
options.add_argument("--detach")
base_url = "https://mmk.kedah.gov.my"
servis = Service("geckodriver.exe")
browser = webdriver.Firefox(service=servis)


def main():
    print("Mulai scrape web...")
    browser.get(parse.urljoin(base_url, "kerajaan/ahli-yang-berhormat/ahli-dewan-undangan-negeri"))
    groups = browser.find_elements(By.CSS_SELECTOR, ".accordion-group")
    
    results = list()
    for group in groups:
        element = group.find_element(By.CSS_SELECTOR, ".accordion-heading")
        element.click()
        # browser.execute("""document.querySelector(".accordion-heading").click()""")
        time.sleep(3)
        inner_html = elem.get_attribute("innerHTML") if (elem := group.find_element(By.CSS_SELECTOR, ".accordion-inner.panel-body")) else ""
        if inner_html:
            souped = BeautifulSoup(inner_html, "html.parser")
            rows = souped.select("table tr")
            if rows:
                result = {
                        "name": col.get_text(strip=True, separator=" ") if (col := rows[0].select("td")[1]) else "",
                        "address": col.get_text(strip=True, separator=" ") if (col := rows[1].select_one("td")) else "",
                        "telephone": col.get_text(strip=True, separator=" ") if (col := rows[2].select("td")[1]) else "",
                        "fax": col.get_text(strip=True, separator=" ") if (col := rows[3].select("td")[1]) else "",
                        "email": col.get_text(strip=True, separator=" ") if (col := rows[4].select("td")[1]) else "",
                        "facebook": col.get_text(strip=True, separator=" ") if (col := rows[5].select("td")[1]) else "",
                        "photo_link": parse.urljoin(base_url, img_src) if (img_src := rows[0].select("td")[0].select_one("img").get("src", None))
                                      else ""
                }
                
                results.append(result)
                
    browser.quit()
    
    filename = "MMK_Kedah_ahli_DUN_{}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    
    print(f"Save to {filename}...")
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=("name", "address", "telephone", "fax", "email", "facebook", "photo_link"))
            writer.writeheader()
            writer.writerows(results)
            f.close()
        print("Berhasil...")
    except Exception as e:
        print(f"{e}")
        

if __name__ == "__main__":
    main()
