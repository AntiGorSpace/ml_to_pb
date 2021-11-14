import os
import re
from progress.bar import IncrementalBar
from PIL import Image as PILImage

import funcs.castFuncs as cf

class PdfBuilder:
    
    
    
    def __init__(self, manga_name):
        self.manga_name = manga_name
        self.images_lists = {}
        self.pdfs_images_lists=[[]]
        self.book_folder = os.path.join('files','img',self.manga_name)
        self.pdf_folder = os.path.join('files','pdf')
        cf.check_and_cre_folder(self.pdf_folder)
        self.res_folder = os.path.join('files','pdf',self.manga_name)
        cf.check_and_cre_folder(self.res_folder)
        self.book_list_builder()

    def book_list_builder(self):
        self.books_list=os.listdir(self.book_folder)
        self.books_list.sort(key=lambda e:float(e))
        self.images_lists_builder()
    
    def images_lists_builder(self):
        for book in self.books_list:
            image_folder = os.path.join(self.book_folder,book)
            self.images_lists[book] = os.listdir(image_folder)
            self.images_lists[book].sort(key = lambda e:float(re.search(r'\d+',e).group(0)))
        self.pdfs_images_lists_builder()
    
    def pdfs_images_lists_builder(self):

        for book in self.books_list:
            image_folder=os.path.join(self.book_folder,book)
            last_index=len(self.pdfs_images_lists)-1
            last_el_len=len(self.pdfs_images_lists[last_index])
            if last_el_len>0 and last_el_len+len(self.images_lists[book])>100:
                self.pdfs_images_lists.append([])
                last_index+=1
            for img in self.images_lists[book]:
                if  True: self.pdfs_images_lists[last_index].append(os.path.join(image_folder, img))
        self.create_pdfs()

    def create_pdfs(self):
        bar = IncrementalBar('create_pdfs', max = len(self.pdfs_images_lists))
        for i in range(0, len(self.pdfs_images_lists)):
            pdfimages=[]
            for image in self.pdfs_images_lists[i]:
                try:
                    pdfimages.append(PILImage.open(image).convert('RGB'))
                except:
                    print('error',image)
                    break
            
            file_name='0'*(4-len(str(i+1)))+str(i+1)+'.pdf'
            file_path=os.path.join(self.res_folder,file_name)
            pdfimages[0].save(file_path,save_all=True, append_images=pdfimages[1:])
            bar.next()
        bar.finish()



                

