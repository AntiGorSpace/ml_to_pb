
from classes.MLParser import MLParser

# mlp=MLParser('akame-ga-kill')
mlp=MLParser('naruto')
mlp.download_all_from_page()
mlp.download_images()
