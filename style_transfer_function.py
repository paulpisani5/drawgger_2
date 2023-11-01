
import tensorflow as tf
import numpy as np
import os
from PIL import Image
import random
import tensorflow_hub as hub
import cv2

# Load the style transfer model.
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def upscale_opencv(image_nparray, target_width, target_height):
    return cv2.resize(image_nparray, (target_width, target_height), interpolation=cv2.INTER_CUBIC)

def load_img(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.resize(img, [300, 300])
    img = tf.cast(img, tf.float32) / 255.0  # Normalize to [0, 1] as float32
    img = tf.expand_dims(img, 0)  # Add batch dimension
    return img

def load_img_no_resize(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.cast(img, tf.float32) / 255.0  # Normalize to [0, 1] as float32
    img = tf.expand_dims(img, 0)  # Add batch dimension
    return img

def resize_image(input_path, output_path, base_width=400):
    img = Image.open(input_path)
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), Image.LANCZOS)
    img.save(output_path)

def apply_styles_to_image(image_path):
    # List of available styles and their corresponding filenames
    style_files = os.listdir('styles/')
    content_image = load_img_no_resize(image_path)

    output_images = []
    for style_filename in style_files:
        if style_filename != ".DS_Store":
            styled_image_path = apply_style(image_path, style_filename)
            output_images.append((style_filename, styled_image_path))
    return output_images

# def apply_style(content_path, style_name, method="Random Choice"):
#     style_files = [f for f in os.listdir('styles/') if f.startswith(style_name) and not f.startswith('.DS_Store')]
#     content_image = load_img_no_resize(content_path)
#
#     selected_style_path = os.path.join('styles', random.choice(style_files))
#     style_image = load_img(selected_style_path)
#
#     stylized_image = hub_model(tf.constant(load_img(content_path)), tf.constant(style_image))[0]
#     original_image = stylized_image
#     # stylized_image = tf.image.resize(stylized_image, original_image.shape[1:3])
#     stylized_image = tf.image.resize(stylized_image, [tf.shape(content_image)[1], tf.shape(content_image)[2]])
#     stylized_image = tf.squeeze(stylized_image).numpy()
#     stylized_image = (stylized_image * 255).astype(np.uint8)
#
#     style_name_without_extension = os.path.splitext(style_name)[0]
#     output_path = f"styled_{style_name_without_extension}.jpg"
#     Image.fromarray(stylized_image).save(os.path.join('styled', output_path))
#     print(output_path)
#     return output_path

def apply_style(content_path, style_name, method="Random Choice"):
    style_files = [f for f in os.listdir('styles/') if f.startswith(style_name) and not f.startswith('.DS_Store')]
    content_image = load_img_no_resize(content_path)

    selected_style_path = os.path.join('styles', random.choice(style_files))
    style_image = load_img(selected_style_path)

    stylized_image = hub_model(tf.constant(load_img(content_path)), tf.constant(style_image))[0]
    stylized_image = tf.squeeze(stylized_image).numpy()
    stylized_image = (stylized_image * 255).astype(np.uint8)

    # Upscale using OpenCV
    target_width, target_height = Image.open(content_path).size
    upscaled_image = upscale_opencv(stylized_image, target_width, target_height)

    style_name_without_extension = os.path.splitext(style_name)[0]
    output_path = f"styled_{style_name_without_extension}.jpg"
    Image.fromarray(upscaled_image).save(os.path.join('styled', output_path))
    print(output_path)
    return output_path
