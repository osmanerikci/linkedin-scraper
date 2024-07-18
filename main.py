from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
count = 0
options = Options()
options.add_argument(r'''user-data-dir=C:\Users\LENOVO\OneDrive - marmara.edu.tr\Projects\Linkedin-scraper\User Data''')
options.add_argument("--start-maximized");
driver = webdriver.Edge(options=options)

# LinkedIn job listings page URL
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
    global count
    # Find the ul element by class name
    ul_element = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
    jobs_list = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
    # Find all li elements within the ul
    li_elements = ul_element.find_elements(By.CLASS_NAME,'jobs-search-results__list-item')
    for li in li_elements:
        li.location_once_scrolled_into_view
        li.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'job-details')))
        time.sleep(0.3)
        title_elem = li.find_element(By.TAG_NAME, 'strong')
        job_title = title_elem.text.strip() if title_elem else 'N/A'
        
        company_elem = li.find_element(By.CLASS_NAME, 'job-card-container__primary-description')
        company_name = company_elem.text.strip() if company_elem else 'N/A'
        
        location_elem = li.find_element(By.CLASS_NAME, 'job-card-container__metadata-item')
        job_location = location_elem.text.strip() if location_elem else 'N/A'
        
        description_elem = driver.find_element(By.ID, 'job-details')
        job_description = description_elem.text.strip().removeprefix("İş ilanı hakkında\n").replace('\\n', '').replace('\\t', '') if description_elem else 'N/A'
        
        try:
            seniortiy_elem = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-insight-view-model-secondary')
            job_seniority = seniortiy_elem.text.strip() if seniortiy_elem else 'N/A'
        except:
            job_seniority = 'N/A'
        
        job_data = {
        'Title': job_title,
        'Company': company_name,
        'Location': job_location,
        'Description': job_description,
        'Seniority': job_seniority
        }

        # Append the job data to the list
        count += 1
        print(f"{count} jobs scraped")
        jobs_data.append(job_data)
        #print(job_data)


    try:
        next_page_button = driver.find_element(By.CLASS_NAME, 'jobs-search-pagination__button--next')
        next_page_button.click()
    except:
        print("No more pages left")
        return
    

scrape_page()
while(next_page_exists()):
    scrape_page()
    
    


df = pd.DataFrame(jobs_data)
excel_filename = 'linkedin_jobs.xlsx'
df.to_excel(excel_filename, index=False)
# Display the DataFrame
print(df.head())



# Close the browser session
driver.quit()