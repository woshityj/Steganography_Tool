import cv2  
import numpy as np  

# converting types to binary  
def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "08b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")
  
def encode(image_name, secret_data, lsb_bits):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
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
  
def decode(image_name, lsb_bits):
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

# Deprecated code
if __name__ == "__main__":
    input_image = "test.PNG"
    output_image = "encoded_image.PNG"
    secret_data = "This is a top secret message....."
    # encode the data into the image
    encoded_image = encode(image_name=input_image, secret_data=secret_data, lsb_bits = 5)
    # save the output image (encoded image)
    cv2.imwrite(output_image, encoded_image)
    # decode the secret data from the image
    decoded_data = decode(output_image, lsb_bits = 5)
    print("[+] Decoded data:", decoded_data)