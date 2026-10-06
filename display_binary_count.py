import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

SDI = 24
RCLK = 23
SRCLK = 18

placeLed = (5, 6, 13, 19, 26)
placePin = (10, 22, 27, 17)
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)

counter = 0

y=int(input('Nº 1 - 31?: '))
x=[[0,0,0,0,1],[0,0,0,1,0],[0,0,0,1,1],[0,0,1,0,0],[0,0,1,0,1],[0,0,1,1,0],[0,0,1,1,1],[0,1,0,0,0],[0,1,0,0,1],[0,1,0,1,0],[0,1,0,1,1],[0,1,1,0,0],[0,1,1,0,1],[0,1,1,1,0],[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,1],[1,0,0,1,0],[1,0,0,1,1],[1,0,1,0,0],[1,0,1,0,1],[1,0,1,1,0],[1,0,1,1,1],[1,1,0,0,0],[1,1,0,0,1],[1,1,0,1,0],[1,1,0,1,1],[1,1,1,0,0],[1,1,1,0,1],[1,1,1,1,0],[1,1,1,1,1]]
while y>=32 or y<=0:
	y=int(input('Nº 1 - 31?: '))


def clearDisplay():
    for i in range(8):
        GPIO.output(SDI, 1)
        GPIO.output(SRCLK, GPIO.HIGH)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def hc595_shift(data):
    for i in range(8):
        GPIO.output(SDI, 0x80 & (data << i))
        GPIO.output(SRCLK, GPIO.HIGH)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def pickDigit(digit):
    for i in placePin:
        GPIO.output(i,GPIO.LOW)
    GPIO.output(placePin[digit], GPIO.HIGH)


def Binary_counter():
    global counter, y
    for i in range(0,y,1):
        loop(counter)
        GPIO.output(5,x[i][0])
        GPIO.output(6,x[i][1])
        GPIO.output(13,x[i][2])
        GPIO.output(19,x[i][3])
        GPIO.output(26,x[i][4])
        time.sleep(3/2)
        print("%d" % counter)
        counter += 1

def loop(count):
    if count < 10:
        clearDisplay()
        pickDigit(0)
        hc595_shift(number[count % 10])
    elif count == 10:
        clearDisplay()
        pickDigit(1)
        hc595_shift(number[count % 100//10])
        pickDigit(0)
        hc595_shift(number[count % 10])


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    for i in placeLed:
        GPIO.setup(i,GPIO.OUT)
    for i in placePin:
        GPIO.setup(i, GPIO.OUT)
    

def destroy():   # When "Ctrl+C" is pressed, the function is executed.
    GPIO.cleanup()

if __name__ == '__main__':  # Program starting from here
    setup()
    try:
        Binary_counter()
    except KeyboardInterrupt:
        destroy()
        
