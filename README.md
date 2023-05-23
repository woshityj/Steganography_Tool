# i_am_a_stegosaurus

# Installation:
You can install Anaconda and create a virtual environment before running

Run this to install dependencies
```
pip install -r requirements.txt
```

1. Download FFMPEG from https://ffmpeg.org/download.html
2. Extract out the 3 exe files (ffmpeg.exe, ffplay.exe, ffprobe.exe)
3. Drop it into the git root folder

# Project Requirement Milestone
## File formats
1. Images (png)✅ gif, bmp (WIP)
2. Audio (wav)✅ mp3, mp4 (WIP)
3. Document (txt)✅ xls, doc (WIP)

## Features
1. Image LSB (1-5 bit encoding)✅
2. Error checking (If payload is too large) - Nick
3. Encryption using password - KK
4. Add before and after encoding for file (Image, Audio, File)
5. File signature checker - Kovi

# Delgations
## Kovi
File signature checker

## Kah Kian
Password encryption

## Yu Jie
Multi-File stegnographic encoder

## Richie
GUI

## Cliff
Add additional file format support
GUI integration

## Nick
Payload size error checking
