# import dependecies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import pandas as pd
import os


# initialize browser
def init_browser():
  
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    browser = init_browser()

    # create Mars dictionary that can be imported into Mongo
    mars_info = {}    


    ##################
    # NASA Mars News #
    ##################
   # Visit Nasa news url through splinter module
    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)

    time.sleep(1)

    # HTML object
    mars_html = browser.html

    # Parse HTML with BeautifulSoup
    mars_soup = bs(mars_html, "html.parser")
   
    ### code to get all nasa news ###
    mars_lists = mars_soup.find_all('div', class_ = 'list_text')

    titles_list = []
    paragraphs_list = []

    # iterate all the news list
    for mars_list in mars_lists:

        title = mars_list.find('div', class_='content_title').text
    
        paragraph = mars_list.find('div', class_='article_teaser_body').text
       
        #Append both to a list
        titles_list.append(title)
        paragraphs_list.append(paragraph)

    # get the first title and paragraph
    news_title = titles_list[0]
    news_p = paragraphs_list[0]    

    ### Store data in a dictionary ###
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
   
   

    #####################
    # Mars Space Images #
    #####################

    # visit mars image url through splinter module
    mars_image_url = 'https://spaceimages-mars.com'
   
    # HTML object
    browser.visit(mars_image_url)

    time.sleep(1)

    # find and click the full image button
    browser.find_by_css('a.showimg.fancybox-thumbs').click()
   
    # parse HTML with BeautifulSoup
    soup = bs(browser.html,'html.parser')

    # find tag 'img'
    end = soup.find('img', class_='headerimage')['src']
   
    # cocatenate website url with scrapped route and store in variable feature_image_url
    feature_image_url = "https://spaceimages-mars.com"+"/"+end

   
    ### store feature image in the dictionary ###
    mars_info['feature_image_url'] = feature_image_url
   
   
   
    ##################
    #    Mars Facts  #
    ##################

    # visit Mars facts URL
    facts_url = 'https://galaxyfacts-mars.com'

    # use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Mars', 'Earth']

    # get rid of trailing colon
    mars_df['Description'] = mars_df['Description'].str[:-1]

    # set the index to the `Description` column without row indexing
    mars_df = mars_df.set_index('Description')

    facts_html_table = mars_df.to_html()
    facts_html_table = facts_html_table.replace('\n', '')
   
   
    ### store facts in the dictionary ###
    mars_info['facts_html_table'] = facts_html_table
   
   
    ###################
    # Mars Hemisphere #
    ###################

   
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit hemispheres website through splinter module
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)

    time.sleep(1)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemisphere_image_urls = []

    # Store the main_ul
    hemispheres_main_url = 'https://marshemispheres.com/'

    # Loop through the items previously stored
    for i in items:
        img_dict = {}
        # Store title
        title = i.find('h3').text
   
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
   
        # Visit the link that contains the full image website
        browser.visit(hemispheres_main_url + partial_img_url)
   
        # HTML Object of individual hemisphere information website
        partial_img_html = browser.html
   
        # Parse HTML with Beautiful Soup for every individual hemisphere information website
        soup = bs( partial_img_html, 'html.parser')
   
        # Retrieve full image source
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
   
        img_dict["title"] = title
        img_dict["img_url"] = img_url
    
        hemisphere_image_urls.append(img_dict)

    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
 
    # close the browser after scrapping
    browser.quit()

    # return results
    return mars_info

#a = scrape()
#print(a)