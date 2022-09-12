import os
from moviepy.editor import *
import tqdm
import csv

# Location of lip syncer
api = r"C:\Users\junru\Downloads\Rhubarb-Lip-Sync-1.13.0-Windows\Rhubarb-Lip-Sync-1.13.0-Windows\rhubarb.exe"  # Location of rhubarb.exe
options = ["-o", "mouth.csv"]  # Options for rhubarb
audio = input("Enter the name of the lip input: ")  # Input file name # Audio file name
if not audio == ".csv":  # Type .csv to bypass rhubarb and use previous run 
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

master = None # I feel bad for my memory

for i in tqdm(range(0, EOF - 1)):
    # Read img from dictionary
    img = faces[stamps[i][1]]
    # Create clip with time of s[i] to s[i+1]
    clip = ImageClip(img).set_duration(float(stamps[i+1][0]) - float(stamps[i][0]))
    if master is None:
        master = clip
    else:
        master = concatenate_videoclips([master, clip], method="compose")

# Add background
final_clip = CompositeVideoClip([ColorClip(size=(1240, 1754), color=(255, 255, 255), duration=float(stamps[-1][0])), master, ImageClip("littleguy/littleguy.PNG").set_duration(float(stamps[-1][0]))])
# Add audio ?
yn = input("Would you like to add audio to the video \"y/n\"")
if yn.upper() == "Y" and not audio == ".csv":
    final_clip = final_clip.set_audio(AudioFileClip(audio))
final_clip.write_videofile("output.mp4", fps=24)