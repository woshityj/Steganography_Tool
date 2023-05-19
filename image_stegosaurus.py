import cv2
import numpy as np

def to_bin(data):
    """Convert 'data' to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image, secret_message):
    # Calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode ", n_bytes)

    # Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
    
    secret_message += "#####" # You can use any string as the delimeter

    data_index = 0
    # Convert input data to binary format using to_bin() function
    binary_secret_msg = to_bin(secret_message)

    data_len = len(binary_secret_msg) # Find the length of data that needs to be hidden
    for values in image:
        for pixel in values:
            # Convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # Modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # Hide the data into least significant bit of red pixel
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # Hide the data into least significant bit of green pixel
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # Hide the data into least significant bit of the blue pixel
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            # If data is encoded, just break out the loop
            if data_index >= data_len:
                break
    return image

def decode(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = to_bin(pixel) # Convert the red, green and blue values into binary format
            binary_data += r[-1] # Extracting data from the least significant bit of red pixel
            binary_data += g[-1] # Extracting data from the least significant bit of green pixel
            binary_data += b[-1] # Extracting data from the least significant bit of blue pixel
    # Split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # Convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####": # Check if we have reached the delimeter which is "######"
            break
    # print(decoded_data)
    return decoded_data[:-5] # Remove the delimeter to show the original hidden message

def encode_text():
    image_name = input("Enter image name(with extension): ")
    image = cv2.imread(image_name) # Read the input image using OpenCV-Python.
    
    print("The shape of the image is: ", image.shape)

    data = input("Enter data to be encoded: ")
    if (len(data) == 0):
        raise ValueError("Data is empty")
    
    filename = input("Enter the name of new encoded image(with extension): ")
    encoded_image = encode(image, data)
    cv2.imwrite(filename, encoded_image)

def decode_text():
    image_name = input("Enter the name of the steganographed image that you want to decode (with extension): ")
    image = cv2.imread(image_name) # Read the input image using OpenCV-Python.

    text = decode(image)
    return text

def Steganography():
    a = input("Image Steganography \n1. Encode the data \n2. Decode the data \nYour input is: ")
    userinput = int(a)
    if (userinput == 1):
        print("\nEncoding...")
        encode_text()
    
    elif (userinput == 2):
        print("\nDecoding...")
        print("\nDecoded message is " + decode_text())
    else:
        raise Exception("Enter correct input")

Steganography()