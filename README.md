## Проект Image Service.
В качестве знакомства с функционалом библиотек обработки изображений (pillow, skimage) в проекте реализованы несколько методов.

Приложение взаимодействует с пользователем через консоль.

### Начало работы.
Для начала работы необходимо проверить наличие установленных пакетов (requirments.txt) и запустить app.py.

После запуска приложения пользователю будет предложено ввести ссылку на изображение, выбрать способ работы с ним:

- 'pil'

    методы реализованы на основе стандартных методов класса Image, пакета pillow. Изображение - объект класса PIL.JpegImagePlugin.JpegImageFile (после загрузки изображения) или PIL.Image.Image (после преобразования исходного изображения).

    [pillow documentation](https://pillow.readthedocs.io/en/stable/handbook/overview.html)


- 'ski'

    методы реализованы на основе стандартных методов пакета scikit-image (skimage). Изображение - объект класса numpy.ndarray  
    [skimage documentation](https://scikit-image.org/docs/stable/user_guide/getting_started.html)

### Основное меню
После выбранного способа обработки изображения, в консоль выводится основное меню:

0. выход
1. вывод изображение на экран
2. сохранение изображение

    (если вместо пути получено только имя файла (в т.ч. и без расширения), изображение сохраняется в папку проекта -> saved_img);
3. изменение размера
4. применение фильтра (у нескольких фильтров доступна ручная настройка параметров):

    - blur - опционально можно задать радиус размытия. Параметры:
        - pil: float(range(0, 15, 0.01)), 
        - ski: int(range(0, 20))
    - sharpen - на основе техники [unsharp masking](https://en.wikipedia.org/wiki/Unsharp_masking#:~:text=Unsharp%20masking%20(USM)%20is%20an,mask%20of%20the%20original%20image.). Параметры:
        - pil: 
        
        sharpen_p_r - blur radius: float(range(0, 15, 0.01)), 

        sharpen_p_p - unsharp strength: float(range(0, 15, 0.01));

        - ski:

        sharpen_s_r - blur scalar: float(range(0, 15, 0.01)), 

        sharpen_s_a - The details will be amplified with this factor: float(range(0, 15, 0.01));

    - smooth - сглаживание, параметры не принимает
    - customer filter - фильтр, заданный автором проекта, параметры не принимает
        - pil: фильтр ImageFilter.ModeFilter (Picks the most frequent pixel value in a box with the given size. Pixel values that occur only once or twice are ignored. Kernel size = 6);

        - ski: фильтр улучшает экспозицию - ski.exposure.equalize_adapthist, также используется ski.filters.butterworth


    После модификации (размера или фильтра) изображение заменяется на модифицированное и исходное становится недоступным.

    Автоматического сохранения не предусмотрено.



    
    
