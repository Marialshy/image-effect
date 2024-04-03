import ui
from image_service import PILImageService, SkiImageService


def create_app():
    url = input('Enter the link to the picture to get started: ')
    image_service = get_service()
    try:
        interface = ui.UI(image_service, url)
    except AttributeError:
        print('Unsuccessful loading. Try another link or path')
        return create_app()
    return interface


def get_service():
    service = input('Choose the service type - pillow (enter [pil]) or skimage (enter [ski]): ').lower().rstrip()
    if service == 'pil':
        return PILImageService()
    elif service == 'ski':
        return SkiImageService()

    return get_service()
    

def app():
    '''
        Allows you to perform the following actions with the image:
        - download (link/path)
        - view
        - modify: filters, resize
        - save
    '''
    interface = create_app()
    while True:
        interface.run()


if __name__ == '__main__':
    app()
    # https://i.pinimg.com/originals/f6/db/2d/f6db2d2968625adf2774de966cf2951b.png (ctrl + shft + v)
    # https://i.pinimg.com/564x/91/74/10/917410946ed00961e793dd28622dc84b.jpg
    # https://i.pinimg.com/originals/4c/d1/40/4cd140e29a0d499d8fc8fe7adf0924e0.jpg
