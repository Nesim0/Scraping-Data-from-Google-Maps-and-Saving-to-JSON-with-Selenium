import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

browser = webdriver.Chrome()
search = ""
browser.get(f"https://www.google.com/maps/search/{search}")

browser.fullscreen_window()

try:
    wait = WebDriverWait(browser, 20)  # 20 saniyelik bekleme süresi
    scrollable_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')))

    browser.execute_script("""
        var scrollableDiv = arguments[0];

        function scrollWithinElement(scrollableDiv) {
            return new Promise((resolve, reject) => {
                var totalHeight = 0;
                var distance = 1000;
                var scrollDelay = 1000;

                var timer = setInterval(() => {
                    var scrollHeightBefore = scrollableDiv.scrollHeight;
                    scrollableDiv.scrollBy(0, distance);
                    totalHeight += distance;

                    if (totalHeight >= scrollHeightBefore) {
                        totalHeight = 0;
                        setTimeout(() => {
                            var scrollHeightAfter = scrollableDiv.scrollHeight;
                            if (scrollHeightAfter > scrollHeightBefore) {
                                return;
                            } else {
                                clearInterval(timer);
                                resolve();
                            }
                        }, scrollDelay);
                    }
                }, scrollDelay);
            });
        }

        return scrollWithinElement(scrollableDiv);
    """, scrollable_element)

    time.sleep(10)

except TimeoutException:
    print("Sayfa yüklenemedi veya element bulunamadı.")

items = browser.find_elements(By.CSS_SELECTOR, "div[role='feed'] > div > div[jsaction]")

result = []
for item in items:
    data = {}
    
    try:
        data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
        result.append(data) 
    except Exception:
        print("Başlık çekilemedi!")
        data['title'] = "Title bulunamadı!"
    try:
        data['score'] = item.find_element(By.CSS_SELECTOR, ".MW4etd").text
    except Exception:
        print("Score çekilemedi!")
        data['score'] = "Score bulunamadı!"
    try:
        data['link'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
    except Exception:
        print("Link çekilemedi!")
        data['link'] = "Link bulunamadı!"
    try:
        data['website'] = item.find_element(By.CSS_SELECTOR, ".lcr4fd.S9kvJb ").get_attribute('href')
    except Exception:
        print("web site çekilemedi")
        data['website'] = "Site bulunamadı!"
        

with open('sonuclar.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("Veriler JSON dosyasına başarıyla yazıldı!")
