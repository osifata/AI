import cv2
import datetime

from img_funcs import get_text_img, paste_image, rotate_resize_brightness
from text_funcs import add_line_break, phone_format

def template_from_images(images, img_size):
    # возвращает шаблон, собранный из изображений
    for img in images.keys():
        locals()[img] = cv2.imread(images[img]['path_to_img'], -1)

        deg = images[img]['rotation']
        brightness = images[img]['brightness']
        if deg!=0 or brightness!=1:
            locals()[img] = rotate_resize_brightness(images[img]['path_to_img'], deg, img_size, images[img]['size'], brightness)
        blur = images[img]['blur']
        if blur!=(0,0):
            locals()[img] = cv2.blur(locals()[img], blur)
            
        img_name = img
        if img == list(images.keys())[1]: 
            # накладываем первое изображение на второе 
            image = paste_image(img_name, locals()[list(images.keys())[0]], locals()[img], *images[img]['pos'])
        elif img != list(images.keys())[0]:
            # все остальные изображения, накладываем их друг на друга по-очереди
            image = paste_image(img_name, image, locals()[img], *images[img]['pos'])
    return image

def paste_text_images(image, texts):
    # возвращает изображение с текстом
    texts_layers = []
    for text in texts.keys():
        current_text = text
        current_text_d = texts[current_text]
        text_img = get_text_img(current_text, 
                                current_text_d['text'], current_text_d['font_size'], 
                                current_text_d['font'], current_text_d['color'], 
                                current_text_d['pos'], current_text_d['align'])
        # current_text_img = cv2.imread(f"temp_images/{current_text}.png", -1)
        image = paste_image(current_text_d['text'][:10], image, text_img, *current_text_d['pos'])
    return image

def get_position(
                # horizontal, vertical, 
                steps_x, steps_y, 
                horizontal_size=100, vertical_size=50, 
                offset_x = 0, offset_y = 0):
    margin_x, margin_y = 10, 10
    grid_step_x, grid_step_y = 25, 50 # размер клеток сетки, чтобы выравнивать элементы 
    # if horizontal == 'left':
    x = steps_x*grid_step_x + margin_x + offset_x
    # else: # left
    #     x = img_size[0] - steps_x*grid_step_x - margin_x  - horizontal_size + offset_x
    #     print(x)

    # if vertical == 'top':
    y = steps_y*grid_step_y + margin_y + offset_y
    # else: # bottom
    #     y = img_size[1] - steps_y*grid_step_y - margin_y  - vertical_size + offset_y
    # print(x, y)
    return (x, y)

# --------------------------------------------------------
def create_portrait_template_1(back_img_path, obj_img_path, img_size, fonts, colors):
    texts = {
        'title_text':{
            'text':add_line_break("ИГРОВАЯ МЫШЬ", 7), # число символов в одной строке до переноса
            # 'pos':(get_position('left', 'top', 1, 1)), # отсчет от верхнего левого края, (1,1) начальные коожинаты сетки
            'pos':(get_position(1, 1)),
            'font': fonts['helvetica'],
            'font_size':56,
            'color': colors['white'],
            'align': 'left'
        }, 
        'subtitle_text':{
            'text':add_line_break("6 кнопок полностью программируемые", 20),
            'pos':(get_position(1, 5)),
            'font': fonts['helvetica'],
            'font_size':36,
            'color': colors['white'],
            'align': 'left'
        }, 
        'address_text':{
            'text':add_line_break("ул. Снежная д.3", 20),
            # 'pos':(get_position('left', 'top', 1, 19)), # right и bottom пока не работают, убрала эти поля полностю
            'pos':(get_position(1, 19)),
            'font': fonts['helvetica'],
            'font_size':26,
            'color': colors['black'],
            'align': 'right'
        }, 
        'phone_text':{
            'text':phone_format('88005353535'),
            'pos':(get_position(10, 18)),
            'font': fonts['helvetica'],
            'font_size':56,
            'color': colors['black'],
            'align': 'right'
        }, 
        'button_text':{
            'text':'Узнать больше',
            'pos':(get_position(1, 16, offset_x=20, offset_y=20)),
            'font': fonts['helvetica'],
            'font_size':40,
            'color': colors['black'],
            'align': 'left'
        }
    }


    images = {
        'back_img':{
            'path_to_img': f'{back_img_path}.png',
            'size': 1, # коэффициет (1 - не менять размер)
            'pos':(0, 0), # px
            'rotation': 0, # градусов
            'blur': (10, 10), # размер блюра
            'brightness': 0.5 # яркость, 1 обычная
        },
        'white_diagonal_img':{
            'path_to_img': "template_elements/portrait_diagonal.png",
            'size': 1,
            'pos':(0, 0),
            'rotation': 0, 
            'blur': (0, 0),
            'brightness': 1
        },
        'white_button_img':{
            'path_to_img': "template_elements/white_button.png",
            'size': 1,
            'pos':(get_position(1, 16)),
            'rotation': 0, 
            'blur': (0, 0),
            'brightness': 1
        },
        'obj_shadow_img':{ # тень для объекта - то же изображение, но с блюром
            'path_to_img': f'{obj_img_path}.png',
            'size': 0.8,
            'pos':(get_position(2, 5, offset_x=5, offset_y=5)), # координаты тени должны совпадать с объектом + отступ
            'rotation': -45, 
            'blur': (70, 70),
            'brightness': 1
        },
        'obj_img':{
            'path_to_img': f'{obj_img_path}.png',
            'size': 0.8,
            'pos':(get_position(2, 5)),
            'rotation': -45, 
            'blur': (0, 0),
            'brightness': 1
        }
    }

    final_template = template_from_images(images, img_size)
    final_template = paste_text_images(final_template, texts)

    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')
    # uniq_filename = 'result'
    cv2.imwrite(f'template_results/{uniq_filename}.png', final_template)
    cv2.imwrite(f'template_results/last_result.png', final_template)
    print(f'---ШАБЛОН {img_size} СОХРАНЕН')


# --------------------------------------------------------
def create_square_template_1(back_img_path, obj_img_path, img_size, fonts, colors):
    texts = {
        'title_text':{
            'text':add_line_break("ИГРОВАЯ МЫШЬ", 7), # число символов в одной строке до переноса
            # 'pos':(get_position('left', 'top', 1, 1)), # отсчет от верхнего левого края, (1,1) начальные коожинаты сетки
            'pos':(get_position(0, 0, offset_x=20, offset_y=20)),
            'font': fonts['helvetica'],
            'font_size':56,
            'color': colors['black'],
            'align': 'left'
        }, 
        'subtitle_text':{
            'text':add_line_break("6 кнопок полностью программируемые", 20),
            'pos':(get_position(7, 2)),
            'font': fonts['helvetica'],
            'font_size':36,
            'color': colors['black'],
            'align': 'left'
        }, 
        'address_text':{
            'text':add_line_break("ул. Снежная д.3", 20),
            # 'pos':(get_position('left', 'top', 1, 19)), # right и bottom пока не работают, убрала эти поля полностю
            'pos':(get_position(6, 8)),
            'font': fonts['helvetica'],
            'font_size':26,
            'color': colors['white'],
            'align': 'right'
        }, 
        'phone_text':{
            'text':phone_format('88005353535'),
            'pos':(get_position(7, 18)),
            'font': fonts['helvetica'],
            'font_size':56,
            'color': colors['black'],
            'align': 'right'
        }, 
        'button_text':{
            'text':'Узнать больше',
            'pos':(get_position(1, 18)), #, offset_x=20, offset_y=20)),
            'font': fonts['helvetica'],
            'font_size':40,
            'color': colors['black'],
            'align': 'left'
        }
    }


    images = {
        'back_img':{
            'path_to_img': f'{back_img_path}.png',
            'size': 1, # коэффициет (1 - не менять размер)
            'pos':(0, 0), # px
            'rotation': 0, # градусов
            'blur': (10, 10), # размер блюра
            'brightness': 0.5 # яркость, 1 обычная
        },
        'white_back_img':{
            'path_to_img': "template_elements/square_circle.png",
            'size': 1,
            'pos':(0, 0),
            'rotation': 0, 
            'blur': (0, 0),
            'brightness': 1
        },
        'white_button_img':{
            'path_to_img': "template_elements/white_button.png",
            'size': 1,
            'pos':(get_position(1, 10)),
            'rotation': 0, 
            'blur': (0, 0),
            'brightness': 1
        },
        'obj_shadow_img':{ # тень для объекта - то же изображение, но с блюром
            'path_to_img': f'{obj_img_path}.png',
            'size': 0.6,
            'pos':(get_position(3, 4, offset_x=5, offset_y=5)), # координаты тени должны совпадать с объектом + отступ
            'rotation': -45, 
            'blur': (70, 70),
            'brightness': 1
        },
        'obj_img':{
            'path_to_img': f'{obj_img_path}.png',
            'size': 0.6,
            'pos':(get_position(3, 4)),
            'rotation': -45, 
            'blur': (0, 0),
            'brightness': 1
        }
    }

    final_template = template_from_images(images, img_size)
    final_template = paste_text_images(final_template, texts)

    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')
    # uniq_filename = 'result'
    cv2.imwrite(f'template_results/{uniq_filename}.png', final_template)
    cv2.imwrite(f'template_results/last_result.png', final_template)
    print(f'---ШАБЛОН {img_size} СОХРАНЕН')


# --------------------------------------------------------
def create_square_template_2(back_img_path, obj_img_path, img_size, fonts, colors):
    pass


# --------------------------------------------------------
def create_landscape_template_1(back_img_path, obj_img_path, img_size, fonts, colors):
    texts = {
        'title_text':{
            'text':add_line_break("ИГРОВАЯ МЫШЬ", 7), # число символов в одной строке до переноса
            # 'pos':(get_position('left', 'top', 1, 1)), # отсчет от верхнего левого края, (1,1) начальные коожинаты сетки
            'pos':(get_position(0, 0, offset_x=20, offset_y=20)),
            'font': fonts['helvetica'],
            'font_size':56,
            'color': colors['white'],
            'align': 'left'
        }, 
        'subtitle_text':{
            'text':add_line_break("6 кнопок полностью программируемые", 20),
            'pos':(get_position(7, 2)),
            'font': fonts['helvetica'],
            'font_size':36,
            'color': colors['white'],
            'align': 'left'
        }, 
        'address_text':{
            'text':add_line_break("ул. Снежная д.3", 20),
            # 'pos':(get_position('left', 'top', 1, 19)), # right и bottom пока не работают, убрала эти поля полностю
            'pos':(get_position(6, 8)),
            'font': fonts['helvetica'],
            'font_size':26,
            'color': colors['white'],
            'align': 'right'
        }, 
        'phone_text':{
            'text':phone_format('88005353535'),
            'pos':(get_position(6, 14)),
            'font': fonts['helvetica'],
            'font_size':56,
            'color': colors['white'],
            'align': 'right'
        }, 
        'button_text':{
            'text':'Узнать больше',
            'pos':(get_position(1,11)), #, offset_x=20, offset_y=20)),
            'font': fonts['helvetica'],
            'font_size':40,
            'color': colors['black'],
            'align': 'left'
        }
    }


    images = {
        'back_img':{
            'path_to_img': f'{back_img_path}.png',
            'size': 1, # коэффициет (1 - не менять размер)
            'pos':(0, 0), # px
            'rotation': 0, # градусов
            'blur': (10, 10), # размер блюра
            'brightness': 0.5 # яркость, 1 обычная
        },
        'white_back_img':{
            'path_to_img': "template_elements/landscape_side.png",
            'size': 1,
            'pos':(0, 0),
            'rotation': 0, 
            'blur': (0, 0),
            'brightness': 1
        },
        'white_button_img':{
            'path_to_img': "template_elements/white_button.png",
            'size': 1,
            'pos':(get_position(1, 10)),
            'rotation': 0, 
            'blur': (0, 0),
            'brightness': 1
        },
        'obj_shadow_img':{ # тень для объекта - то же изображение, но с блюром
            'path_to_img': f'{obj_img_path}.png',
            'size': 0.4,
            'pos':(get_position(5, 4, offset_x=5, offset_y=5)), # координаты тени должны совпадать с объектом + отступ
            'rotation': -45, 
            'blur': (70, 70),
            'brightness': 1
        },
        'obj_img':{
            'path_to_img': f'{obj_img_path}.png',
            'size': 0.4,
            'pos':(get_position(5, 4)),
            'rotation': -45, 
            'blur': (0, 0),
            'brightness': 1
        }
    }

    final_template = template_from_images(images, img_size)
    final_template = paste_text_images(final_template, texts)

    uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')
    # uniq_filename = 'result'
    cv2.imwrite(f'template_results/{uniq_filename}.png', final_template)
    cv2.imwrite(f'template_results/last_result.png', final_template)
    print(f'---ШАБЛОН {img_size} СОХРАНЕН')
