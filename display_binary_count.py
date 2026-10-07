import RPi.GPIO as GPIO
from time import sleep
import threading

GPIO.setmode(GPIO.BCM)

#74HC595 shift register pins
SDI = 24   #Data
RCLK = 23  #Storage clock 
SRCLK = 18 #Deslocation clock 

placeLed = (5, 6, 13, 19, 26)
placePin = (10, 22, 27, 17)  #7-Segment-Display pins

# 8 bit     0     1     2    3               ......              9
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)

#Counter control parameters
counter = 1
stop_timer = False
timer_ref = None

# 5 LEDs binary representation of a count from 1-31 
x = [[0,0,0,0,1],[0,0,0,1,0],[0,0,0,1,1],[0,0,1,0,0],[0,0,1,0,1],
     [0,0,1,1,0],[0,0,1,1,1],[0,1,0,0,0],[0,1,0,0,1],[0,1,0,1,0],
     [0,1,0,1,1],[0,1,1,0,0],[0,1,1,0,1],[0,1,1,1,0],[0,1,1,1,1],
     [1,0,0,0,0],[1,0,0,0,1],[1,0,0,1,0],[1,0,0,1,1],[1,0,1,0,0],
     [1,0,1,0,1],[1,0,1,1,0],[1,0,1,1,1],[1,1,0,0,0],[1,1,0,0,1],
     [1,1,0,1,0],[1,1,0,1,1],[1,1,1,0,0],[1,1,1,0,1],[1,1,1,1,0],
     [1,1,1,1,1]]

y = int(input('Nº 1 - 31?: '))
while y >= 32 or y <= 0:
    y = int(input('Nº 1 - 31?: '))


def clear_shift_register():
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
        GPIO.output(i, GPIO.LOW)
    GPIO.output(placePin[digit], GPIO.HIGH)


def display_value(count):
    if count < 10:
        clear_shift_register()
        hc595_shift(number[count % 10])   # defines the data(number) in the shift register 
        pickDigit(0)                      # presentes only one digit in the display
    elif count < 32: # According to the max value that can be presente in banary on the LEDs
        digit_units = count % 10
        digit_tens  = count // 10

        # Unit digits
        clear_shift_register()
        hc595_shift(number[digit_units])
        pickDigit(0)
        sleep(0.005)

        # Digit of tens
        clear_shift_register()
        hc595_shift(number[digit_tens])
        pickDigit(1)
        sleep(0.005)


def refresh_display():
    """Thread loop: multiplexa o display a ~100 Hz"""
    global stop_timer
    while not stop_timer:
        display_value(counter-1)
        sleep(0.005)  # 5 ms for ciclo → ~100 Hz


def Binary_counter():
    global counter, timer_ref, stop_timer

    # Inicia a thread de multiplexagem
    stop_timer = False
    refresh_thread = threading.Thread(target=refresh_display, daemon=True)
    refresh_thread.start()

    for i in range(0, y, 1):
        # Atualiza LEDs binários
        GPIO.output(5, x[i][0])
        GPIO.output(6, x[i][1])
        GPIO.output(13, x[i][2])
        GPIO.output(19, x[i][3])
        GPIO.output(26, x[i][4])

        print("%d" % counter)
        counter += 1
        sleep(1.5)

    # Para a thread de multiplexagem
    stop_timer = True
    refresh_thread.join()


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    for i in placeLed:
        GPIO.setup(i, GPIO.OUT)
    for i in placePin:
        GPIO.setup(i, GPIO.OUT)


def destroy():
    global stop_timer
    stop_timer = True          
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        Binary_counter()
    except KeyboardInterrupt:
        destroy()