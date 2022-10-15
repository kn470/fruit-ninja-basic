import cv2
import time
import math


class Fruit:

    def __init__(self, name, img, cut_img, pos, vel):
        self.name = name
        img_1 = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        self.img = cv2.resize(img_1, (75,75))
        self.cut_img = cv2.imread(cut_img)
        self.pos = pos
        self.vel = vel

    def touched(self, index_point):
        if self.pos[0] < index_point[0] < self.pos[0] + 75 and self.pos[1] < index_point[1] < self.pos[1] + 75:
            return True
        else:
            return False

    def explode(self, ex_list):
        ex_list.remove(self)
        
    def throw(self):
        #time.sleep(0.00000000001)
        self.vel[1] -= 5
        self.pos[0] += self.vel[0]
        self.pos[1] -= math.floor(self.vel[1]*0.5)

    def rotate(self):
        pass



    