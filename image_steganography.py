import cv2  
import numpy as np  
import math
from steganograpy_utility import to_bin

def png_encode(image_name, secret_data, lsb_bits):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // (8 - lsb_bits)
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    print(data_len)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            data = ""
            for i in range(lsb_bits):
                if data_index < data_len:
                    data += binary_secret_data[data_index]
                    data_index += 1
                else:
                    data += "0"
            pixel[0] = int(r[:-lsb_bits] + data, 2)
            # least significant red pixel bit

            data = ""
            for i in range(lsb_bits):
                if data_index < data_len:
                    data += binary_secret_data[data_index]
                    data_index += 1
                else:
                    data += "0"
            pixel[1] = int(g[:-lsb_bits] + data, 2)
            # least significant green pixel bit

            data = ""
            for i in range(lsb_bits):
                if data_index < data_len:
                    data += binary_secret_data[data_index]
                    data_index += 1
                else:
                    data += "0"
            pixel[2] = int(b[:-lsb_bits] + data, 2)
            # least significant blue pixel bit

            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image
  
def png_decode(image_name, lsb_bits):
    print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-lsb_bits:]
            binary_data += g[-lsb_bits:]
            binary_data += b[-lsb_bits:]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

def bmp_encode(image_path, data, lsb_bits):
    # Open the file in binary mode
    with open(image_path, "rb") as image:
        f = image.read()
        byte_array = bytearray(f)

    # Convert data to binary
    data_binary = ''.join(format(ord(i), '08b') for i in data)
    data_len = format(len(data_binary), '08b')

    # Append the size of data to the start of data_binary
    data_binary = data_len + data_binary

    hidden_bits = 255 - lsb_bits
    # Append data_binary to image bytes
    for i in range(len(data_binary)):
        byte_array[i+54] = (byte_array[i+54] & hidden_bits) | int(data_binary[i])  # 54 bytes is standard BMP header

    return byte_array


def bmp_decode(image_path, lsb_bits):
    # Open the file in binary mode
    with open(image_path, "rb") as image:
        f = image.read()
        byte_array = bytearray(f)

    # Extract the size of original hidden data
    len_str = ""
    for i in range(8):
        if byte_array[i+54] & lsb_bits:
            len_str += '1'
        else:
            len_str += '0'
    data_len = int(len_str, 2)

    # Extract data
    data_binary = ""
    for i in range(data_len):
        if byte_array[i+54+8] & lsb_bits:
            data_binary += '1'
        else:
            data_binary += '0'

    # Convert binary data to string
    data_str = "".join(chr(int(data_binary[i:i+8], 2)) for i in range(0, len(data_binary), 8))
    return data_str