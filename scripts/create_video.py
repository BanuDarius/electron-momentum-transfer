import os
import sys
import subprocess
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"
OUTPUT_VIDEO_DIR = PROJECT_ROOT / "output-video"

# ----------------------------------------------------------------------- #

def get_axis_text(axis):
    if(axis == 0):
        axis_text = "X"
    elif(axis == 1):
        axis_text = "Y"
    else:
        axis_text = "Z"
    return axis_text
    
def get_lowercase_text(axis):
    text = get_axis_text(axis).lower()
    return text

# ----------------------------------------------------------------------- #

def create_2d_colormap_video(method, framerate, axis_horiz, axis_vert, axis_p):
    axis_text_horiz = get_axis_text(axis_horiz)
    lowercase_text_horiz = axis_text_horiz.lower()
    
    axis_text_vert = get_axis_text(axis_vert)
    lowercase_text_vert = axis_text_vert.lower()
    
    axis_text_p = get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-colormap-{mode}-{lowercase_text_horiz}{lowercase_text_vert}{lowercase_text_p}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-colormap-{mode}-{lowercase_text_horiz}{lowercase_text_vert}{lowercase_text_p}.mp4"
    
    arguments = ["ffmpeg", "-r", framerate, "-i", images_path, "-s", "1200:1200", "-c:v", "libx264", "-b:v", "12M", "-pix_fmt", "yuv420p", "-y", "-loglevel", "error", video_path]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
        
    print(f"Created 2D colormap animation for {method} mode.")

# ----------------------------------------------------------------------- #

def create_phase_video(method, framerate, axis_pos, axis_p):
    axis_text_pos = get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-phase-space-{mode}-{lowercase_text_pos}{lowercase_text_p}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-phase-space-{mode}-{lowercase_text_pos}{lowercase_text_p}.mp4"
    
    arguments = ["ffmpeg", "-r", framerate, "-i", images_path, "-s", "1200:1200", "-c:v", "libx264", "-b:v", "12M", "-pix_fmt", "yuv420p", "-y", "-loglevel", "error", video_path]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
        
    print(f"Created phase space animation for {method} mode.")

# ----------------------------------------------------------------------- #

def create_time_momentum_video(method, framerate, axis_pos, axis_p):
    axis_text_pos = get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-time-momentum-{mode}-{lowercase_text_pos}{lowercase_text_p}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-time-momentum-{mode}-{lowercase_text_pos}{lowercase_text_p}.mp4"
    
    arguments = ["ffmpeg", "-r", framerate, "-i", images_path, "-s", "1200:1200", "-c:v", "libx264", "-b:v", "12M", "-pix_fmt", "yuv420p", "-y", "-loglevel", "error", video_path]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
        
    print(f"Created time-momentum animation for {method} mode.")

# ----------------------------------------------------------------------- #