from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from collections import Counter

# Install and setup WebDriver
driver = webdriver.Edge()

# Visit T-Series Dailymotion page
t_series_url = 'https://www.dailymotion.com/tseries2'
driver.get(t_series_url)

# Scroll down to load videos dynamically
for _ in range(15):  # Adjust the range if necessary to load enough videos
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    
    time.sleep(1)  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
# Sleep to allow new videos to load



# Collect the video URLs
video_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')
video_urls = [elem.get_attribute('href') for elem in video_elements[:500]]

# Extract video IDs from URLs
video_ids = [url.split('/video/')[1] for url in video_urls]

# Find and count the most frequently repeated character in video IDs
all_ids_combined = ''.join(video_ids).lower()  # Case-insensitive search
char_counter = Counter(all_ids_combined)
most_common_char, most_common_count = char_counter.most_common(1)[0]

# Print the result
print(f'{most_common_char}:{most_common_count}')

# Clean up
driver.quit()
