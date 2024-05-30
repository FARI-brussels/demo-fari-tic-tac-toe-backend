import base64

def encode_image_to_base64(image_path, output_path):
    # Read the image file in binary mode and encode it to base64
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Add the data URL prefix
    data_url_prefix = "data:image/png;base64,"
    full_encoded_string = data_url_prefix + encoded_string
    
    # Save the base64 encoded string with the prefix to a text file
    with open(output_path, 'w') as text_file:
        text_file.write(full_encoded_string)
    
    print(f"Encoded image saved to {output_path}")

def read_base64_image(input_path):
    # Read the base64 encoded image from a text file
    with open(input_path, 'r') as file:
        base64_image = file.read().strip()
    
    return base64_image

# Example usage:
image_path = 'test_image.png'
output_path = 'test_image.txt'

# Encode image and save to text file
encode_image_to_base64(image_path, output_path)

# Read the base64 encoded image from the text file
base64_image = read_base64_image(output_path)

