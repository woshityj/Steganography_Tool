import wave
from pydub import AudioSegment

def encode_wav_data(name_of_file, data):

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

from pydub import AudioSegment
import array

def encode_audio_segment_data(name_of_file, data):
    song = AudioSegment.from_file(name_of_file, format="wav")

    # Convert data to binary string
    res = ''.join(format(i, '08b') for i in bytearray(data, encoding='utf-8'))
    print("\nThe string after binary conversion: " + res)
    length = len(res)
    print("Length of binary after conversion: ", length)

    # Add delimiter to the data
    data = data + "*^*^*"

    # Convert data characters to binary and store in a list
    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    # Modify the audio frames
    frames = array.array('h', song.raw_data)
    j = 0
    for i in range(len(result)):
        res = bin(frames[j])[2:].zfill(16)
        if res[-4] == str(result[i]):
            frames[j] = frames[j] & 0xFFFD
        else:
            frames[j] = (frames[j] & 0xFFFD) | 0x0002
            frames[j] = (frames[j] & 0xFFFE) | result[i]
        j = (j + 1) % len(frames)

    return frames.tobytes()


def decode_wav_data(name_of_file):

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
    


def decode_mp3_data(name_of_file):
    from pydub import AudioSegment
    # Load the MP3 file
    audio = AudioSegment.from_mp3(name_of_file)

    # Extract the least significant bit from audio frames
    frames = audio.get_array_of_samples()
    extracted_payload = ""
    for sample in frames:
        # Extract the least significant bit from the sample
        bit = sample & 0x0001
        extracted_payload += str(bit)

    # Convert the extracted binary payload to text
    payload = ""
    for i in range(0, len(extracted_payload), 8):
        byte = extracted_payload[i:i+8]
        char_code = int(byte, 2)
        payload += chr(char_code)
        if payload[-5:] == "*^*^*":
            print("The Encoded data was :--" , payload[:-5])
            return payload[-5:]

