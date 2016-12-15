import smbus
import RPi.GPIO as GPIO
from time import time, sleep, strftime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sec1 = 13
sec2 = 20
sec4 = 16
sec8 = 19
sec10 = 21
sec20 = 26
sec40 = 18

GPIO.setup(sec1, GPIO.OUT)
GPIO.setup(sec2, GPIO.OUT)
GPIO.setup(sec4, GPIO.OUT)
GPIO.setup(sec8, GPIO.OUT)
GPIO.setup(sec10, GPIO.OUT)
GPIO.setup(sec20, GPIO.OUT)
GPIO.setup(sec40, GPIO.OUT)


#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20 # Device address (A0-A2)
IODIRA = 0x00 # Pin dircetion register A
IODIRB = 0x01 # Pin Direction register B
GPIOA = 0x12 # Register for inputs A
GPIOB = 0x13 # Register for inputs B
OLATA = 0x14 # Register for outputs A
OLATB = 0x15 # Regitser for outputs B

# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRA,0x00)
bus.write_byte_data(DEVICE,IODIRB,0x00)

# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATA,0)
bus.write_byte_data(DEVICE,OLATB,0)

def ZeroAll():
    # Set all bits to zero
    bus.write_byte_data(DEVICE,OLATA,0)
    bus.write_byte_data(DEVICE,OLATB,0)

def secDigit1(status):
    if status == "on":
        GPIO.output(sec1, GPIO.HIGH)
    else:
        GPIO.output(sec1, GPIO.LOW)

def secDigit2(status):
    if status == "on":
        GPIO.output(sec2, GPIO.HIGH)
    else:
        GPIO.output(sec2, GPIO.LOW)

def secDigit4(status):
    if status == "on":
        GPIO.output(sec4, GPIO.HIGH)
    else:
        GPIO.output(sec4, GPIO.LOW)

def secDigit8(status):
    if status == "on":
        GPIO.output(sec8, GPIO.HIGH)
    else:
        GPIO.output(sec8, GPIO.LOW)

def secDigit10(status):
    if status == "on":
        GPIO.output(sec10, GPIO.HIGH)
    else:
        GPIO.output(sec10, GPIO.LOW)

def secDigit20(status):
    if status == "on":
        GPIO.output(sec20, GPIO.HIGH)
    else:
        GPIO.output(sec20, GPIO.LOW)

def secDigit40(status):
    if status == "on":
        GPIO.output(sec40, GPIO.HIGH)
    else:
        GPIO.output(sec40, GPIO.LOW)

def Seconds(x):
    first = int(x[:1])
    second = int(x[-1:])
 #   print str(first) + "" + str(second)

#Tens of Seconds
    if first == 1:
        secDigit10("on")
        secDigit20("off")
        secDigit40("off")
    
    if first == 2:
        secDigit20("on")
        secDigit10("off")
        secDigit40("off")

    if first == 3:
        secDigit10("on")
        secDigit20("on")
        secDigit40("off")

    if first == 4:
        secDigit40("on")
        secDigit10("off")
        secDigit20("off")
    
    if first == 5:
        secDigit40("on")
        secDigit10("on")
        secDigit20("off")

    if first == 0:
        secDigit10("off")
        secDigit20("off")
        secDigit40("off")
  
#Single Seconds
    if second == 1:
        secDigit1("on")
        sleep(1)
    else:
        secDigit1("off")

    if second == 2:
        secDigit2("on")
        sleep(1)
    else:
        secDigit2("off")

    if second == 3:
        secDigit1("on")
        secDigit2("on")
        sleep(1)
    else:
        secDigit1("off")
        secDigit2("off")

    if second == 4:
        secDigit4("on")
        sleep(1)
    else:
        secDigit4("off")

    if second == 5:
        secDigit4("on")
        secDigit1("on")
        sleep(1)
    else:
        secDigit4("off")
        secDigit1("off")
    
    if second == 6:
        secDigit4("on")
        secDigit2("on")
        sleep(1)
    else:
        secDigit4("off")
        secDigit2("on")

    if second == 7:
        secDigit4("on")
        secDigit2("on")
        secDigit1("on")
        sleep(1)
    else:
        secDigit4("off")
        secDigit2("off")
        secDigit1("off")

    if second == 8:
        secDigit8("on")
        sleep(1)
    else:
        secDigit8("off")

    if second == 9:
        secDigit8("on")
        secDigit1("on")
        sleep(1)
    else:
        secDigit8("off")
        secDigit1("off")
        
    if second == 0:
        secDigit1("off")
        secDigit2("off")
        secDigit4("off")
        secDigit8("off")
        sleep(1)

def Minutes(x):
    first = int(x[:1])
    second = int(x[-1:])
    val = (second + (int(first)*16))
    bus.write_byte_data(DEVICE,GPIOB, val)

def Hours(x):
    first = int(x[:1])
    second = int(x[-1:])
    val = (second + (int(first)*16))
    bus.write_byte_data(DEVICE,GPIOA, val)

global displayedMin 
displayedMin = 0

global displayedHour
displayedHour = 0

while True:
    global varSeconds   
    varSeconds = strftime("%S")    
    Seconds(str(varSeconds))
    Hours(strftime("%H"))
    Minutes(strftime("%M"))

    if displayedMin < strftime("%M"):
        ZeroAll() 
        Minutes(strftime("%M"))
        displayedMin = strftime("%M")
    
    if displayedHour < strftime("%H"):
        ZeroAll() 
        Hours(strftime("%H"))
        displayedHour = strftime("%H")

    print str(strftime("%H") + ":" + strftime("%M") + ":" + strftime("%S"))
    print ("Displayed Hour: " + displayedHour)
    print ("Displayed Minute: " + displayedMin)
