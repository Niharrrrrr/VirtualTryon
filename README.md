# Virtual Try-On with Flask, Twilio, and HuggingFace

This repository contains the code for a virtual try-on application built using Flask, Twilio , Gradio and Ngrok.

## Features
- Receive images of the user and a garment via WhatsApp.
- Use Gradio’s Inference API to generate virtual try-on results.
- Display's the final image to the user via WhatsApp.

## Prerequisites
Before running this project, ensure you have the following:
- Twilio account setup with whatsapp service enabled.
- Normal HF account to use the Gradio API.
- Compatible Python installed on your machine.

## Twilio Setup

1. Used the given link: (https://www.twilio.com/console/sms/whatsapp/sandbox):
2. Get your **Twilio Account SID** and **Auth Token** from your Twilio console:.
3. Upate the .env file with the credentials.

## NOTE: 

ThIs wasn't running on their ZeroGPU so I couldn't use that for my task https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On , So I used https://huggingface.co/spaces/Nymbo/Virtual-Try-On Space using Gradio.

## Setup
Clone the repository:
```bash
git https://github.com/Niharrrrrr/VirtualTryon.git
cd VirtualTryon
```
Install the required Python packages:
```
pip install -r requirements.txt
```
Set up your environment variables:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
NGROK_URL=The URL you get after running that terminal
```

Start the Flask server:
```
python app.py
```
## Setup for Ngrok. 
Since the Flask server runs locally, we use **ngrok** to expose the server to the internet so that Twilio's WhatsApp Sandbox works.

1. Download ngrok with respect to your specs.
2. Once installed, authenticate ngrok by running:
```
ngrok authtoken your_ngrok_auth_token
```
3. Running ngrok to expose your local Flask server:
```
.\ngrok http 8080
```
You will see a link like:  https://link.app and set this as your Twilio webhook under the WhatsApp Sandbox Settings:
![alt text](image.png)
```
https://link.app/webhook
```
Also Updated the .env file with your ngrok URL.

## Usage
1. Forward your photo to the whatsapp chat.
2. It will ask you to send the photo of the garment
3. After that wait for a few seconds and it displays you your image.

## Note:
I was unable to deploy this for free because of some dependency problems on Render. But we can use that and many paid services for deployment.

## Future Scopes
1. To handle scaling of this we can create a more robust api with session managements for each user , queuing to get proper results.
2. This model is running via inference API of huggingface which is basically gpu usage dependent. To improve the speed we can clone that in our HF Space where we can run this on a better gpu to get faster results.
3. Instead of using Ngrok we can deploy this on Cloud platforms to get better speed and scalable solutions.
4. Improvements can be added in a way where we describe the garment , we can customize that according to each garment to get a better description of that.
5. Other use cases are many. In healthcare, we can create a ambulance service using Twilio SMS/Whatsapp , we can create a medicine delivery system. This application can be used in many E-commerce apps to get a better view of what you're buying.
6. Security implications are many , because we need to have many guardrails present because people might send NSFW content via this channel , also it might have some issues displaying the  body structure of the user which might create some scenes. 

## Results

![alt text](1.jpg)
![alt text](2.jpg)
![alt text](3.jpg)
   





