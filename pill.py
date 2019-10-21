from PIL import Image, ImageDraw
import random

class CirclesImg:
    def __init__(self, width, height):
        self.img = Image.new('RGB', (width, height), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)

    def create_image_with_ball(self, ball_x, ball_y, ball_size, color):
        self.draw.ellipse((ball_x, ball_y, ball_x + ball_size, ball_y + ball_size), fill=color)

    def image(self):
        return self.img

maxx = 400
maxy = 400
objs = list()
for i in range(10):
    objs.append((random.randint(1,maxx), random.randint(1, maxy)))

def shift(x,y):
    if random.randint(0,1)==1:
        x = x+random.randint(0,5)
    else:
        x = x-random.randint(0,5)
    if random.randint(0,1)==1:
        y = y+random.randint(0,5)
    else:
        y = y-random.randint(0,5)
    return x,y

frames = []
for i in range(100):
    img = CirclesImg(maxx, maxy)
    for o in objs:
        img.create_image_with_ball(*shift(o[0], o[1]), 10, 'red')
    frame = img.image()
    frames.append(frame)

 
frames[0].save('moving_ball.gif', format='GIF', append_images=frames[1:], save_all=True, duration=10)
