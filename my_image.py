import requests
import os
from PIL import Image
from io import BytesIO


class MyImage:
    def __init__(self, url: str) -> None:
        self.url = url
        self.downloaded_image = self._get()
        self.modified_image = None

    def _get(self) -> Image.Image | None:
        try:
            img_request = requests.get(self.url)
            if img_request.status_code == 200:
                return Image.open(BytesIO(img_request.content))
        except OSError as e:
            print(e)

    def save(self, name: str, img_type='downloaded', format_to_jpg=False):
        format = self.downloaded_image.format.lower()
        if img_type == 'downloaded':
            modified_name = ''
            image_to_save = self.downloaded_image
        else:
            modified_name = '_'+img_type
            image_to_save = self.modified_image
        if format_to_jpg:
            format = 'jpg'
        directory = os.path.dirname(os.path.abspath(__file__))  # директория исполняемого файла
        fp = os.path.join(directory, 'saved_pictures', f'{name+modified_name}.{format}')

        try:
            image_to_save.save(fp)
        except FileNotFoundError as e:
            # print(e)
            os.chdir(directory)
            os.mkdir('saved_pictures')
            image_to_save.save(fp)
        return fp

    def resize_by_height(self, new_height: int):
        new_width = int(new_height / self.downloaded_image.height * self.downloaded_image.width)
        self.modified_image = self.downloaded_image.resize((new_width, new_height))

    def apply_filter(self):
        pass


if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_img = MyImage(test_url)
    print(test_img.downloaded_image.size, test_img.downloaded_image.format)

