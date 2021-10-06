from selenium import webdriver
from bs4 import BeautifulSoup
from os import path

class MLParser:

    chromedriver_path='chromedriver.exe'
    
    def page_parser(self, url):
        # return 1
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=options)
        browser.get(url)
        requiredHtml = browser.page_source
        # print(requiredHtml)
        soup = BeautifulSoup(requiredHtml, 'lxml')
        link_div=soup.find_all("div", class_="media-chapters-list")
        # links=link_div.find_all("a", class_="link-default")

        print(link_div)

    
    def pageges_list_builder(self):
        pages=[]

        return pages
    def pageges_list_builder(self):
        pages=[]

        return pages

    def images_list_builder(self, pages):

        images=[]
        for i in pages:
            image_urls=[]


            images.append({"page":i, "image_urls":image_urls})

        return images