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
    images_path = f"{OUTPUT_IMAGE_DIR}/out-colormap-{mode}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-colormap-{mode}.mp4"
    os.system(f"ffmpeg -r {framerate} -i {images_path} -s 1200:1200 -c:v libx264 -preset slower -pix_fmt yuv420p -y -loglevel error {video_path}")
    print(f"Created 2D colormap animation for {method} mode.")

def create_error_video(framerate):
    images_path = f"{OUTPUT_IMAGE_DIR}/out-errors-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-errors.mp4"
    os.system(f"ffmpeg -r {framerate} -i {images_path} -s 1200:1200 -c:v libx264 -preset slower -pix_fmt yuv420p -y -loglevel error {video_path}")
    print("Created error animation.")

def create_enter_exit_video(method, framerate):
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-{mode}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-enter-exit-time-{mode}.mp4"
    os.system(f"ffmpeg -r {framerate} -i {images_path} -s 1200:1200 -c:v libx264 -preset slower -pix_fmt yuv420p -y -loglevel error {video_path}")
    print("Created enter exit time animation.")

def create_phase_video(method, framerate):
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-phase-space-{mode}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-phase-space-{mode}.mp4"
    os.system(f"ffmpeg -r {framerate} -i {images_path} -s 1200:1200 -c:v libx264 -preset slower -pix_fmt yuv420p -y -loglevel error {video_path}")
    print(f"Created phase space animation for {method} mode.")