
# Import Splinter and BeautifulSoup
from splinter import Browser, browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#function to initialize the browser and create a dict
def scrape_all():
    #initiate the headless driver for deployment
    #executable_path and browser path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    #url_image, title = hemi(browser)
    hemisphere_image_urls = hemi(browser)
    #url_image, title = hemisphere_image_urls
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "url_hemi": hemisphere_image_urls,
      #"url_image": url_image,
      #"title" : title
    }
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try: 
        slide_elem = news_soup.select_one('div.list_text')
        ##slide_elem.find('div', class_='content_title')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_p, news_title


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None


        # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    #expert to a dataframe
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html(classes="table table-hover")
    

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
    #print(hemispheres)
        #return(hemispheres)
    return hemisphere_image_urls   
    #    return hemispheres
    

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())
    #print(hemi(browser))

