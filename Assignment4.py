#!/usr/bin/python
#assignment 4 #

### import Python Modules ###
import threading
import time

## importing GPIO library
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

ledstate =False
print("Program is starting")
#set up GPIO using GPIO Board
GPIO.setmode(GPIO.BOARD)
#Green PushButton
GPIO.setup(22,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    #Red PushButton
GPIO.setup(12,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    #Yellow PushButton
GPIO.setup(13,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    #Blue PushButton
GPIO.setup(15,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    #Green LED
GPIO.setup(29,GPIO.OUT,initial =GPIO.LOW)
    #RED LED
GPIO.setup(31,GPIO.OUT,initial=GPIO.LOW)
    #Yellow LED
GPIO.setup(32,GPIO.OUT,initial=GPIO.LOW)
    #Blue LED
GPIO.setup(33,GPIO.OUT,initial=GPIO.LOW)

#assign button board number from bread board
BTN_G = 22
BTN_R = 12
BTN_Y = 13
BTN_B = 15
LED_G = 29
LED_R =31
LED_Y = 32
LED_B = 33

##dictionary
btn2led = {
    BTN_G : LED_G,
    BTN_R : LED_R,
    BTN_Y : LED_Y,
    BTN_B : LED_B
        }

#blink thread is assigned to function handle where threading is done.
def blink_thread():
    #ledstate is true when someone presses on button and false when nothing if false
    global ledstate#ledstate is declared false in the top
    #calculate time in this case run for 30 sec
    timeout = time.time() + 60*1
    #assign true
    ledstate = not ledstate
    #run blinking mode, check timer and when blue button is clicked Red and Green Led is turned off
    while True:
        test =0
        GPIO.output(29,True)
        time.sleep(0.5)
        GPIO.output(31,True)
        time.sleep(0.5)
        GPIO.output(29,False)
        time.sleep(0.5)
        GPIO.output(31,False)
        time.sleep(0.5)
        
        #timer condition
        if test == 1 or time.time() >timeout:
            break
        #When Blue button is clicked red and green is turned off and breaks out of loop
        elif GPIO.input(BTN_B) == ledstate:
            print("Blue Button is pressed, Red and Green Led turns off")
            break
        test = test -1
        
## Tell GPIO library to look out for an event on each pushbutton and pass handle ###
###function to be run for each pushbutton detection ###
def handle(pin):
    
    GPIO.output(btn2led[pin],not GPIO.input(pin))
    t = None
    if pin == BTN_Y:
        print("Yellow button is pressed please press green and red simulatenously")
    if pin == BTN_G or pin == BTN_R:
    ### when green and red pressed simulaneously, both red and green leds start blinking
        if GPIO.input(BTN_G) and GPIO.input(BTN_R):
            print("Start thread")
            t= threading.Thread(target=blink_thread)
            t.daemon=True
            t.start()

def loop():
    #Button Detect
    GPIO.add_event_detect(BTN_G,GPIO.BOTH,handle)
    GPIO.add_event_detect(BTN_R,GPIO.BOTH,handle)
    GPIO.add_event_detect(BTN_B,GPIO.BOTH,handle)
    GPIO.add_event_detect(BTN_Y,GPIO.BOTH,handle)


def destroy():
    #led is turned off
    GPIO.output(29,GPIO.LOW)
    GPIO.output(31,GPIO.LOW)
    GPIO.output(31,GPIO.LOW)
    GPIO.output(33,GPIO.LOW)
    GPIO.cleanup()
    
if __name__=='__main__':
   
    try:
        loop()
    except KeyboardInterrupt: #When ctrl+c is pressed, subprogram destroy() will be executed
        print("Error")
        destroy()
        

