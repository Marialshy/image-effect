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
    def resize(self, image,  height: int, width: int):
        pass

    def check_path(self, path: str):
        file_path = os.path.split(path)
        directory = self.__check_dir(file_path[0])

        checked_path = os.path.join(directory, file_path[1])
        f_extension = os.path.splitext(file_path[1])[1]
        if f_extension:
            return checked_path, False
        return checked_path, True

    def __check_dir(self, dir_path: str):
        if os.path.isdir(dir_path):
            return dir_path
        directory = os.path.dirname(os.path.abspath(__file__))  # директория исполняемого файла
        fp = os.path.join(directory, 'saved_img')
        if not os.path.isdir(fp):
            os.chdir(directory)
            os.mkdir('saved_img')
        return fp

    @abstractmethod
    def save(self, image, path: str):
        pass

    @abstractmethod
    def show(self, image):
        pass

    @abstractmethod
    def apply_filter(self, image, filter_type, params: dict):
        pass

    def set_filters(self, functions: list):
        keys = [ImgFilters.blur, ImgFilters.sharpen, ImgFilters.smooth, ImgFilters.filter]
        return {k: v for k, v in zip(keys, functions)}


class ImgFilters(Enum):
    blur = 1
    sharpen = 2
    smooth = 3
    filter = 4


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

    def resize(self, image: Image.Image, height: int, width: int):
        return ImageOps.fit(image, (width, height))
        # return image.resize(size) # без применения масштабирования

    def save(self, image: Image.Image, path: str):
        fp = self.check_path(path)
        checked_path = fp[0]
        if fp[1]:
            checked_path += '.' + image.format.lower()
        try:
            image.save(checked_path)
        except OSError as e:
            return e
        return checked_path

    def show(self, image: Image.Image):
        image.show()

    def apply_filter(self, image: Image.Image, filter_type: ImgFilters, params={}):
        filter_functions = [ImageFilter.BoxBlur(params.get('blur', 5)),
                            ImageFilter.SHARPEN(), ImageFilter.SMOOTH(), ImageFilter.ModeFilter(size = 6)]
        filters = self.set_filters(filter_functions)
        return image.filter(filters.get(filter_type))


class SkiImageService(ImageService):
    def load(self, path: str):
        try:
            return ski.io.imread(path)
        except (FileNotFoundError, urllib.error.HTTPError, urllib.error.URLError):
            return None

    def show(self, image):
        ski.io.imshow(image)
        plt.show()

    def resize(self, image, height: int, width: int):
        height_crop, width_crop = self.evaluate_crop_size(image, height, width)
        if height_crop or width_crop:
            image = ski.util.crop(image, ((height_crop, height_crop), (width_crop, width_crop), (0, 0)))

        return ski.transform.resize(image, (height, width), anti_aliasing=True)

    def evaluate_crop_size(self, image, height, width):
        # skimage.util.crop(ar, crop_width, copy=False, order='K')[source]
        # Crop array ar by crop_width along each dimension.

        height_crop, width_crop = 0, 0
        acceptable_diff = 0.05
        image_ratio = image.shape[0]/image.shape[1]
        size_ratio = height/width
        ratio = image_ratio - size_ratio

        if ratio >= acceptable_diff:
            height_crop = int((image.shape[0] - image.shape[1]*size_ratio)/2)
        elif ratio <= acceptable_diff:
            width_crop = int((image.shape[1] - image.shape[0]/size_ratio)/2)
        return height_crop, width_crop

    def save(self, image, path: str, extension='.jpg'):
        fp = self.check_path(path)
        checked_path = fp[0]
        if fp[1]:
            checked_path += extension
        try:
            ski.io.imsave(checked_path, image)
        except OSError as e:
            return e
        return checked_path

    def apply_filter(self, image, filter_type: ImgFilters, params={}):
        def my_filter(image):
            img = ski.exposure.equalize_adapthist(image, clip_limit=0.007)
            bw_img = ski.filters.butterworth(img, cutoff_frequency_ratio=0.01)
            img += bw_img*0.0015
            return img

        filters_list = [
            lambda: ski.filters.gaussian(image, sigma=params.get('blur', 5), channel_axis=-1),
            lambda: ski.filters.unsharp_mask(image, params.get('sharpen_r', 0.52), params.get('sharpen_a', 7), channel_axis=2),
            lambda: ski.restoration.denoise_bilateral(image, channel_axis=-1),
            lambda: my_filter(image)
        ]
        filters = self.set_filters(filters_list)
        return (filters.get(filter_type)()* 255).round().astype(plt.np.uint8)


if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_url2 = 'https://i.pinimg.com/564x/91/74/10/917410946ed00961e793dd28622dc84b.jpg'
    test_url_h = 'https://i.pinimg.com/originals/4c/d1/40/4cd140e29a0d499d8fc8fe7adf0924e0.jpg'
    test_url_403 = 'https://i.pinimg.com/564x/91/74/10/917410946ed0e793dd28622dc84b.jpg'
    test_url_sh = 'https://i.pinimg.com/564x/23/17/6a/23176ad95fd1fbc051635fdc0152a874.jpg'
    test_path = '.\\saved_img_pil\\test-1.jpg'
    test_PIL = PILImageService()
    # print(test_PIL.load(test_url_403))
    # test_PIL.save(test_PIL.load(test_url), 'test') #ValueError: unknown file extension:
    # except ValueError: or FileNotFoundError
    # print(test_PIL.save(test_PIL.load(test_url), '3-test.jpg'))
    # print(test_PIL.save(test_PIL.load(test_url), '  $& /cha"?:s'))
    # print(test_PIL.save(test_PIL.load(test_url), 'abs_test'))
    # print(test_PIL.save(test_PIL.load(test_url), '.\\saved_img\\1_test.jpg'))
    # print(test_PIL.save(test_PIL.load(test_url), 'D:\\learning\\python_practice\\files_user\\saved_pictures\\test_abstract_saved.jpg'))

    loaded = test_PIL.load(test_url)
    # print(loaded.format, loaded.size)
    # test_PIL.resize(loaded, 180,300).show()
    # test_PIL.resize(loaded, 150,1080).show()

    # test_PIL.apply_filter(loaded, ImgFilters.blur, {'radius': 1.2}).show()
    # test_PIL.apply_filter(loaded, ImgFilters.blur).show()
    # test_PIL.apply_filter(loaded, ImgFilters.sharpen).show()
    # test_PIL.apply_filter(loaded, ImgFilters.smooth).show()
    test_PIL.apply_filter(loaded, ImgFilters.filter).show()

    test_ski = SkiImageService()
    # print(test_ski.load('.\\saved_test\\1_test.jpg'))
    # print(test_ski.load(test_url_403))
    # img_ski = test_ski.load(test_url)
    img_ski = test_ski.load(test_url2)
    # test_ski.show(img_ski)
    # print('height:', img_ski.shape[0], 'width:', img_ski.shape[1])
    # test_ski.show(test_ski.resize(img_ski, 700, 200))
    # test_ski.show(test_ski.resize(img_ski, 300, 350))
    # test_ski.show(test_ski.resize(img_ski, 800, 1080))
    # test_ski.save(img_ski, 'test-s')
    # test_ski.show(test_ski.load(test_url_sh))
    # test_ski.show(ski.filters.unsharp_mask(test_ski.load(test_url_sh), 1, 10))
    # test_ski.show(ski.filters.unsharp_mask(test_ski.load(test_url_sh), 0.47, 5, channel_axis=2))
    # test_ski.show(ski.filters.unsharp_mask(test_ski.load(test_url_sh), 0.4, 7, channel_axis=2))
    # test_ski.show(ski.filters.gaussian(test_ski.load(test_url_sh), sigma=1, channel_axis=2))  # blur
    # test_ski.show(ski.filters.gaussian(test_ski.load(test_url_sh), sigma=6, channel_axis=2))  # blur
    # test_ski.show(ski.filters.gaussian(test_ski.load(test_url_sh), truncate=0.1, channel_axis=2))
    # test_ski.show(ski.filters.butterworth(test_ski.load(test_url_sh)))

    test_my_filtered = test_ski.apply_filter(img_ski, ImgFilters.filter)
    # test_blured = test_ski.apply_filter(img_ski, ImgFilters.blur)
    # test_sharpen = test_ski.apply_filter(img_ski, ImgFilters.sharpen)
    # test_smooth = test_ski.apply_filter(img_ski, ImgFilters.smooth)
    # print(type(test_my_filtered))
    # print(test_my_filtered.__dir__())
    # print(test_my_filtered.__array__())
    # print(test_blured.__array__()) # float
    # print(test_sharpen.__array__()) # float
    # print(test_smooth.__array__()) # float
    test_ski.show(test_my_filtered)
    # test_ski.show(test_ski.apply_filter(test_ski.load(test_url2), ImgFilters.filter))
    # test_ski.show(test_ski.apply_filter(test_ski.load(test_url_sh), ImgFilters.filter))
    # test_ski.show(test_ski.apply_filter(test_ski.load(test_url_h), ImgFilters.filter))
