import sys
from image_service import PILImageService, ImgFilters, SkiImageService


class UI:
    def __init__(self, img_service: str, path: str) -> None:
        self.img_service = img_service
        self.path = path
        self.actions = [self.quit, self.show, self.save, self.resize, self.apply_filter]
        self.__image_service = self.__apply_image_service()
        self.__image = self.load()
        if self.__image is None:
            raise AttributeError

    def __apply_image_service(self):
        if self.img_service == 'pil':
            return PILImageService()
        elif self.img_service == 'ski':
            return SkiImageService()

    def load(self):
        loaded_img = self.__image_service.load(self.path)
        return loaded_img  # уточнить ошибку (None, e) (?)

    def run(self):
        print('\n\t --- * ---')
        for action in enumerate(self.actions):
            print(f'\t{action[0]}: {action[1].__name__}')
        self.select_action()

    def select_action(self):
        input_msg = f'Please insert number 0 - {len(self.actions)-1} to continue: '
        err_msg = 'Try again. Enter number to select action.'
        act = self.get_input_value(input_msg, err_msg, (0, len(self.actions)))
        self.actions[int(act)]()

    def quit(self):
        print('\t -> quit')
        sys.exit()

    def save(self):
        filepath = self.get_file_path()
        try:
            self.__image_service.save(self.__image, filepath)
            print(f'\t saved: {filepath}')
        except OSError:
            print('Incorrect path. Try again')
            self.save(self.__image)

    def show(self):
        self.__image_service.show(self.__image)

    def resize(self):
        width = self.get_new_picture_width()
        height = self.get_new_picture_height()
        self.__image = self.__image_service.resize(self.__image, height, width)

    def apply_filter(self):
        filter_type = self.get_filter_type()
        if filter_type in (ImgFilters.blur, ImgFilters.sharpen):
            # params = self.get_filter_params(self)
            pass
        self.__image = self.__image_service.apply_filter(self.__image, filter_type)  # тут нет параметров

    def get_file_path(self):
        return input('Please enter file name or path to save: ')

    def get_input_value(self, input_msg: str, err_msg: str, comparison_range: tuple[int, int]):
        inputed = input(input_msg)
        try:
            if int(inputed) in range(*comparison_range):
                return int(inputed)
            raise ValueError
        except ValueError:
            print(err_msg)
            return self.get_input_value(input_msg, err_msg, comparison_range)

    def get_new_picture_width(self):
        input_msg = "Enter a new width to resize the image: "
        err_msg = 'incorrect input, should be integer in range 120 - 1080 px. Try again'
        return self.get_input_value(input_msg, err_msg, (120, 1081))

    def get_new_picture_height(self):
        input_msg = "Enter a new height to resize the image: "
        err_msg = 'incorrect input, should be integer in range 120 - 1080 px. Try again'
        return self.get_input_value(input_msg, err_msg, (120, 1081))

    def get_filter_type(self):
        filter_description = [
            'blur image by given radius e.g. = 1 - takes 1 pixel in each direction \
            \n\t(9 pixels in total). Possible to set blur intensity Default radius = 5',
            'sharpen image, possible to set parametrs',
            'smooth image',
            'custom filter, result depends on choosen image service']
        print('\n > Availiable options:')
        for type in zip(ImgFilters, filter_description):
            print(f'\t>  {type[0].value}. {type[0].name.title()}: {filter_description[type[0].value-1]}')

        input_msg = "Select filter (by number): "
        err_msg = "incorrect filter type, try again"
        selected = self.get_input_value(input_msg, err_msg, (1, len(ImgFilters)+1))
        return ImgFilters(int(selected))


if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_url_h = 'https://i.pinimg.com/originals/4c/d1/40/4cd140e29a0d499d8fc8fe7adf0924e0.jpg'
    # test_ui = UI('PILImageService', test_url)
    test_ui = UI('pil', test_url_h)
    # test_ui2 = UI('PILImageService', '.\\saved_img_pil\\test-1.jpg') # AttributeError: 'MissingSchema' object has no attribute 'save'

    # test_ui.run()
    test_ui.resize()
