# OCR Tool

This script is a simple Optical Character Recognition (OCR) tool that allows you to capture a region of the screen and perform OCR on it. It uses the Tesseract OCR engine and the Pytesseract library to perform OCR.

## Dependencies
This script requires Tesseract-OCR to be installed on your system. You can download it from  https://github.com/UB-Mannheim/tesseract/wiki and install it on your system. Make sure to add the Tesseract executable path to the .env file.
You will also need to install the dependencies using the following command: 
```bash
pip install -r requirements.txt
```
## Usage
Once the script is running, you can press Ctrl+Shift+Plus to capture a region of the screen. The script will perform OCR on the captured region and copy the result to the clipboard.