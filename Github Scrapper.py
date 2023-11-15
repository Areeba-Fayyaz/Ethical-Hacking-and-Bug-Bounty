from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from urllib.parse import urljoin

# Setting up the Chrome driver
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# URL of the GitHub user whose repositories will be scanned
github_user = 'https://github.com/Areeba-Fayyaz/'
driver.get(github_user)
time.sleep(2)  # Pausing to allow the page to load

# Finding all elements that represent repositories
repositories = driver.find_elements(By.CLASS_NAME, 'repo')

# Lists to store repository links and file links within repositories
repository_links = []
repository_file_links = []

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to click the 'Raw' button in a GitHub file view
def click_raw(file_link):
    driver.get(file_link)
    print(file_link)
    try:
        # Waiting for the raw button to be clickable
        raw = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="raw-button"]'))
        )
        raw.click()
        # Checking the page source for the presence of 'password'
        html = driver.page_source
        if 'password' in html:
            print('Found password in: ', file_link)
    except Exception as e:
        print(f"Error occurred: {e}")

# Collecting links to each repository
for repository in repositories:
    repository_links.append(github_user + repository.text + '/')

print(repository_links)

# Visiting each repository and collecting links to Python files
for link in repository_links:
    driver.get(link)
    repository_files = driver.find_elements(By.CLASS_NAME, 'js-navigation-open')

    for file_element in repository_files:
       if '.py' in file_element.text:
           repository_file_links.append(file_element.get_attribute("href"))
    
# Processing each Python file link
for file_link in repository_file_links:
    click_raw(file_link)

# Close the driver after completing the tasks
driver.quit()
