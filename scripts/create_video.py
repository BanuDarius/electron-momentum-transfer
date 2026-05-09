'''MIT License

Copyright (c) 2026 Banu Darius-Matei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import os
import sys
import subprocess
from pathlib import Path
import scripts.common as common
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"
OUTPUT_VIDEO_DIR = PROJECT_ROOT / "output-video"

# ----------------------------------------------------------------------- #

def create_2d_colormap_video(method, framerate, axis_horiz, axis_vert, axis_p):
    axis_text_horiz = common.get_axis_text(axis_horiz)
    lowercase_text_horiz = axis_text_horiz.lower()
    
    axis_text_vert = common.get_axis_text(axis_vert)
    lowercase_text_vert = axis_text_vert.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-colormap-{mode}-{lowercase_text_horiz}{lowercase_text_vert}{lowercase_text_p}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-colormap-{mode}-{lowercase_text_horiz}{lowercase_text_vert}{lowercase_text_p}.mp4"
    
    arguments = ["ffmpeg", "-r", framerate, "-i", images_path, "-s", "1600:1600", "-c:v", "libx264", "-b:v", "12M", "-pix_fmt", "yuv420p", "-y", "-loglevel", "error", video_path]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit()
        
    print(f"Created 2D colormap animation for {method} mode.")

# ----------------------------------------------------------------------- #

def create_phase_video(method, framerate, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-phase-space-{mode}-{lowercase_text_pos}{lowercase_text_p}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-phase-space-{mode}-{lowercase_text_pos}{lowercase_text_p}.mp4"
    
    arguments = ["ffmpeg", "-r", framerate, "-i", images_path, "-s", "1600:1600", "-c:v", "libx264", "-b:v", "12M", "-pix_fmt", "yuv420p", "-y", "-loglevel", "error", video_path]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit()
        
    print(f"Created phase space animation for {method} mode.")

# ----------------------------------------------------------------------- #

def create_time_momentum_video(method, framerate, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    images_path = f"{OUTPUT_IMAGE_DIR}/out-time-momentum-{mode}-{lowercase_text_pos}{lowercase_text_p}-%d.png"
    video_path = f"{OUTPUT_VIDEO_DIR}/out-time-momentum-{mode}-{lowercase_text_pos}{lowercase_text_p}.mp4"
    
    arguments = ["ffmpeg", "-r", framerate, "-i", images_path, "-s", "1600:1600", "-c:v", "libx264", "-b:v", "12M", "-pix_fmt", "yuv420p", "-y", "-loglevel", "error", video_path]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit()
        
    print(f"Created time-momentum animation for {method} mode.")

# ----------------------------------------------------------------------- #