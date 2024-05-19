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

inputs = sys.argv[1:]

print("Found %d files" % len(inputs))

grid_size = (3, 3)
frames = grid_size[0] * grid_size[1]

print("")
print("Grid is %d × %d" % (grid_size[0], grid_size[1]))

for index, input_video in enumerate(inputs):
    
    print("")
    print("Input file: %s" % input_video)
    
    input_file_dir = os.path.dirname(input_video)
    input_file_name = os.path.basename(input_video)

    max_file_name_length = 100
    if len(input_file_name) > max_file_name_length:
        print("File name is too long (%s+). Consider renaming." % max_file_name_length)
        continue

    frames_dir = os.path.join(input_file_dir, input_file_name + "_frames")
    thumbnails_name = input_file_name + "_thumbs.jpg"
    thumbnails_path = os.path.join(input_file_dir, thumbnails_name)

    os.makedirs(frames_dir, exist_ok=True)

    duration = float(ffmpeg.probe(input_video)["format"]["duration"])
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

    merged_grid = merge_frames_into_grid(frame_paths, grid_size, 2048, 1152)
    merged_grid.save(thumbnails_path, "jpeg", quality=90)
    print("Merged frames into a grid.")

    shutil.rmtree(frames_dir)
    print("Removed output folder.")

print("")
print("Done")

time.sleep(5)

