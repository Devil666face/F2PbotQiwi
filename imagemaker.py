import qrcode, pytz, config, os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime

from modify import add_null

def make_qrcode_image(text):
    image = qrcode.make(text)
    image_name = f'{datetime.now()}.png'
    image.save(image_name)
    return image_name

def get_font(bold,size):
    if bold:
        font = ImageFont.truetype('fonts/arial_bold.ttf', size)
    else:
        font = ImageFont.truetype('fonts/arial.ttf', size)
    return font

def get_time_now():
    tz = pytz.timezone('Europe/Moscow')
    cur_time = datetime.now(tz)
    return f'{add_null(cur_time.hour)}:{add_null(cur_time.minute)}'

def get_date_now():
    tz = pytz.timezone('Europe/Moscow')
    cur_time = datetime.now(tz)
    return f'{add_null(cur_time.day)}.{add_null(cur_time.month)}.{cur_time.year}'

def create_image(bus,bus_number,start_station,stop_station,url_qr):
    path_to_qr = make_qrcode_image(url_qr)
    img = Image.open("clear.PNG")
    img_qr = Image.open(path_to_qr)
    img_qr = img_qr.resize((870,870),Image.ANTIALIAS)

    img.paste(img_qr,(0,407))

    draw = ImageDraw.Draw(img)
    draw.text((75, 41),get_time_now(),(0,0,0),font=get_font(True,48))
    draw.text((43, 1272),f'{get_date_now()} {get_time_now()}',(0,0,0),font=get_font(False,52))
    draw.text((336, 1356),str(bus),(0,0,0),font=get_font(True,60))
    draw.text((122, 1465),start_station,(0,0,0),font=get_font(False,55))
    draw.text((122, 1670),stop_station,(0,0,0),font=get_font(False,55))
    draw.text((73, 1922),bus_number,(0,0,0),font=get_font(True,50))
    draw.text((333, 1803),config.PRICE,(0,0,0),font=get_font(False,50))

    path_to_image = f'{datetime.now()}.png'
    img.save(path_to_image)

    os.remove(path_to_qr)

    return path_to_image