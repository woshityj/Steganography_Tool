from pydub import AudioSegment
import wave
import os


def encode_aud_data(name_of_file, data):

    _, ext = os.path.splitext(name_of_file)
    if ext == '.mp3':
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        convertMP3ToWave(name_of_file)
        filename = os.path.join("./tmp", _ + '.wav')
        print(filename)
        song = wave.open(filename, mode = 'rb')
    else:
        # name_of_file = input("Enter name of the file (with extension): - ")
        song = wave.open(name_of_file, mode = 'rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    # data = input("\nEnter the secret message:- ")

    res = ''.join(format(i, '08b') for i in bytearray(data, encoding = 'utf-8'))
    print("\nThe string after binary conversion:- " + (res))
    length = len(res)
    print("\nLength of binary after conversion:- ", length)

    data = data + "*^*^*"

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0, len(result), 1):
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res) - 4] == result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1
    
    frame_modified = bytes(frame_bytes)
    song.close()
    return frame_modified

def decode_aud_data(name_of_file):

    _, ext = os.path.splitext(name_of_file)
    if ext == '.mp3':
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        convertMP3ToWave(name_of_file)
        filename = os.path.join("./tmp", _ + '.wav')
        song = wave.open(filename, mode = 'rb')
    else:
        # name_of_file = input("Enter name of the file to be decided:- ")
        song = wave.open(name_of_file, mode = 'rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    extracted = ""
    p = 0
    for i in range(len(frame_bytes)):
        if (p == 1):
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res) - 2] == 0:
            extracted += res[len(res) - 4]
        else:
            extracted += res[len(res) - 1]
        
        all_bytes = [ extracted[i: i + 8] for i in range(0, len(extracted), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was :--" , decoded_data[:-5])
                p = 1
                return decoded_data[:-5]
    
def convertWAVToMP3(name_of_file):
    audio_segment = AudioSegment.from_file(name_of_file)
    _, ext = os.path.splitext(name_of_file)
    audio_segment.export(os.path.join("./tmp", _ + '.mp3'), format = "wav")

def convertMP3ToWave(name_of_file):
    audio_segment = AudioSegment.from_file(name_of_file)
    _, ext = os.path.splitext(name_of_file)
    audio_segment.export(os.path.join("./tmp", _ + '.wav'), format = "wav")