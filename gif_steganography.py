from PIL import Image, ImageSequence, GifImagePlugin
import image_steganography as ims

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS


def encode(image_path, secret_data, lsb_bits, output_path):
    # load image
    img = Image.open(image_path)
    pixels = img.load()
    # check size of data can fit
    max_byte = img.height * img.width * img.n_frames * lsb_bits // 8
    if len(secret_data) > max_byte:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    # add stopping criteria
    secret_data += "====="
    # data to binary
    binary_secret_data = ims.to_bin(secret_data)
    data_index = 0
    # size of data to hide
    data_len = len(binary_secret_data)
    print(f"Number of secret bits: {data_len}")
    print(f"binary: {binary_secret_data}")
    print(f"number of frames: {img.n_frames}")
    # return variable
    return_data = []

    # for each frame number:
    for fn in range(img.n_frames):
        # get current frame
        img.seek(fn)
        temp = Image.new('RGB', (img.width, img.height))
        print(f"duration for frame {fn} : {img.info['duration']}")
        # if data_index >= data_len:
        #     print(f"skipped frame {fn}")
        #     return_data.append(img)
        #     img.show()
        #     break

        # for each pixel
        for row in range(img.height):
            for col in range(img.width):
                rgb = []
                binary_rgb = ims.to_bin(img.getpixel((col, row)))
                # add the data in
                for i in range(3):
                    data = ""
                    for b in range(lsb_bits):
                        if data_index < data_len:
                            data += binary_secret_data[data_index]
                            data_index += 1
                        else:
                            data += binary_rgb[i][-3+b]
                    binary_rgb[i] = binary_rgb[i][:-lsb_bits] + data
                    rgb.append(int(binary_rgb[i], 2))
                # add pixel
                temp.putpixel((col, row), tuple(rgb))
        # add to return data
        print(f"reformed frame {fn}")
        return_data.append(temp)

    print("saving...")
    # save gif
    return_data[0].save(output_path, save_all=True, append_images=return_data[1:], duration=img.info['duration'], loop=0)


encode("C:/Users/Richie/Pictures/44.gif", "hello", 1, "C:/Users/Richie/Pictures/45.gif")
