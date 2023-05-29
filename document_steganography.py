from steganograpy_utility import to_bin

from tkinter.filedialog import asksaveasfilename, askopenfilename

def secret(secret_data):
    l = len(secret_data)
    i = 0
    add = ''
    while i < l:
        t = ord(secret_data[i]) # Getting ascii value of each character
        print(t)
        if (t >= 32 and t <= 64): # If ascii is between 32 and 64
            t1 = t + 48 # Increment the ascii value by 48
            t2 = t1 ^ 170 # Xoring with 170 (binary value - 10101010)
            res = bin(t2)[2:].zfill(8) # Converting obtained value to 8 bit binary value
            add += "0011" + res
        else:
            t1 = t - 48
            t2 = t1 ^ 170
            res = bin(t2)[2:].zfill(8)
            add += "0110" + res
        i += 1

    res1 = add + "111111111111"
    print("The string after binary conversion applying all the transformation :- " + (res1))
    length = len(res1)
    print("Length of binary after conversion:- ", length)

    return res1

def encode(document_name, encoded_file, res1):
    HM_SK = ""
    ZWC = {"00":u'\u200C', "01":u'\u202C', "11":u'\u202D', "10":u'\u200E'}
    file1 = open(document_name, "r+")

    encoded_file = open(encoded_file, "w+", encoding="utf-8")
    word = []
    for line in file1:
        word += line.split()
    i = 0
    while (i < len(res1)):
        s = word[int(i / 12)]
        j = 0
        x = ""
        HM_SK = ""
        while (j < 12):
            x = res1[j + i] + res1[i + j + 1]
            HM_SK += ZWC[x]
            j += 2
        s1 = s + HM_SK
        encoded_file.write(s1)
        encoded_file.write(" ")
        i += 12
    t = int(len(res1) / 12)
    while t < len(word):
        encoded_file.write(word[t])
        encoded_file.write(" ")
        t += 1
    encoded_file.close()
    file1.close()
    print("\nStego file has successfully generated")

def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string


def decode(document_path):
    ZWC_reverse = {u'\u200C':"00", u'\u202C':"01", u'\u202D':"11", u'\u200E':"10"}
    file4 = open(document_path, "r", encoding = "utf-8")
    temp = ''
    for line in file4:
        for words in line.split():
            T1 = words
            binary_extract = ""
            for letter in T1:
                if (letter in ZWC_reverse):
                    binary_extract += ZWC_reverse[letter]
            if binary_extract == "111111111111":
                break
            else:
                temp += binary_extract
    print("\nEncrypted message presented in code bits: ", temp)
    lengthd = len(temp)
    print("\nLength of encoded bits:- ", lengthd)
    i = 0
    a = 0
    b = 4
    c = 4
    d = 12
    final = ''
    while i < len(temp):
        t3 = temp[a:b]
        a += 12
        b += 12
        i += 12
        t4 = temp[c:d]
        c += 12
        d += 12
        if (t3 == '0110'):
            decimal_data = BinaryToDecimal(t4)
            final += chr((decimal_data ^ 170) + 48)
        elif (t3 == '0011'):
            decimal_data = BinaryToDecimal(t4)
            final += chr((decimal_data ^ 170) - 48)
    print("\nMessage after decoding from the stego file:- ", final)
    return final