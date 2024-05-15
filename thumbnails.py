import subprocess
import os
import sys
import time
import ffmpeg
from utils import float_to_duration, merge_frames_into_grid
import shutil

from os import system
system("title " + "Thumbnails Generator")

if len(sys.argv) < 2:
    print("No video file provided. Please drop a video file onto this script.")
    input("Press Enter to exit.")
    sys.exit()

input_video = sys.argv[1]
input_file_name = os.path.basename(input_video)

max_file_name_length = 100
if len(input_file_name) > max_file_name_length:
    print("File name is too long (%s+). Consider renaming." % max_file_name_length)
    input("Press Enter to exit.")
    sys.exit()

duration = float(ffmpeg.probe(input_video)["format"]["duration"])
frames = 4
desktop_path = os.path.join(os.path.expanduser('~'), "Desktop")
frames_dir = os.path.join(desktop_path, input_file_name + "_frames")
thumbnails_path = os.path.join(desktop_path, input_file_name + "_thumbs.jpg")

print("Input video:", input_video)
print("Frames:", frames)
print("Output folder:", frames_dir)
print("Output file:", thumbnails_path)

os.makedirs(frames_dir, exist_ok=True)

interval = duration / (frames + 1)
timestamps = [interval * (i + 1) for i in range(frames)]
timestamps = [float_to_duration(ts) for ts in timestamps]
frame_paths = []

for index, ts in enumerate(timestamps):
    file_name = "{:02d}.png".format(index + 1)
    frame_path = os.path.join(frames_dir, file_name)
    frame_paths.append(frame_path)
    command = ['ffmpeg', '-y', '-ss', ts, '-i', input_video, '-frames:v', '1', frame_path]
    subprocess.call(
        command, 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    print("Extracted the frame at %s as %s" % (ts, file_name))

grid_size = (2, 2)
merged_grid = merge_frames_into_grid(frame_paths, grid_size, 1920, 1080)
merged_grid.save(thumbnails_path, "jpeg", quality=90)
print("Merged frames into a grid.")

shutil.rmtree(frames_dir)
print("Removed output folder.")

print("Done")

time.sleep(2)

