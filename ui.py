import sys
from my_image import MyImage


class MenuInterface:
    def __init__(self, url: str) -> None:
        self.image = MyImage(url)
        self.actions = [self.quit, self.save_image, self.resize_image_by_height, self.apply_filter]

    def run(self):
        if self.check_if_image():
            self.show_menu()
            self.select_action()
        else:
            print('No image was detected. Try another link')

    def check_if_image(self):
        return self.image.downloaded_image is not None

    def show_menu(self):
        for action in enumerate(self.actions):
            print(f'\t{action[0]}: {action[1].__name__}')
        print('\t--- ---')

    def select_action(self):
        act = input(f'Please insert number 0 - {len(self.actions)-1} to continue: ')
        try:
            if int(act) in range(len(self.actions)):
                self.actions[int(act)]()
        except ValueError:
            print(f'Try again.')
            self.select_action()

    def quit(self):
        print('\t -> quit')
        sys.exit()

    def save_image(self):
        name = self.create_file_name()
        fp = self.image.save(name)  # to jpg (bool)
        print(f'saved: {fp}')

    def resize_image_by_height(self):
        new_height = self.get_new_picutre_height()
        name = self.create_file_name()
        self.image.resize_by_height(new_height)
        self.image.save(name, 'resized', True)  # автосохранение в jpg

    def apply_filter(self):
        return
        self.image.apply_filter()

    def create_file_name(self):
        return input('Please enter file name: ')  # тут нет проверки на спецсимволы

    def get_new_picutre_height(self):
        height = input("Enter a new height to resize the image: ")
        try:
            if 10 < int(height) < 1080:
                return int(height)
            raise ValueError
        except ValueError:
            print('incorrect height, should be integer in range 10 - 1080 px. Try again')
            return self.get_new_picutre_height()


if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_ui = MenuInterface(test_url)
    test_ui.run()
