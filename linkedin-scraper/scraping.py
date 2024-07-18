from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_linkedin_jobs():
    options = Options()
    options.headless = True
    options.add_argument(r'user-data-dir=C:\Users\LENOVO\OneDrive - marmara.edu.tr\Projects\linkedin-analysis\User Data')
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(options=options)

    url = 'https://www.linkedin.com/jobs/search/?currentJobId=3968403108&distance=25&f_E=1%2C2%2C3&f_TPR=r86400&f_WT=2%2C3&geoId=91000000&keywords=developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))

    jobs_data = []

    def next_page_exists():
        try:
            driver.find_element(By.CLASS_NAME, 'jobs-search-pagination__button--next')
            return True
        except:
            return False
    
    def scrape_page():
        ul_element = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
        li_elements = ul_element.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
        for li in li_elements:
            li.location_once_scrolled_into_view
            li.click()
            wait.until(EC.visibility_of_element_located((By.ID, 'job-details')))
            time.sleep(0.2)
            job_data = extract_job_data(li)
            jobs_data.append(job_data)

        try:
            next_page_button = driver.find_element(By.CLASS_NAME, 'jobs-search-pagination__button--next')
            next_page_button.click()
        except:
            return

    def extract_job_data(li):
        job_title = li.find_element(By.TAG_NAME, 'strong').text.strip()
        company_name = li.find_element(By.CLASS_NAME, 'job-card-container__primary-description').text.strip()
        job_location = li.find_element(By.CLASS_NAME, 'job-card-container__metadata-item').text.strip()
        job_description = driver.find_element(By.ID, 'job-details').text.strip().removeprefix("İş ilanı hakkında\n").replace('\\n', '').replace('\\t', '')
        try:
            job_seniority = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-insight-view-model-secondary').text.strip()
        except:
            job_seniority = 'N/A'

        return {
            'Title': job_title,
            'Company': company_name,
            'Location': job_location,
            'Description': job_description,
            'Seniority': job_seniority
        }

    scrape_page()
    while next_page_exists():
        scrape_page()
    
    driver.quit()
    return jobs_data

jobs = scrape_linkedin_jobs()
print(jobs)
