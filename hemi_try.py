# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def hemi(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
    for image in img_soup.find_all('div', class_='item'):
        hemispheres = {}
        if image.find('a', class_='itemLink product-item'):
            image_link = image.find(href=True).get('href')
            link = url+image_link
            browser.visit(link)
            enhan_img_soup = soup(browser.html, 'html.parser')
            full_image_elem = enhan_img_soup.find('img', class_='wide-image').get('src')
            img_url = url+full_image_elem
            hemispheres.update({'url_image': img_url})
            hemi_title = image.find('h3').text
            hemispheres.update({'title': hemi_title})
            hemisphere_image_urls.append(hemispheres)
    return hemisphere_image_urls

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())