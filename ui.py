import sys
from image_service import PILImageService, ImgFilters


class UI:
    def __init__(self, img_service: str, path: str) -> None:
        self.img_service = img_service
        self.path = path
        self.actions = [self.quit, self.show, self.save, self.resize, self.apply_filter]
        self.image_service = self.apply_image_service()
        self.image = self.load()

    def apply_image_service(self):
        if self.img_service == 'PILImageService':
            return PILImageService()
        
    def load(self):
        loaded_img = self.image_service.load(self.path)
        if loaded_img is None:
            print('Unsuccessful loading. Try another link ot path.') # выход или перезапуск?
    
    def run(self):
        for action in enumerate(self.actions):
            print(f'\t{action[0]}: {action[1].__name__}')
        print('\t--- ---')
        self.select_action()
        
    def select_action(self):
        act = input(f'Please insert number 0 - {len(self.actions)-1} to continue: ')
        try:
            if int(act) in range(len(self.actions)):
                self.actions[int(act)]()
        except ValueError:
            print(f'Try again. Enter number to select action.')
            self.select_action()

    def quit(self):
        print('\t -> quit')
        sys.exit()

    def save(self): 
        filepath = self.get_file_path()
        try: 
            self.image_service.save(self.image, filepath)
            print(f'\t saved: {filepath}')
        except OSError:
            print('Incorrect path. Image will be saved automatically')
            self.image_service.save(self.image, 'auto_saved')

    def show(self):
        self.image_service.show(self.image)

    def resize(self):
        resized = self.image_service.resize(self.image, self.get_new_picutre_size())
        self.image_service.show(resized)
        return resized

    def apply_filter(self):
        self.image_service.apply_filter(self.image, self.get_filter_type()) # тут нет параметров

    def get_file_path(self):
        return input('Please enter file name or path to save: ')

    def get_new_picutre_size(self):
        width = input("Enter a new width to resize the image: ")
        height= input("Enter a new height to resize the image: ")
        try:
            if 10 < int(height) < 1080 and 10 < int(width) < 1080:
                return (int(width), int(height))
            raise ValueError
        except ValueError:
            print('incorrect input, should be integer in range 10 - 1080 px. Try again')
            return self.get_new_picutre_size()
        
    def get_filter_type(self):
        print('\n > Availiable options:')
        for type in ImgFilters:
            print(f'\t> {type.name} - {type.value}')
        selected = input("Select filter (by name): ").lower().rstrip()
        if selected == 'blur':
            return ImgFilters.blur
        elif selected == 'sharpen':
            return ImgFilters.sharpen
        elif selected == 'smooth':
            return ImgFilters.smooth
        elif selected == 'filter':
            return ImgFilters.filter
        print("incorrect filter type, try again")
        return self.get_filter_type()

            

        




if __name__ == '__main__':
    test_url = 'https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png'
    test_ui = UI('PILImageService', test_url)
    test_ui2 = UI('PILImageService', '.\\saved_img_pil\\test-1.jpg') # AttributeError: 'MissingSchema' object has no attribute 'save'
    
    test_ui.run()
