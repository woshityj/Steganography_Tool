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
    # return list
    out_frames = []
    for frame in frames:
        # if no data to insert, directly add the frame to return list
        if data_index < data_len:
            # do LSB for frame
            for row in range(frame.height):
                for col in range(frame.width):
                    if data_index < data_len:
                        binary_rgb = ims.to_bin(frame.getpixel((col, row)))
                        rgb = [binary_rgb[0]]
                        # loop rgb
                        for i in range(1, 3):
                            data = ""
                            for b in range(bit):
                                if data_index < data_len:
                                    data += binary_secret_data[data_index]
                                    data_index += 1
                                else:
                                    data += binary_rgb[i][-bit + b]
                            binary_rgb[i] = binary_rgb[i][:-bit] + data
                            rgb.append(binary_rgb[i])
                        # rgb.append(binary_rgb[3])
                        frame.putpixel((col, row), tuple(int(i, 2) for i in rgb))
        # add temp to frames
        out_frames.append(frame)
    return out_frames


def gif_decode(path, bit):
    frames = get_all_frames(path)
    binary_data = ""
    decoded_data = ""
    # for each frame, get the last x bit to binary_data
    for frame in frames:
        for row in range(frame.height):
            for col in range(frame.width):
                binary_rgb = ims.to_bin(frame.getpixel((col, row)))
                for i in range(1, 3):
                    binary_data += binary_rgb[i][-bit:]
                if len(binary_data) >= 8:
                    # convert to chr
                    decoded_data += chr(int(binary_data[:8], 2))
                    # check if obtained all data
                    if decoded_data.endswith("====="):
                        return decoded_data[:-5]
                    binary_data = binary_data[8:]


def gif_save(frames, path):
    frames[0].save(path, save_all=True, append_images=frames[1:], disposal=2)

