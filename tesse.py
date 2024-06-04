import threading
import pyautogui
from PIL import Image
import pytesseract
import keyboard
import pyperclip
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw
from plyer import notification
from dotenv import load_dotenv
import os

load_dotenv()

tesseract_exe = os.getenv('TESSERACT_EXE')

pytesseract.pytesseract.tesseract_cmd = tesseract_exe

# Global variables
ix, iy = -1, -1
px, py = -1, -1
drawing = False
rect_over = False
img = None
rectangle = (0,0,1,1)

# Mouse callback function
def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing, img, rect_over, rectangle, px, py

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        px, py = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rect_over = True
        rectangle = (ix, iy, x, y)
    
def select_region():
    global ix,iy,drawing, img, rect_over, rectangle, px, py
    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    img = screenshot.copy()

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('image',draw_rectangle)

    img2 = img.copy()
    while(1):
        img2 = img.copy()
        # conver to grayscale
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        darkened = cv2.addWeighted(img2, 0.3, np.zeros(img2.shape, img2.dtype), 0, 0)
        rct = img2[iy:py, ix:px]
        if drawing:
            # copy non darkened rectangle to darkened image
            darkened[iy:py, ix:px] = img2[iy:py, ix:px]
        # Draw white crosshair
        cv2.line(darkened, (px - 10, py), (px + 10, py), (255, 255, 255), 2)
        cv2.line(darkened, (px, py - 10), (px, py + 10), (255, 255, 255), 2)
        cv2.imshow('image',darkened)
        k = cv2.waitKey(1) & 0xFF # ESC key to break
        if rect_over:
            break
    cv2.destroyAllWindows()

    # Crop the selected region from the screenshot
    if rectangle[2] > rectangle[0] and rectangle[3] > rectangle[1]:
        region = screenshot[rectangle[1]:rectangle[3], rectangle[0]:rectangle[2]]
        # Reset the global variables        
        ix, iy = -1, -1
        drawing = False
        rect_over = False
        img = None
        rectangle = (0,0,1,1)
        return region
    else:
        ix, iy = -1, -1
        drawing = False
        rect_over = False
        img = None
        rectangle = (0,0,1,1)
        return None
    

def capture_and_ocr():
    region = select_region()
    if region is not None:
        # Convert the selected region to a PIL image
        region_image = Image.fromarray(region)
        try:
                
            # Perform OCR on the selected region
            text = pytesseract.image_to_string(region_image, lang='eng')

            # Copy the text to the clipboard
            pyperclip.copy(text)
        except Exception as e:
            notify('OCR Error', 'An error occurred during OCR. Please try again.')
    else:
        # print("rectangle was none")
        notify('OCR Error', 'No region selected or invalid selection. Please try again.')

def on_shortcut():
    capture_and_ocr()
    notify('OCR Result', pyperclip.paste())


def register_hotkey():
    keyboard.add_hotkey('ctrl+shift+plus', on_shortcut)

    notify('OCR Tool', 'OCR Tool is running. Press Ctrl+Shift+Plus to capture the screen region and perform OCR.'
           )
def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  
        timeout=10,
    )
    
def main():
    hotkey_thread = threading.Thread(target=register_hotkey, daemon=True)
    hotkey_thread.start()
    
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()


