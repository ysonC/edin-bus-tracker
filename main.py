from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_departure_info(url):
    # Set up Chrome options (headless mode so it doesn't open a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the Chrome WebDriver 
    service = Service("chromedriver.exe")  # Work with chrome 129.0
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Load the webpage
        driver.get(url)

        # Wait for the departure board to be loaded (adjust time if needed)
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'lb-l-livebustimes-departure'))
        )

        # Find the departure elements
        departures = driver.find_elements(By.CLASS_NAME, 'lb-l-livebustimes-departure')

        departure_list = []

        # Iterate over each departure item and extract details
        for item in departures:
            service_name = item.find_element(By.CLASS_NAME, 'lb-o-livebustimes-departure-servicename').text.strip()
            next_time = item.find_element(By.CLASS_NAME, 'lb-o-livebustimes-departure-nexttime').text.strip()
            further_times = item.find_element(By.CLASS_NAME, 'lb-o-livetimespanel-departure-furthertimes').text.strip()

            departure_list.append({
                'service': service_name,
                'next_time': next_time,
                'further_times': further_times
            })

        return departure_list

    except Exception as e:
        print(f"Error fetching the webpage: {e}")
        return None
    finally:
        driver.quit()

# Test the function with the Lothian Buses URL
url = "https://www.lothianbuses.com/live-travel-info/live-bus-times/?stop_id=6200242650"
departures = fetch_departure_info(url)
print(departures)
