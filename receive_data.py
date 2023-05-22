import serial
import time
from gtts import gTTS
import pygame
import tempfile

# Set the serial port and baud rate
port = "/dev/cu.HC-05"  # Update with the appropriate port on your system
baud_rate = 9600  # Example baud rate, replace with the correct value

# Create a serial connection
ser = serial.Serial(port, baud_rate, rtscts=True)

# Read data continuously
while True:
    text = ''
    if ser.in_waiting > 0:
        data = ser.readline().decode().rstrip()
        print("Received:", data)
        fingers = data.split(',')
        thumb = int(fingers[0])
        index = int(fingers[1])
        pk = int(fingers[2])
        if thumb == 0 and index == 0 and pk == 0: # the button is not pressed
            text = ''
        elif thumb > 2300 and index < 3500 and pk < 12500: #100
            text = 'สวัสดีค่ะ คุณลูกค้ารับอะไรดีคะ'
        elif thumb < 2100 and index > 5000 and pk < 12200: #010
            text = 'รับหวานปกติไหมคะ'
        elif thumb < 2100 and index < 4000 and pk > 13300: #001
            text = 'รับอะไรเพิ่มอีกไหมคะ'
        elif thumb > 2200 and index > 4600 and pk < 12500: #110
            text = 'ทั้งหมดเท่านี้ค่ะ'
        elif thumb < 2000 and index > 4800 and pk > 13500: #011
            text = 'คุณลูกค้าสามารถสแกนจ่ายได้เลยค่ะ'
        elif thumb > 2200 and index < 3800 and pk > 13300: #101
            text = 'ขอบคุณค่ะ'
        elif thumb < 2000 and index < 3800 and pk < 12500 and thumb!= 0: #000
            text = 'ขอโทษค่ะ ฉันไม่สามารถตอบคำถามนี้ได้ รบกวนติดต่อพนักงานท่านอื่นนะคะ'
        if text != '':
            tts = gTTS(text, lang="th")
            temp_file = tempfile.NamedTemporaryFile(delete=True)
            tts.save(temp_file.name)

            pygame.mixer.init()
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()

            # Wait until sound finishes playing
            while pygame.mixer.music.get_busy():
                continue
    else:
        time.sleep(0.1)  # Add a small delay to avoid busy waiting

# Close the serial connection
ser.close()
