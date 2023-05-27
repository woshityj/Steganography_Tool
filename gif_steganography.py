from PIL import Image, ImageSequence
import image_steganography as ims


def get_all_frames(path):
    img = Image.open(path)
    frames = []
    # try:
    #     print(img.info['transparency'])
    #     convert_rule = "RGBA"
    # except KeyError:
    convert_rule = "RGB"
    for frame in ImageSequence.Iterator(img):
        frames.append(frame.convert(convert_rule))
    return frames


def gif_encode(path, msg, bit):
    frames = get_all_frames(path)
    max_byte = frames[0].height * frames[0].width * len(frames) * bit // 8
    if len(msg) > max_byte:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    # add stopping criteria
    msg += "====="
    # data to binary
    binary_secret_data = ims.to_bin(msg)
    data_index = 0
    # size of data to hide
    data_len = len(binary_secret_data)
    # for each pixel position
    for col in range(frames[0].height):
        for row in range(frames[0].width):
            # for each frame:
            for fn in range(len(frames)):
                # if data obtained
                if data_index >= data_len:
                    return frames
                # else read current pixel and add data
                rgb = ims.to_bin(frames[fn].getpixel((row, col)))
                for i in range(1, 3):  # skip r value as tested unstable
                    data = ""
                    for b in range(bit):  # determine how many bits to put in pixels
                        if data_index < data_len:
                            data += binary_secret_data[data_index]
                            data_index += 1
                        else:
                            data += rgb[i][-bit + b]
                    rgb[i] = rgb[i][:-bit] + data
                # put modified pixel
                frames[fn].putpixel((row, col), tuple(int(i, 2) for i in rgb))


def gif_decode(path, bit):
    frames = get_all_frames(path)
    binary_data = ""
    decoded_data = ""
    # for each pixel position
    for col in range(frames[0].height):
        for row in range(frames[0].width):
            # for each frame:
            for fn in range(len(frames)):
                # else read current pixel and add data
                rgb = ims.to_bin(frames[fn].getpixel((row, col)))
                for i in range(1, 3):  # skip r value as tested unstable
                    binary_data += rgb[i][-bit:]
                if len(binary_data) >= 8:
                    # convert to chr
                    decoded_data += chr(int(binary_data[:8], 2))
                    # check if obtained all data
                    if decoded_data.endswith("====="):
                        return decoded_data[:-5]
                    binary_data = binary_data[8:]


def gif_save(frames, path):
    frames[0].save(path, save_all=True, append_images=frames[1:], disposal=2, optimize=False, lossless=True)


# # debug
# bn = 5
# gif_save(gif_encode("testingfiles/cat.gif", """
# Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vitae ultrices justo. Vivamus maximus bibendum orci
# at hendrerit. Morbi tincidunt a nulla a commodo. Suspendisse eu nulla in risus aliquam pharetra eget a sapien.
# Pellentesque a ante et est porta lobortis. Fusce quis fermentum ante. Aliquam scelerisque vel dui vitae accumsan.
# """, bn), "testingfiles/encoded_cat.gif")
#
# print(gif_decode("testingfiles/encoded_cat.gif", bn))
