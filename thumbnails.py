import subprocess
import os
import sys
import ffmpeg
from utils import float_to_duration

from os import system
system("title " + "Thumbnails Generator")

if len(sys.argv) < 2:
    print("No video file provided. Please drop a video file onto this script.")
    input("Press Enter to exit.")
    sys.exit()

input_video = sys.argv[1]
input_filename = os.path.basename(input_video)
duration = float(ffmpeg.probe(input_video)["format"]["duration"])
frames = 4
desktop_path = os.path.join(os.path.expanduser('~'), "Desktop")
frames_dir = os.path.join(desktop_path, input_filename[:50].rstrip(".") + "_frames")

print("Input video:", input_video)
print("Frames:", frames)
print("Output folder:", frames_dir)

os.makedirs(frames_dir)

interval = duration / (frames + 1)
timestamps = [interval * (i + 1) for i in range(frames)]
timestamps = [float_to_duration(ts) for ts in timestamps]

for index, ts in enumerate(timestamps):
    file_name = "{:02d}.png".format(index + 1)
    frame_path = os.path.join(frames_dir, file_name);
    command = ['ffmpeg', '-ss', ts, '-i', input_video, '-frames:v', '1', frame_path]
    subprocess.call(
        command, 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    print("Extracted the frame at %s as %s" % (ts, file_name))

print("Done")

input()
