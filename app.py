import os
import requests
import cv2
from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from gradio_client import Client as GradioClient, file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Virtual Tryon Assignment. Made by : Nihar Mittal", 200

user_sessions = {}

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
gradio_client = GradioClient("Nymbo/Virtual-Try-On")
NGROK_URL = os.getenv("NGROK_URL")

@app.route('/webhook', methods=['POST'])
def webhook():
    sender_number = request.form.get('From')
    media_url = request.form.get('MediaUrl0')

    print(f"Received media URL: {media_url}")

    resp = MessagingResponse()

    if media_url is None:
        resp.message("I did not get an image. Try sending your image again.")
        return str(resp)

    if sender_number not in user_sessions:
        user_sessions[sender_number] = {}
        if media_url:
            user_sessions[sender_number]['person_image'] = media_url
            resp.message("Nice! Now please send the image of the cloth you want to try on.")
        else:
            resp.message("Please send your image to begin the virtual try-on.")
    elif 'person_image' in user_sessions[sender_number] and 'garment_image' not in user_sessions[sender_number]:
        if media_url:
            user_sessions[sender_number]['garment_image'] = media_url
            try_on_image_url = send_to_gradio(user_sessions[sender_number]['person_image'], media_url)
            if try_on_image_url:
                send_media_message(sender_number, try_on_image_url)
                resp.message("Here is your virtual try-on result!")
            else:
                resp.message("Soomething went wrong with the try-on process.")
            del user_sessions[sender_number]
        else:
            resp.message("Do send the garment image to complete the process.")
    else:
        resp.message("Please send your image to begin the virtual try-on.")

    return str(resp)

def send_to_gradio(person_image_url, garment_image_url):
    person_image_path = download_image(person_image_url, 'person_image.jpg')
    garment_image_path = download_image(garment_image_url, 'garment_image.jpg')

    if person_image_path is None or garment_image_path is None:
        print("Error: One of the images could not be downloaded.")
        return None

    try:
        result = gradio_client.predict(
            dict={"background": file(person_image_path), "layers": [], "composite": None},
            garm_img=file(garment_image_path),
            garment_des="A cool description of the garment",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )

        print(f"API result: {result}")

        if result and len(result) > 0:
            try_on_image_path = result[0]
            print(f"Generated try-on image path: {try_on_image_path}")

            static_dir = 'static'
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
                print(f"Created directory: {static_dir}")

            if os.path.exists(try_on_image_path):
                img = cv2.imread(try_on_image_path)
                target_path_png = os.path.join(static_dir, 'result.png')
                cv2.imwrite(target_path_png, img)
                print(f"Image saved to: {target_path_png}")

                return f"{NGROK_URL}/static/result.png"
            else:
                print(f"Image not found at: {try_on_image_path}")
                return None

        print("No image returned from the API.")
        return None

    except Exception as e:
        print(f"Error interacting with Gradio API: {e}")
        return None

def send_media_message(to_number, media_url):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="Your virtual try-on result:",
        media_url=[media_url],
        to=to_number
    )
    print(f"Sent media message to {to_number}. Message SID: {message.sid}")

def download_image(media_url, filename):
    try:
        message_sid = media_url.split('/')[-3]
        media_sid = media_url.split('/')[-1]

        print(f"Message SID: {message_sid}, Media SID: {media_sid}")

        media = client.api.accounts(TWILIO_ACCOUNT_SID).messages(message_sid).media(media_sid).fetch()

        media_uri = media.uri.replace('.json', '')
        image_url = f"https://api.twilio.com{media_uri}"

        print(f"Downloading image from: {image_url}")

        response = requests.get(image_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully as {filename}.")
            return filename
        else:
            print(f"Failed to download image: {response.status_code}")
            return None
    except Exception as err:
        print(f"Error downloading image from Twilio: {err}")
        return None

@app.route('/static/<path:filename>')
def serve_static_file(filename):
    file_path = os.path.join('static', filename)
    if os.path.exists(file_path):
        return send_from_directory('static', filename, mimetype='image/png')
    else:
        print(f"File not found: {filename}")
        return "File not found", 404

if __name__ == '__main__':
    app.run(port=8080)
