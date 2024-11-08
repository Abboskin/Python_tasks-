import fitz
import requests
import os

BOT_TOKEN = '7633846433:AAGgwuh-msxd98rQn4z6TYV2Cch-TOmkIMo'
CHANNEL_ID = '@book4task'

book_path = "C:\\IELTS\\books\\1000-English-Collocations-Ebook.pdf"
screenshot_path = "screenshot.png"

def generate_screenshot(pdf_path, output_image_path):
    with fitz.open(pdf_path) as pdf:
        page = pdf[0]  
        pix = page.get_pixmap()  
        pix.save(output_image_path) 

def send_to_telegram(bot_token, channel_id, file_path, image_path):
    with open(image_path, 'rb') as image:
        response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendPhoto',
            data={'chat_id': channel_id},
            files={'photo': image}
        )
    message_id = response.json().get("result", {}).get("message_id")

    with open(file_path, 'rb') as book:
        requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendDocument',
            data={
                'chat_id': channel_id,
                'reply_to_message_id': message_id
            },
            files={'document': book}
        )

generate_screenshot(book_path, screenshot_path)
send_to_telegram(BOT_TOKEN, CHANNEL_ID, book_path, screenshot_path)

os.remove(screenshot_path)
