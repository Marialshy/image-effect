import requests
import os
from abc import ABC, abstractmethod
from enum import Enum
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
import skimage as ski



class ImageService(ABC):
    @abstractmethod
    def load(self, path: str):
        pass

    @abstractmethod
    def resize(self, image, size: tuple[int, int]):
        pass

    @abstractmethod
    def save(self, image, path: str):
        pass

    @abstractmethod
    def show(self, image):
        pass

    @abstractmethod
    def apply_filter(self, image, filter, params: dict):
        pass


class ImgFilters(Enum):
    blur = 'Blur image by given radius. Radius 1 takes 1 pixel in each direction, i.e. 9 pixels in total. (default radius = 5)'
    sharpen = 'Sharpen image'
    smooth = 'Smooth image'
    filter = 'Create a mode filter. Picks the most frequent pixel value in a box (3*3 pixels)'


class PILImageService(ImageService):
    def load(self, path: str):
        if os.path.isfile(path):
            return Image.open(path)

        try:
            img_request = requests.get(path)
            if img_request.status_code == 200:
                return Image.open(BytesIO(img_request.content))
        except OSError as e:
            return e

    def resize(self, image: Image.Image, size: tuple[int, int]): 
        return ImageOps.fit(image, size)
        # return image.resize(size) # (ширина, высота), без применения масштабирования

    def save(self, image: Image.Image, path: str):
        file_path = os.path.split(path)
        if os.path.isdir(file_path[0]):
            image.save(path)
            return path

        directory = os.path.dirname(os.path.abspath(__file__))  # директория исполняемого файла
        fp = os.path.join(directory, 'saved_img_pil')
        if not os.path.isdir(fp):
            os.chdir(directory)
            os.mkdir('saved_img_pil')
        try:
            path = os.path.join(fp, path)
            image.save(path)
        except ValueError:
            path = os.path.join(fp, f'{path}.{image.format.lower()}')
            image.save(path)
        except FileNotFoundError:
            path = os.path.join(fp, f'{file_path[1]}')
            image.save(path)
        return path
    
    def show(self, image: Image.Image):
        image.show()

    def apply_filter(self, image: Image.Image, filter: ImgFilters, params = {}):
        if filter == ImgFilters.blur:
            blur_radius = params.get('radius', 5)
            return image.filter(ImageFilter.BoxBlur(blur_radius))
        
        elif filter == ImgFilters.sharpen:
            return image.filter(ImageFilter.SHARPEN())
        
        elif filter == ImgFilters.smooth:
            return image.filter(ImageFilter.SMOOTH())
        
        elif filter == ImgFilters.filter:
            return image.filter(ImageFilter.ModeFilter())
        

class SkiImageService(ImageService):
    def load(self, path: str):
        ski.io.imread(path)
        return super().load(path)
        





if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_PIL = PILImageService()
    # test_PIL.save(test_PIL.load(test_url), 'test') #ValueError: unknown file extension: 
    # except ValueError: or FileNotFoundError
    # print(test_PIL.save(test_PIL.load(test_url), '3-test.jpg'))
    # print(test_PIL.save(test_PIL.load(test_url), '.\\image_effect\\saved_test\\1_test.jpg'))
    
    # loaded = test_PIL.load(test_url)
    # print(loaded.format, loaded.size)
    # test_PIL.resize(loaded, (180,300)).show()
    # test_PIL.resize(loaded, (150,1080)).show()

    # test_PIL.apply_filter(loaded, ImgFilters.blur, {'radius': 1.2}).show()
    # test_PIL.apply_filter(loaded, ImgFilters.blur).show()
    # test_PIL.apply_filter(loaded, ImgFilters.sharpen).show()
    # test_PIL.apply_filter(loaded, ImgFilters.smooth).show()
    # test_PIL.apply_filter(loaded, ImgFilters.filter).show()


