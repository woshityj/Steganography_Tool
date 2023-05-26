import shutil
import os
import cv2
import image_steganography
from subprocess import call, STDOUT

def count_frames(filename):
    cap = cv2.VideoCapture(filename)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frame in video are: {length - 1}")
    return length

def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder = "./tmp"
    print("[Info] tmp directory is created")
    vidcap = cv2.VideoCapture(video)
    count = 0
    print("[Info] Extracting frames from video \n Please be patient")
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1
    print("[INFO] All frames are extrated from value")

def encode_string(secret, frame_number, lsb, root ="./tmp"):
    filename = os.path.join(root, frame_number + '.png')
    encoded_image = image_steganography.png_encode(filename, secret, lsb)
    cv2.imwrite(filename, encoded_image)

def save_as(filename):
    call(["ffmpeg", "-i", "tmp/%d.png", "-c:v", "libx264rgb", "-crf", "0", "-preset", "faster", f"{filename}.mp4"], stdout = open(os.devnull, "w"), stderr=STDOUT)
    clean_tmp()

def clean_tmp(path = "./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")

def encode_video(video, secret, frame_number, lsb):
    no_of_frames = count_frames(video)
    if int(frame_number) < 0 or int(frame_number) > no_of_frames:
        raise ValueError("Frame Number is out of bounds")
    frame_extraction(video)
    encode_string(secret, frame_number, int(lsb))

def decode_video(video, frame_number, lsb):
    no_of_frames = count_frames(video)
    if int(frame_number) < 0 or int(frame_number) > no_of_frames:
        raise ValueError("Frame Number is out of bounds")
    frame_extraction(video)
    encoded_frame = os.path.join("./tmp", frame_number + '.png')
    secret = image_steganography.png_decode(encoded_frame, int(lsb))
    clean_tmp()
    return secret


# encode_video("cover_video.mp4", "Hello, I have a very big cock", "2", 1)
# secret = decode_video("lossless.mp4", "2", 1)
# print(secret)