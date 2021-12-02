
from classes.MLParser import MLParser
from classes.PdfBuilder import PdfBuilder


# import os
# mlp = MLParser('naruto')
# resp=mlp.file_download('https://img33.cdnlibs.link//manga/naruto/chapters/72-695/02.jpg')

# mlp.save_image(os.path.join('files','img','naruto','695','2.png'),resp.content)


for i in ['the-fable']:
    mlp = MLParser(i)
    mlp.download_all_from_page()

    # pb = PdfBuilder(i)

