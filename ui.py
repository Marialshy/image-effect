import sys
from image_service import PILImageService, ImgFilters, SkiImageService, ImageService
import numpy as np


class UI:
    def __init__(self, img_service: ImageService, path: str) -> None:
        self.__image_service = img_service
        self.path = path
        self.actions = [self.quit, self.show, self.save, self.resize, self.apply_filter]
        self.__image = None
        self.loading_error = None
        self.load()

    def load(self):
        loading_result = self.__image_service.load(self.path)
        self.__image = loading_result[0]
        self.loading_error = loading_result[1]
        if self.loading_error:
            print(self.loading_error)
            raise AttributeError

    def run(self):
        print('--- * ---\n\tSelect action:')
        for action in enumerate(self.actions):
            print(f'\t{action[0]}: {action[1].__name__}')
        self.select_action()

    def select_action(self):
        input_msg = f'\t press 0 - {len(self.actions)-1} to continue : \n'
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
        filter_params = self.__image_service.filter_params
        filter_type = self.get_filter_type()
        params = {}
        if filter_type in (ImgFilters.blur, ImgFilters.sharpen) and self.need_set_filter_params():
            keys = filter_params.get(filter_type)
            params = self.get_filter_params(keys)
        self.__image = self.__image_service.apply_filter(self.__image, filter_type, params)

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
            \n\t(9 pixels in total). Possible to set blur intensity Default radius = 5.',
            'sharpen image, possible to set parameters',
            'smooth image',
            'custom filter, result depends on choosen image service']
        print('\n > Availiable options:')
        for type in zip(ImgFilters, filter_description):
            print(f'\t>  {type[0].value}. {type[0].name.title()}: {filter_description[type[0].value-1]}')

        input_msg = "Select filter (by number): "
        err_msg = "incorrect filter type, try again"
        selected = self.get_input_value(input_msg, err_msg, (1, len(ImgFilters)+1))
        return ImgFilters(int(selected))

    def need_set_filter_params(self) -> bool:
        need_set = input('Do you want to set the parmeters manually [y/n]?: ')
        if need_set == 'y':
            return True
        return False

    def get_filter_params(self, keys: list):
        params = {}

        def get_float_value(inp_msg, err_msg, comparison_r):
            try:
                param = float(input(inp_msg))
                if param in np.arange(*comparison_r, 0.01):
                    return param
                raise ValueError
            except ValueError:
                print(err_msg)
                return get_float_value(inp_msg, err_msg, comparison_r)

        comparison_range = (0, 15)
        err_msg = f'Incorrect input. Should be float: 0-{comparison_range[1]}'
        for k in keys:
            input_msg = f'set {k}: '
            if k == 'blur_s':
                comparison_range = (0, 20)
                err_msg = f'Incorrect input. Should be integer: 0-{comparison_range[1]}'
                params[k] = self.get_input_value(input_msg, err_msg, comparison_range)
            else:
                params[k] = get_float_value(input_msg, err_msg, comparison_range)

        return params


if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_url_h = 'https://i.pinimg.com/originals/4c/d1/40/4cd140e29a0d499d8fc8fe7adf0924e0.jpg'
    # test_ui = UI('PILImageService', test_url)
    test_ui = UI(PILImageService(), test_url_h)
    test_ui1 = UI(SkiImageService(), test_url_h)
    # test_ui2 = UI('PILImageService', '.\\saved_img_pil\\test-1.jpg') # AttributeError: 'MissingSchema' object has no attribute 'save'

    # test_ui.run()
    test_ui.apply_filter()
    test_ui1.apply_filter()
