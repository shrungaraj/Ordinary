from flask import Flask, render_template, request
import requests
from PIL import Image, ImageDraw

app = Flask(__name__)

# Set your remove.bg API key here
API_KEY = 'r48QDmPv7y36cYDGciBwTQkz'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    image_file = request.files['image']

    # Check if a file was uploaded
    if image_file:
        # Read the image file
        image_data = image_file.read()

        # Send a POST request to remove.bg API
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': image_data},
            headers={'X-Api-Key': API_KEY},
        )

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            # Save the extracted foreground image
            with open('static/foreground.png', 'wb') as output_file:
                output_file.write(response.content)
            
            # Add background color to the image
            add_background_color('static/foreground.png', '#fd4800')
            
            return render_template('result.html')
        else:
            return render_template('index.html', error='Error processing the image. Please try again.')

    return render_template('index.html', error='No image file was uploaded.')


def add_background_color(image_path, color):
    image = Image.open(image_path)
    width, height = image.size

    background = Image.new('RGB', (width, height), color)
    background.paste(image, (0, 0), image)

    background.save(image_path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)