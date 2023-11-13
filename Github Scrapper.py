
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from urllib.parse import urljoin


s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

github_user='https://github.com/Areeba-Fayyaz/'
driver.get('https://github.com/Areeba-Fayyaz/')
time.sleep(2)


repositories = driver.find_elements(By.CLASS_NAME,'repo')

repository_links=[]
repository_file_links=[]

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_raw(file_link):
    driver.get(file_link)
    print(file_link)
    try:
        # Wait for the raw button to be clickable
        raw = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="raw-button"]'))
        )
        raw.click()
        html = driver.page_source
        html = f'{html}'
        if 'password' in html:
            print('Found password in: ', file_link)
    except Exception as e:
        print(f"Error occurred: {e}")


for repository in repositories:
    repository_links.append(github_user+repository.text+'/')

print(repository_links)

for link in repository_links:
    driver.get(link)
    repository_files = driver.find_elements(By.CLASS_NAME,'js-navigation-open')

    for file_element in repository_files:
       if '.py' in file_element.text:
           repository_file_links.append(file_element.get_attribute("href"))
    
for file_link in repository_file_links:
    click_raw(file_link)
    # print(repository_files)
# print(repository_file_links)

