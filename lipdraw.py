import os
from moviepy.editor import *
import csv

# Location of lip syncer
api = r"C:\Users\junru\Downloads\Rhubarb-Lip-Sync-1.13.0-Windows\Rhubarb-Lip-Sync-1.13.0-Windows\rhubarb.exe"  # Location of rhubarb.exe
options = ["-o", "mouth.csv"]  # Options for rhubarb
audio = input("Enter the name of the lip input: ")  # Input file name # Audio file name
os.system(api + " " + audio + " " + " ".join(options))  # Run rhubarb

# A, B, C, D, E, F, G, H, X
# TODO create images
faces = {
    'A': "littleguy/A.PNG", 'B': "littleguy/B.PNG", 'C': "littleguy/C.PNG", 'D': "littleguy/D.PNG", 'E': "littleguy/E.PNG", 'F': "littleguy/E.PNG",
     'G': "littleguy/G.PNG", 'H': "littleguy/H.PNG", "X": "littleguy/X.PNG"} # dictionary of faces # Pretend we have a bunch of faces
stamps = [] # Time stamps

# Read from file
with open("mouth.csv", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter="\t")
    for row in reader:
        stamps.append((row[0], row[1])) # Get rid of the decimal
EOF = len(stamps)

clips = [] # I feel bad for my memory
for i in range(0, EOF - 1):
    # Read img from dictionary
    img = faces[stamps[i][1]]
    # Create clip with time of s[i] to s[i+1]
    clip = ImageClip(img).set_duration(float(stamps[i+1][0]) - float(stamps[i][0]))
    clips.append(clip)

# Create video
final_clip = concatenate_videoclips(clips, method="compose")
# Add background
final_clip = CompositeVideoClip([ColorClip(size=(1240, 1754), color=(255, 255, 255), duration=float(stamps[-1][0])), final_clip, ImageClip("littleguy/littleguy.PNG").set_duration(float(stamps[-1][0]))])
# Add audio
final_clip = final_clip.set_audio(AudioFileClip(audio))
final_clip.write_videofile("output.mp4", fps=30)