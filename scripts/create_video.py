import os
import sys
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"
OUTPUT_VIDEO_DIR = PROJECT_ROOT / "output-video"

def create_2d_colormap_video(method, framerate):
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    imagesPath = f"{OUTPUT_IMAGE_DIR}/out-colormap-{mode}-%d.png"
    videoPath = f"{OUTPUT_VIDEO_DIR}/out-colormap-{mode}.mp4"
    os.system(f"ffmpeg -r {framerate} -i {imagesPath} -s 1200:1200 -c:v libx264 -pix_fmt yuv420p -y -loglevel error {videoPath}")
    print(f"Created 2D colormap animation for {method} mode.")

def create_error_video(framerate):
    imagesPath = f"{OUTPUT_IMAGE_DIR}/out-errors-%d.png"
    videoPath = f"{OUTPUT_VIDEO_DIR}/out-errors.mp4"
    os.system(f"ffmpeg -r {framerate} -i {imagesPath} -s 1200:1200 -c:v libx264 -pix_fmt yuv420p -y -loglevel error {videoPath}")
    print("Created error animation.")