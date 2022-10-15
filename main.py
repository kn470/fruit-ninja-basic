import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
from fruits import Fruit
import threading
import random
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
background = cv2.imread("background.jpg")
background = cv2.resize(background, (1000,600))
#this section is for an individual apple - temporary - will be adjusted
apple = Fruit("apple", "apple.png", "apple.png", [500,525], [5,100])
w,h = apple.img.shape[0], apple.img.shape[1]
x,y = apple.pos[0], apple.pos[1]


apple_list = [apple]
score = 0
run = True
generate = True
generator_count = 0
def generate():
    global generator_count
    while True:
        time.sleep(1.5)
        rand_pos = [random.randrange(925), 525]
        rand_vel = [random.randrange(-10,10), 100]
        apple_list.append(Fruit(f"apple{generator_count}", "apple.png", "apple.png", rand_pos, rand_vel))
        generator_count += 1
        

def run():
    global score
    while True:
            
        success, img = cap.read()
        img = cv2.flip(img,1)
        img = cv2.resize(img, (1000,600))
        hands = detector.findHands(img, draw=False, flipType=False)
        img = cv2.addWeighted(img, 0.1, background, 0.95, 0)
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            index_finger = lmList[8][0:2]
            
            cv2.circle(img, index_finger, 10, (255,0,255), -1)
                
            for apple in apple_list:
                apple.throw()         
                if 0 < apple.pos[1] < 525 and 0 < apple.pos[0] < 925 and apple.touched(index_finger):
                    apple.explode(apple_list)
                    score += 1
            for apple in apple_list:
                if 0 < apple.pos[1] < 525 and 0 < apple.pos[0] < 925:   
                    img = cvzone.overlayPNG(img, apple.img, apple.pos)

            # elif apple.pos[0] < index_finger[0] < apple.pos[0] + 75 and apple.pos[1] < index_finger[1] < apple.pos[1] + 75:
            #     apple.explode(apple_list)    
            
            cv2.putText(img, str(score), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, )
            
            
                   
        cv2.imshow("frame",img)

        cv2.waitKey(1)

p1 = threading.Thread(target=generate)
p2 = threading.Thread(target=run)

p1.start()
p2.start()


cv2.destroyAllWindows()