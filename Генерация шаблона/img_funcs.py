from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import cv2


def paste_image(img_name, back_img, front_img, x_offset, y_offset):
    # накладывает два изображения с отступом
    back_img = cv2.cvtColor(back_img, cv2.COLOR_RGB2RGBA)
    front_img = cv2.cvtColor(front_img, cv2.COLOR_RGB2RGBA)
    y1, y2 = y_offset, y_offset + front_img.shape[0]
    x1, x2 = x_offset, x_offset + front_img.shape[1]
    try:
        alpha_s = front_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            back_img[y1:y2, x1:x2, c] = (alpha_s * front_img[:, :, c] +
                                    alpha_l * back_img[y1:y2, x1:x2, c])
    except ValueError:
        print(f'---Не удалось вставить изображение "{img_name}"')
    return back_img

def rotate_resize_brightness(file_path, deg, img_size, size=1, brightness=1):
    # поворот изображение через PIL - сохранение повернутого изображение
    # чтение повернутого изображения через cv2
    # resize изображения по размеру шаблона
    file_name = file_path.split('/')[1][:-4]
    img = Image.open(file_path)
    if deg!=0:
        img = img.rotate(deg)
    if brightness!=1:
        img = ImageEnhance.Brightness(img).enhance(brightness)
        
    file_name = f"temp_images/{file_name}.png"
    img.save(file_name,"PNG")
    print(f'Изображение {file_name} сохранено')

    img = cv2.imread(file_name, -1)
    if size!=1:
        img_size = (int(img_size[0]*size), int(img_size[0]*size))
        img = cv2.resize(img, img_size)
    
    # cv2.imwrite(f'resize.png', img)
    return img


def get_text_img(file_name, text, font_size, font_path, color, position, align):
    # сохраняет изображние с текстом по заданным параметрам
    file_name = f"temp_images/{file_name}.png"
    font = ImageFont.truetype(font_path, font_size)
    text_mask = font.getmask(text, "L")
    break_num = text.count('\n')+1
    img = Image.new("RGBA", (text_mask.size[0], text_mask.size[1]*break_num*2))
    draw = ImageDraw.Draw(img)
    draw.text((0,0), text, font = font, align = align, fill = color) 
    img.save(file_name,"PNG")

    img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    if color == (255, 255, 255, 255):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x, y, w, h = cv2.boundingRect(cv2.findNonZero(gray))
        img = img[y:y+h, x:x+w]
        try:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
            cv2.imwrite(file_name, img)
        except:
            pass
    print(f'Изображение {file_name}.png сохранено')
    return img
