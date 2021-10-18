import io
from selenium import webdriver
from PIL import Image

import time
import os
import sys
import requests

# DRIVER_PATH = wherever your chromedriver is.
# Put the path for your ChromeDriver here

DRIVER_PATH = 'C:\\Users\ethan\\Documents\\chromedriver\\chromedriver.exe'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)

def fetch_image_urls(query, max_links_to_fetch, wd:webdriver, googleWait=1):

    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(googleWait)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = []
    image_count = 0
    results_start = 0

    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        
        
        for img in thumbnail_results[results_start:len(thumbnail_results)]:
            # try to click every thumbnail such that we can get the real image behind it
            
            img.click()
            time.sleep(googleWait)
            
            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')

            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.append(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if image_count >= max_links_to_fetch:
                print(f"Found: {image_count} image links, done!")
                break

        else:
            print(f"Found: {image_count} image links, looking for more ...")
            time.sleep(30)

            return
        

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

fetch_urls = fetch_image_urls('Traffic Barrel', 5, wd)

def persist_image(folder_path,url,counter):
    

    if url[-4:] == '.jpg' or url[-4:] == '.png' or url[-4:] == '.gif' or url[-5:] == '.jpeg':
        
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')

            file_path = os.path.join(folder_path, 'trafficBarrel' + str(counter) + '.jpg')

            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)

            print(f"SUCCESS - saved {url} - as {file_path}")

        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")

   
    print(url[-4:] != '.png')
    return None,None



print(fetch_urls)

counter = 0 

for i in fetch_urls:

    counter += 1
    persist_image('C:\\Users\\ethan\\OneDrive\\Documents\\Test\\charolette', i, counter)
    




