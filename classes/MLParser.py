from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re
import requests
import os
from progress.bar import IncrementalBar

def stethem_write(name,data):
    with open(name+'.json', 'w') as outfile:
        json.dump(data, outfile)
def stethem_reader(name):
    with open(name+'.json', "r") as infile:
        return json.load(infile)


def check_and_cre_folder(dirname):
        if not os.path.isdir(dirname):
            os.mkdir(dirname)


class MLParser:

    chromedriver_path='chromedriver.exe'
    image_folder='img'
    page_links=set()
    image_links={}
    def __init__(self, manga_name):
        self.manga_name = manga_name


    def get_page(self,url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.page = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=options)
        self.page.get(url)
    
    def download_all_from_page(self):
        url=f'https://mangalib.me/{self.manga_name}?section=chapters'
        self.get_page(url)
        for i in range(0,100):
            self.page.execute_script(f"window.scrollTo(0, {i*200})")
            self.pageges_list_builder()
        self.images_list_builder()
    
    def pageges_list_builder(self) -> None:
        page_body = BeautifulSoup(self.page.page_source, 'lxml')
        link_divs=page_body.find("div", class_="media-chapters-list").find_all("div", class_="media-chapter__name")
        for link_div in link_divs:
            self.page_links.add(link_div.find("a", class_="link-default", href=True)['href'])

    def images_list_builder(self):
        bar = IncrementalBar('images_list_builder', max = len(self.page_links))
        self.page_links
        for url in self.page_links:
            self.get_page('https://mangalib.me'+str(url))
            self.get_image_url(str(url))
            bar.next()
        bar.finish()
        stethem_write("image_links-{self.manga_name}",self.image_links)


    def get_image_url(self,url):
        self.image_links[url]=[]
        soup = BeautifulSoup(self.page.page_source, 'lxml')
        pages_cnt=int(re.findall(r'[0-9]+',str(soup.find("label", class_="reader-pages__label")))[1])
        for i in range(1,pages_cnt):
            self.page.execute_script(f'document.querySelector(".reader-paginate__item_right").click()')
        soup = BeautifulSoup(self.page.page_source, 'lxml')
        imgs=soup.find("div", class_="reader-view__container").find_all("img")
        for img in imgs:
            self.image_links[url].append(img.get('src'))


    def download_images(self):
        # pages=self.image_links
        pages=stethem_reader("image_links-{self.manga_name}")
        check_and_cre_folder(self.image_folder)
        books_folder=os.path.join(self.image_folder,self.manga_name)
        check_and_cre_folder(books_folder)
        {self.manga_name}
        image_cnt=0
        for page in pages:
            image_cnt+=len(pages[page])
        bar = IncrementalBar('download_images', max = image_cnt)
        for page in pages:
            img_folder=os.path.join(books_folder,page[1:].replace('/','-'))
            check_and_cre_folder(img_folder)
            
    
            while len(pages[page])>0:
                try:
                    img_name=re.search(r'[.\w]+.\w+$',pages[page][0]).group(0)
                    img_path=os.path.join(img_folder,img_name)
                    if not os.path.exists(img_path) or os.path.getsize(img_path)<50000:
                        resp=self.file_download(pages[page][0])
                        if resp.status_code!=200:
                            continue
                        self.save_image(img_path,resp.content)
                    del pages[page][0]
                    bar.next()
                except:
                    print('err',pages[page][0])
        bar.finish()


    def file_download(self,link):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
            }
        resp = requests.get(link, headers=headers, allow_redirects=True)
        return(resp)

    def save_image(self,img_path,content):
        img = open(img_path,'wb')
        img.write(content)
        img.close()
        
        

