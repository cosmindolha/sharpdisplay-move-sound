import board
import busio
import storage
import sdcardio

import time
import busio
import board
import displayio
import framebufferio
import sharpdisplay
# import terminalio
from terminalio import FONT
# import adafruit_display_text.label
from adafruit_display_text.label import Label
import asyncio
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
# import random


# import simpleio


buzzer = board.GP8



TONE_FREQ = [262, 392, 494, 440, 494, 440, 392, 440, 494, 440, 494, 262, 494, 262, 392, 440, 262, 494, 262, 494, 262, 494, 440, 262, 494, 262, 349, 392, 262, 349, 294, 262, 392, 294, 262, 440, 392, 349, 262, 392, 262, 392, 494, 262, 494, 262, 494, 262, 392, 494, 440, 349, 494, 392, 494, 440, 392, 494, 262, 494, 262, 392, 349, 262, 494, 262, 494, 262, 494, 262, 494, 440, 262, 494, 262, 494, 262, 392, 262]
             


# Set up SPI0 and CS pin according to the schematic
spi = busio.SPI(board.GP18, board.GP19, board.GP16)  # SCK, MOSI, MISO
cs = board.GP17  # CS

# Initialize the SD card
sd = sdcardio.SDCard(spi, cs)

# Mount the filesystem
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")

# List the contents of the SD card
import os
print("Files on my SD card:")

print(os.listdir("/sd"))

# Writing to a file on the SD card
# with open("/sd/test.txt", "w") as file:
#     file.write("Hello, SD card!")

# Reading from a file on the SD card
# with open("/sd/test.txt", "r") as file:
#     content = file.read()
#     print(content)

# on spi1
# csPin = board.GP13

import digitalio

ckPin = board.GP10
mosiPin = board.GP11

csPin = board.GP13


displayio.release_displays()
      

bus = spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)




group = displayio.Group()




framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, csPin, 400, 240, baudrate=8000000, jdi_display=False)
print("Framebuffer initialized")

display = framebufferio.FramebufferDisplay(framebuffer, auto_refresh = True)

print("Display initialized")

whiteBmp = displayio.Bitmap(400, 240, 1)
whitePalette = displayio.Palette(1)
whitePalette[0] = 0xFFFFFF
whiteSprite = displayio.TileGrid(whiteBmp, pixel_shader=whitePalette, x=0, y=0)


display.rotation = 180



text_area = Label(font=FONT, text="Connecting..", x=5, y=55, scale=3, line_spacing=1.2)

text_area.color = 0x000000

group.append(whiteSprite)
# group.append(text_area)

# create a circle

myCircle = Circle(100, 120, 10, fill=0x00000)

group.append(myCircle)

display.root_group = group



# display.root_group.append(text_area)

text_area.text = "Let's map buttons"

# - ------------------ SEETUP ----- on rspberry pico

# GP0 is action button up
# GP1 is action button down
# GP2 - arrow right
# GP3 arrow down
# GP4 arrow left
# GP5 arrow up

# global buttons states

buttonsState = {
    "button_ActionUp_IsPressed": False,
    "button_ActionDown_IsPressed": False,
    "button_ArrowRight_IsPressed": False,
    "button_ArrowDown_IsPressed": False,
    "button_ArrowLeft_IsPressed": False,
    "button_ArrowUp_IsPressed": False
}

buttonsLabel = ["Action Up", "Action Down", "Arrow Right", "Arrow Down", "Arrow Left", "Arrow Up"]


button_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5]

buttons = []

for pin in button_pins:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

debounce_time = 0.05  # 50 milliseconds debounce time
last_states = [button.value for button in buttons]
last_times = [time.monotonic() for _ in buttons]

def setButtonStateByIndex(index, state):
    global buttonsState
    buttons_list = list(buttonsState.keys())
    if 0 <= index < len(buttons_list):
        button_name = buttons_list[index]
        buttonsState[button_name] = state

async def detectButtonPresses():
    global last_states, last_times, buttonsState
    while True:
        for i, button in enumerate(buttons):
            current_state = button.value
            current_time = time.monotonic()

            if current_state != last_states[i]:
                last_times[i] = current_time
                last_states[i] = current_state

            if (current_time - last_times[i]) > debounce_time:
                if not current_state:
                    if i == 0:
                       buttonsState["button_ActionUp_IsPressed"] = True
                    elif i == 1:
                          buttonsState["button_ActionDown_IsPressed"] = True
                    elif i == 2:
                         buttonsState["button_ArrowRight_IsPressed"] = True
                    elif i == 3:
                            buttonsState["button_ArrowDown_IsPressed"] = True
                    elif i == 4:
                            buttonsState["button_ArrowLeft_IsPressed"] = True
                    elif i == 5:
                            buttonsState["button_ArrowUp_IsPressed"] = True
                else:
                    
                    if i == 0:
                       buttonsState["button_ActionUp_IsPressed"] = False
                    elif i == 1:
                        buttonsState["button_ActionDown_IsPressed"] = False
                    elif i == 2:
                        buttonsState["button_ArrowRight_IsPressed"] = False
                    elif i == 3:
                        buttonsState["button_ArrowDown_IsPressed"] = False
                    elif i == 4:
                        buttonsState["button_ArrowLeft_IsPressed"] = False
                    elif i == 5:
                        buttonsState["button_ArrowUp_IsPressed"] = False
                        
        await asyncio.sleep(0.001)  # 1 millisecond delay





moveBy = 5

async def shootSquare():
    global buttonsState
    while True:
        if buttonsState["button_ActionDown_IsPressed"]:
          square = Rect(0, 0, 10, 10, fill=0x000000)
          square.x = myCircle.x
          square.y = myCircle.y+7
          group.append(square)
          while square.x < 400:
             square.x += 3
             await asyncio.sleep(0.0016)
          group.remove(square)
        await asyncio.sleep(0.0016)

async def shootLines():
    global buttonsState
    while True:
        if buttonsState["button_ActionUp_IsPressed"]:
          line = Rect(0, 0, 20, 4, fill=0x000000)
          line.x = myCircle.x
          line.y = myCircle.y+7
          group.append(line)
          while line.x < 400:
             line.x += 10
             await asyncio.sleep(0.0016)
          group.remove(line)
        await asyncio.sleep(0.0016)

async def moveCircle():
    # print("Moving circle")
    global buttonsState
    while True:
       for button, state in buttonsState.items():
        if state:
            if button == "button_ArrowRight_IsPressed":
                myCircle.x += moveBy
            elif button == "button_ArrowLeft_IsPressed":
                myCircle.x -= moveBy
            elif button == "button_ArrowUp_IsPressed":
                myCircle.y -= moveBy
            elif button == "button_ArrowDown_IsPressed":
                myCircle.y += moveBy
        await asyncio.sleep(0.0016)

async def main():
        button_task = asyncio.create_task(detectButtonPresses())
        move_task = asyncio.create_task(moveCircle())
        line_task = asyncio.create_task(shootLines())
        square_task = asyncio.create_task(shootSquare())
        playMusicTask = asyncio.create_task(playMusic())
       
        await asyncio.gather(button_task, move_task, line_task, square_task, playMusicTask)

import pwmio


BuzzerOFF = 0
BuzzerON = 2**15

myBuzzer = pwmio.PWMOut(buzzer, variable_frequency=True)

async def playMusic():
    global buttonsState
   
    while True:
      if buttonsState["button_ActionDown_IsPressed"]:
          myBuzzer.frequency = 550
          myBuzzer.duty_cycle = BuzzerON
          await asyncio.sleep(0.1)
          myBuzzer.duty_cycle = BuzzerOFF
          myBuzzer.frequency = 300
          myBuzzer.duty_cycle = BuzzerON  
          await asyncio.sleep(0.3)
          myBuzzer.duty_cycle = BuzzerOFF
          myBuzzer.frequency = 280
          myBuzzer.duty_cycle = BuzzerON  
          await asyncio.sleep(0.1)
          myBuzzer.duty_cycle = BuzzerOFF
          myBuzzer.frequency = 270
          myBuzzer.duty_cycle = BuzzerON  
          await asyncio.sleep(0.1)
          myBuzzer.duty_cycle = BuzzerOFF
          myBuzzer.frequency = 260
          myBuzzer.duty_cycle = BuzzerON  
          await asyncio.sleep(0.1)
      if buttonsState["button_ActionUp_IsPressed"]:
          myBuzzer.frequency = 400
          myBuzzer.duty_cycle = BuzzerON
          await asyncio.sleep(0.03)
          myBuzzer.duty_cycle = BuzzerOFF
          await asyncio.sleep(0.03)
          myBuzzer.frequency = 500
          myBuzzer.duty_cycle = BuzzerON
          await asyncio.sleep(0.03)
          myBuzzer.duty_cycle = BuzzerOFF
      else:
          myBuzzer.duty_cycle = BuzzerOFF
          for freq in TONE_FREQ:
              if buttonsState["button_ActionUp_IsPressed"]:
                    break
              if buttonsState["button_ActionDown_IsPressed"]:
                    break
              myBuzzer.frequency = freq
              myBuzzer.duty_cycle = BuzzerON
              await asyncio.sleep(0.1)
              myBuzzer.duty_cycle = BuzzerOFF
              await asyncio.sleep(0.1)
      await asyncio.sleep(0.001)





try:
    asyncio.run(main())
except Exception as e:
    print("Error in main loop", e)
    time.sleep(3)
    print("Resetting")
    pass

 
