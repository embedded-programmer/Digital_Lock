import tkinter as tk
from tkinter import ttk
import threading
import time
import serial  
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
RELAY_PIN = 16    

GPIO.setup(RELAY_PIN, GPIO.OUT)

MAX_VAL = 1023

PASS_1 = 1000
PASS_2 = 1000
PASS_3 = 1000
PASS_STATE = False

class CircularProgress:
    def __init__(self, canvas, x, y, radius, width=20, color='white'):
        self.canvas = canvas
        self.x, self.y = x, y
        self.radius = radius
        self.width = width
        self.color = color

        self.arc = None
        self.label = None
        GPIO.output(RELAY_PIN, GPIO.HIGH)
                            
    def set_progress(self, progress):
        if self.arc:
            self.canvas.delete(self.arc)
        if self.label:
            self.canvas.delete(self.label)

        start_angle = 90  # Start from the top
        end_angle = start_angle - 360 * progress
        self.arc = self.canvas.create_arc(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            start=start_angle, extent=end_angle - start_angle,
            width=self.width, outline=self.color, style=tk.ARC
        )

        label_x = self.x
        label_y = self.y + self.radius + 20
        self.label = self.canvas.create_text(label_x, label_y, text=f"{int(progress*MAX_VAL)}", fill=self.color,
                                             font=("Helvetica", 12, "bold"))

class CircularProgressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Lock")

        self.canvas = tk.Canvas(root, width=720, height=340, bg='white')
        self.canvas.pack()

        self.circular_progress_1 = CircularProgress(self.canvas, 120, 150, 100, color='red')
        self.circular_progress_2 = CircularProgress(self.canvas, 360, 150, 100, color='green')
        self.circular_progress_3 = CircularProgress(self.canvas, 600, 150, 100, color='blue')

        self.start_button = ttk.Button(root, text="Start Reading USART", command=self.start_usart_thread)
        self.start_button.pack()

        self.stop_button = ttk.Button(root, text="Stop Reading USART", command=self.stop_usart_thread, state=tk.DISABLED)
        self.stop_button.pack()

        self.pass_button = ttk.Button(root, text="ENTER PASSWORD", command=self.password_check, state=tk.DISABLED)
        self.pass_button.pack()

        
        self.serial_port = None
        self.read_usart_thread = None
        self.is_reading_usart = False

    def start_usart_thread(self):
        try:
            # Change the port and baudrate based on your USART configuration
            self.serial_port = serial.Serial(port='/dev/serial0', baudrate=9600, timeout=0.01)
            self.is_reading_usart = True

            self.start_button['state'] = tk.DISABLED
            self.stop_button['state'] = tk.NORMAL
            self.pass_button['state'] = tk.NORMAL
            
            self.read_usart_thread = threading.Thread(target=self.read_usart_data)
            self.read_usart_thread.start()

        except Exception as e:
            print(f"Error opening serial port: {e}")

    def stop_usart_thread(self):
        self.is_reading_usart = False
        self.start_button['state'] = tk.NORMAL
        self.stop_button['state'] = tk.DISABLED

        
    def password_check(self):
        if PASS_STATE == 1:
            GPIO.output(RELAY_PIN, GPIO.LOW)
            self.pass_button['text']="ACCESS GRANTED!"

        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            self.pass_button['text']="ENTER PASSWORD"

        
    def read_usart_data(self):
        while self.is_reading_usart:
            try:
                line = self.serial_port.readline().decode().strip()
                values = [int(value) for value in line.split(',')]  # Assuming data is comma-separated
                if len(values) == 3:
                    adc_value_1, adc_value_2, adc_value_3 = values
                    progress_1 = adc_value_1 / MAX_VAL
                    progress_2 = adc_value_2 / MAX_VAL
                    progress_3 = adc_value_3 / MAX_VAL
            
                    self.circular_progress_1.set_progress(progress_1)
                    self.circular_progress_2.set_progress(progress_2)
                    self.circular_progress_3.set_progress(progress_3)
                    
                    global PASS_STATE
                    
                    if PASS_1 == int(progress_1*MAX_VAL) and PASS_2 == int(progress_2*MAX_VAL) and PASS_3 == int(progress_3*MAX_VAL) :
                        PASS_STATE = True
                    else:
                        PASS_STATE = False


                    
            except Exception as e:
                print(f"Error reading USART data: {e}")

            #time.sleep(1)  # Adjust the sleep time based on your requirements

if __name__ == "__main__":
    root = tk.Tk()
    app = CircularProgressApp(root)
    root.mainloop()
