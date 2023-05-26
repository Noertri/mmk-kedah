import csv
import time
from datetime import datetime
from urllib import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import sys


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
                cols = list()
                for row in rows:
                    tds = [col.get_text(strip=True, separator=" ") for col in row.select("td")]
                    if any(tds):
                        cols.append(tds)
                        
                result = {
                        "name": cols[0][1],
                        "position": "Member of the State Legislative Assembly (Ahli Dewan Undangan Negeri)/State Legislative Assembly (Dewan "
                                    "Undangan Negeri), Kedah",
                        "address": cols[1][0],
                        "telephone": cols[2][1],
                        "fax": cols[3][1],
                        "email": cols[4][1],
                        "facebook": cols[5][1],
                        "photo_link": parse.urljoin(base_url, img_src) if (img_src := rows[0].select("td")[0].select_one("img").get("src", None))
                                      else ""
                }
                
                print(result)
                results.append(result)
                
    browser.quit()
    
    if input("Save results to file?[Y/n]: ").lower() == "y":
        filename = "MMK_Kedah_ahli_DUN_{}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    
        print(f"Save to {filename}...")
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, delimiter=";", fieldnames=("name", "position", "address", "telephone", "fax", "email", "facebook",
                                                                      "photo_link"))
                writer.writeheader()
                writer.writerows(results)
                f.close()
            print("Berhasil...")
        except Exception as e:
            print(f"{e}")
        

if __name__ == "__main__":
    main()
