import requests
import urllib
import os
from abc import ABC, abstractmethod
from enum import Enum
from PIL import Image, ImageFilter, ImageOps
from matplotlib import pyplot as plt
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
        except OSError:  # as e:
            return None

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

    def apply_filter(self, image: Image.Image, filter: ImgFilters, params={}):
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
        try:
            return ski.io.imread(path)
        except (FileNotFoundError, urllib.error.HTTPError):
            return None

    def show(self, image):
        ski.io.imshow(image)
        plt.show()

    def resize(self, image, size: tuple[int, int]):
        height_crop, width_crop = self.evaluate_crop_size(image, size)
        if height_crop or width_crop:
            image = ski.util.crop(image, ((height_crop, height_crop), (width_crop, width_crop), (0, 0)))

        return ski.transform.resize(image, size, anti_aliasing=True)

    def evaluate_crop_size(self, image, size):
        # skimage.util.crop(ar, crop_width, copy=False, order='K')[source]
        # Crop array ar by crop_width along each dimension.

        height_crop, width_crop = 0, 0
        acceptable_diff = 0.05
        image_ratio = image.shape[0]/image.shape[1]
        size_ratio = size[0]/size[1]  # (height/width)
        ratio = image_ratio - size_ratio
        
        if ratio >= acceptable_diff:
            height_crop = int((image.shape[0] - image.shape[1]*size_ratio)/2)
        elif ratio <= acceptable_diff:
            width_crop = int((image.shape[1] - image.shape[0]/size_ratio)/2)
        return height_crop, width_crop

    def save(self, image, path: str):
        return super().save(image, path)

    def apply_filter(self, image, filter, params: dict):
        return super().apply_filter(image, filter, params)


if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_url2 = 'https://i.pinimg.com/564x/91/74/10/917410946ed00961e793dd28622dc84b.jpg'
    test_url_h = 'https://i.pinimg.com/originals/4c/d1/40/4cd140e29a0d499d8fc8fe7adf0924e0.jpg'
    test_url_403 = 'https://i.pinimg.com/564x/91/74/10/917410946ed0e793dd28622dc84b.jpg'
    test_path = '.\\saved_img_pil\\test-1.jpg'
    test_PIL = PILImageService()
    # print(test_PIL.load(test_url_403))
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

    test_ski = SkiImageService()
    # print(test_ski.load('.\\saved_test\\1_test.jpg'))
    # print(test_ski.load(test_url_403))
    # img_ski = test_ski.load(test_url)
    img_ski = test_ski.load(test_url)
    test_ski.show(img_ski)
    # print('height:', img_ski.shape[0], 'width:', img_ski.shape[1])
    test_ski.show(test_ski.resize(img_ski, (450, 280)))
    test_ski.show(test_ski.resize(img_ski, (300, 350)))
    test_ski.show(test_ski.resize(img_ski, (800, 1080)))
