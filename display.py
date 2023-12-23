import time
import Adafruit_Python_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = 24

disp =Adafruit_Python_SSD1306.SSD_128_64(rst = RST)

disp.begin()
width = disp.width
height = disp.height
while True:
    disp.clear()
    disp.display()

    image = Image.open('raspberry.png').resize((width,height), Image.ANTIALIAS).convert('1')
    disp.image(image)
    disp.display()
    time.sleep(0.4)
    top=10
    fonr = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf',13)
    for i in range(50,0,-10):
        image = Image.new('1',(width,height))
        draw = ImageDraw.Draw(image)

        draw.text((i,top), 'Don',font = fonr ,fill=255)



        disp.image(image)
        disp.display()
        time.sleep(0.3)