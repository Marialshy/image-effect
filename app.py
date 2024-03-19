import ui

def app():
    '''
        - Скачивание изображения по ссылке
        - Ресайз картинки
        - Наложение фильтров
    '''
    def start_app():
        url = input('Enter the link to the picture to get started: ')
        interface = ui.MenuInterface(url)
        if not interface.check_if_image():
            return start_app()
        return interface
    
    menu_interface = start_app()
    
    while True:
        menu_interface.run()


if __name__ == '__main__':
    app()
    # https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png (ctrl + shft + v)
    # https://i.pinimg.com/564x/91/74/10/917410946ed00961e793dd28622dc84b.jpg

