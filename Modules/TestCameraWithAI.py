from CameraModule import *
import os
from pyzbar.pyzbar import decode
from PIL import Image
import openai

openai.api_key = "10540e2776604f23872c9a1252d76694"
openai.api_type = "azure"
openai.api_base = "https://team03roborumble.openai.azure.com/"
openai.api_version = "2023-07-01-preview"

# Function to scan QR code and extract text
def scan_qr_code(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')
    else:
        return None

# Function to ask AI and get a one-word answer
def ask_ai(riddle_text):
    try:       
        messages = [
            {
                "role":"system",
                "content":"You are an AI assistant that helps people solve riddles intelligently."
            },
            {
                "role":"user",
                "content": "You are an AI assistant that helps me navigate my autonomous moving robot; by solving riddles, you give me smart and efficient answers as to what direction I should ideally go."
            },
            {
                "role":"user",
                "content": "You are an AI assistant that helps me navigate my autonomous moving robot; by solving riddles, you give me a smart and correct answer from - Forward, Backward, Left or Right."
            },
            {
                "role":"user",
                "content": riddle_text
            }
        ]

        # Generate a short answer using the Azure OpenAI model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            engine="team03roborubble",
            messages=messages,
            temperature=0.7,
            max_tokens=10,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        # print(response)

        # Extract and return the answer from the response
        answer = response["choices"][0]["message"]["content"]
        return answer

    except Exception as e:
        return str(e)

def scan_and_decipher():
    # Create a directory for images
    currentPath = os.path.join(os.getcwd(), 'images/')
    os.mkdir(currentPath)

    file_path = currentPath + "test.jpg"

    # Capture image and save it
    startCameraAndGetImage().save(file_path, force=True)
    print("Image saved to:", file_path)

    riddle_text = scan_qr_code(file_path)
    print("The decrypted English prompt is -> " + riddle_text)

    if riddle_text:
        riddle_text = "Solve this riddle: " + riddle_text  + "; Answer in one word please."
        ai_answer = ask_ai(riddle_text)

        if ai_answer:
            print("AI's answer to the riddle:", ai_answer)
        else:
            print("AI couldn't provide an answer.")
    else:
        print("No QR code found or QR code couldn't be decoded.")

    return ai_answer    