from PIL import Image, ImageSequence
import image_steganography as ims


def get_all_frames(path):
    img = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(img):
        frames.append(frame.convert('RGB'))
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
    print(f"Number of secret bits: {data_len}")
    print(f"binary: {binary_secret_data}")
    print(f"number of frames: {len(frames)}")
    # return list
    out_frames = []
    # debugging
    count = 0
    for frame in frames:
        # if no data to insert, directly add the frame to return list
        if data_index >= data_len:
            print(f"skipping frame {count}")
            count += 1
        else:
            print(f"reforming frame {count}")
            count += 1

            # do LSB for frame
            for col in range(frame.width):
                for row in range(frame.height):
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


def decode(path, bit):
    frames = get_all_frames(path)
    binary_data = ""
    decoded_data = ""
    # for each frame, get the last x bit to binary_data
    for frame in frames:
        for col in range(frame.width):
            for row in range(frame.height):
                binary_rgb = ims.to_bin(frame.getpixel((col, row)))
                for i in range(1, 3):
                    binary_data += binary_rgb[i][-bit:]
                if len(binary_data) >= 8:
                    # convert to chr
                    decoded_data += chr(int(binary_data[:8], 2))
                    if len(decoded_data) > 100:
                        return
                    # check if obtained all data
                    if decoded_data.endswith("====="):
                        return decoded_data[:-5]
                    binary_data = binary_data[8:]


def save_gif(frames, path):
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=frames[0].info['duration'], loop=0)


save_gif(gif_encode("testingfiles/cat.gif", "Lorem ipsum dolor sit amet, consectetur adipiscing "
                                                        "elit.", 1), "testingfiles/encoded_cat.gif")
print(f"message: {decode('testingfiles/encoded_cat.gif', 1)}")
