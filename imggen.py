import os
import streamlit as st
from openai import OpenAI
from PIL import Image
from io import BytesIO
import requests
from dotenv import find_dotenv, load_dotenv

# Load environment variables
#load_dotenv(find_dotenv())
api_key = os.environ["OPENAI_API_KEY"]=#API Key
client = OpenAI(api_key=api_key)



# Initialize the OpenAI client with your API key
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit Page Configuration

# Display title and introduction
st.title('Image Generator')

# Collect user input for image generation
image_prompt = st.text_input("Enter prompt for image generation", 'Type something here...')
size_config = st.selectbox("Select image size", ("256x256", "512x512", "1024x1024"))
quality_config = st.selectbox("Select image quality", ("standard", "hd"))
style_config = st.selectbox("Select image style", ("natural", "vivid"))

# Generate the image on button click
if st.button('Generate Image'):
    # Function to generate image
    def generate_image(prompt: str, size: str = "256x256", quality: str = 'standard', style: str = 'natural') -> Image:
        """
        Generates an image using OpenAI DALL-E-2 model.
        """
        response = client.images.generate(
            prompt=prompt,
            n=1,
            style=style,
            size=size,
            quality=quality,
        )
        img_url = response.data[0].url
        img_response = requests.get(img_url)
        return Image.open(BytesIO(img_response.content))

    # Generating the image
    generated_image = generate_image(
        prompt=image_prompt, 
        size=size_config, 
        quality=quality_config, 
        style=style_config
    )

    # Display the generated image
    st.image(generated_image, caption='Generated Image', use_column_width=True)
