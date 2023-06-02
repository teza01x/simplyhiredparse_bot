import time
import warnings
from config import *
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from to_exsls import *


class Objects:
    def __init__(self, wait):
        self.wait = wait


    def job_list(self, job_list):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, job_list)))
            return True
        except:
            return False


    def check_count_offers(self, browser, ul_class, current_website):
        try:
            links = list()
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            ul_list = soup.find('ul', class_=ul_class)
            li_list = ul_list.find_all('li')
            for i in li_list:
                href_value = i.find('a', href=True)['href']
                links.append(current_website+href_value)
            li_count = len(li_list)
            return li_count, links
        except:
            return 0, []


    def navigate_by_offers(self, current_offer):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, current_offer))).click()
        except Exception as e:
            print("Error {}".format(e))


    def scan_offer(self, browser, right_menu_class, title_class, right_menu_css, company_id, detail_text, company_location, time_class, posting_id, info_selector):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, right_menu_css)))
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, info_selector)))
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            right_menu = soup.find('div', class_=right_menu_class)
            try:
                title = right_menu.find('h2', class_=title_class).get_text()
            except:
                title = "None"
            try:
                company_name = right_menu.find('span', attrs={'data-testid': company_id}).find('span', attrs={'data-testid': detail_text}).get_text()
            except:
                company_name = "None"
            try:
                job_location = right_menu.find('span', attrs={'data-testid': company_location}).find('span', attrs={'data-testid': detail_text}).get_text()
            except:
                job_location = "None"
            try:
                time_posted = right_menu.find('div', class_=time_class).find('span', attrs={'data-testid': posting_id}).find('span', attrs={'data-testid': detail_text}).get_text()
                time_posted = time_posted.split(' ')
                time_posted = int(time_posted[0])
            except:
                time_posted = "None"
            return [company_name, title, job_location, time_posted]
        except Exception as e:
            print("Error {}".format(e))


    def next_page(self, next_page_xpath):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, next_page_xpath))).click()
            return True
        except:
            return False


class Objects_v2():
    def __init__(self, wait):
        self.wait = wait


    def job_list(self, job_list):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, job_list)))
            return True
        except:
            return False


    def check_count_offers(self, browser, ul_class):
        links = list()
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        body = browser.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(1)
        try:
            ul_list = soup.find('ul', class_=ul_class)
            li_list = ul_list.find_all('li')
            li_count = len(li_list)
            return li_count
        except:
            return 0


    def navigate_by_offers(self, browser, current_offer, left_menu_class, link_class):
        try:
            print(current_offer)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, current_offer)))
            jb_offer = browser.find_element(By.CSS_SELECTOR, current_offer)
            browser.execute_script("arguments[0].scrollIntoView();", jb_offer)
            jb_offer.click()
            print("кликнул")
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            left_menu = soup.find('div', left_menu_class)
            active_job_offer = left_menu.find('article', class_=link_class).find('a', href=True)['href']
            print("удачно")
            return active_job_offer
        except:
            return None


    def scan_offer(self, browser, right_menu_class, title_class, right_menu_css, company_class, c_location_class, time_class, info_selector):
        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, right_menu_css)))
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, info_selector)))
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            right_menu = soup.find('div', class_=right_menu_class)
            try:
                title = right_menu.find('div', class_=title_class).get_text()
            except:
                title = "None"
            try:
                company_name = right_menu.find('div', class_=company_class).get_text()
            except:
                company_name = "None"
            try:
                elements = right_menu.find_all('div', class_=c_location_class)
                if len(elements) >= 2:
                    job_location = elements[1].text
            except:
                job_location = "None"
            try:
                element = right_menu.find('span', class_=time_class)
                time_text = element.text
                time_text = time_text.split(' ')

                for i in time_text:
                    for j in "0123456789":
                        if j in i:
                            time_posted = int(i)
                            break
            except:
                time_posted = "None"
            return [company_name, title, job_location, time_posted]
        except Exception as e:
            print("Error {}".format(e))


    def next_page(self, next_page_xpath):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, next_page_xpath))).click()
            time.sleep(5)
            return True
        except:
            return False


def main_other(browser, country):
    wait = WebDriverWait(browser, 15)
    objects = Objects_v2(wait)
    current_html_cfg = country_dicts[1]
    now = datetime.now()
    for one_page in range(total_pages):
        try:
            time.sleep(5)
            if objects.job_list(current_html_cfg["job_list"]) == True:
                count_offers = objects.check_count_offers(browser, current_html_cfg["ul_class"])
                if count_offers > 0:
                    job_page_info = list()
                    for i in range(1, count_offers+1):
                        href = objects.navigate_by_offers(browser, current_html_cfg["li_css"].format(i), current_html_cfg["left_menu_class"], current_html_cfg["link_class"])
                        time.sleep(1.5)
                        try:
                            if href != None:
                                offer_text_info = objects.scan_offer(browser, current_html_cfg["right_menu_class"], current_html_cfg["title_class"], current_html_cfg["right_menu_css"],
                                                   current_html_cfg["company_class"], current_html_cfg["c_location_class"], current_html_cfg["time_class"], current_html_cfg["offer_info_selector"])
                                link = country + href
                                offer_text_info.insert(0, link)
                                offer_text_info.insert(0, platform)
                                offer_text_info.append(status)
                                offer_text_info.append(int(now.strftime("%d")))
                                if len(offer_text_info) == 8:
                                    job_page_info.append(offer_text_info)
                                else:
                                    pass
                        except:
                            pass
                        time.sleep(2)
                    add_new_data(job_page_info)
                    print("<Added a page to the table, you can check>")
            time.sleep(5)
            if objects.next_page(current_html_cfg["next_page_xpath"]) == True:
                print("<Going on next page>")
                time.sleep(5)
            else:
                break
        except Exception as e:
            print("Error: {}".format(e))


def main_usa(browser):
    wait = WebDriverWait(browser, 20)
    objects = Objects(wait)
    current_html_cfg = country_dicts[0]
    for one_page in range(total_pages):
        try:
            time.sleep(5)
            if objects.job_list(current_html_cfg["job_list"]) == True:
                count_offers, job_offer_links = objects.check_count_offers(browser, current_html_cfg["ul_class"], current_html_cfg["current_website"])
                if count_offers > 0:
                    job_page_info= list()
                    for i in range(2, count_offers+1):
                        offer_text_info = objects.scan_offer(browser, current_html_cfg["right_menu_class"], current_html_cfg["title_class"], current_html_cfg["right_menu_css"],
                                           current_html_cfg["company_id"], current_html_cfg["detail_text"], current_html_cfg["company_location"], current_html_cfg["time_class"],
                                           current_html_cfg["posting_id"], current_html_cfg["offer_info_selector"])
                        job_page_info.append(offer_text_info)
                        objects.navigate_by_offers(current_html_cfg["li_css"].format(i))
                        time.sleep(2)
                    now = datetime.now()
                    for i in range(len(job_page_info)):
                        job_page_info[i].insert(0, job_offer_links[i])
                        job_page_info[i].insert(0, platform)
                        job_page_info[i].append(status)
                        job_page_info[i].append(int(now.strftime("%d")))
                    add_new_data(job_page_info)
                    print("<Added a page to the table, you can check>")
            time.sleep(5)
            if objects.next_page(current_html_cfg["next_page_xpath"]) == True:
                print("Going on next page>")
                time.sleep(5)
            else:
                break
        except Exception as e:
            print("Error {}".format(e))


def main(browser, country):
    if country == "simplyhired.com":
        main_usa(browser)
    else:
        main_other(browser, country)


if __name__ == "__main__":
    options = Options()
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    options.binary_location = chrome_path
    browser = Chrome("chromedriver.exe", chrome_options=options)
    wait = WebDriverWait(browser, 20)
    browser.maximize_window()

    url = 'https://{}/search?q={}&fdb=1&sb=dd&s=d&t=1'

    while True:
        for country in countries:
            for key in keywords:
                try:
                    browser.get(url.format(country, key))
                    try:
                        main(browser, country)
                    except:
                        pass
                except:
                    pass