# pip install opencv-python numpy windows-curses


#####################################################################################
# This module play mp4 video in terminal, with ascii characters
#####################################################################################
# Distribution steps
#------------------------------------------------------------------------------------
# 1. install required tools
#    > pip install setuptools wheel twine
# 2. execute setup.py
#    > python .\ascii_mp4_video_player_exp\setup.py sdist bdist_wheel
# 
# 1. You can also install the whl or gz file directly (in other machine / virtual env)
# > pip install X:\pythonProjects\distributeDemo\dist\ascii_mp4_video_player_exp-0.1-py3-none-any.whl
# OR
# > pip install X:\pythonProjects\distributeDemo\dist\ascii_mp4_video_player_exp-0.1.tar.gz
#------------------------------------------------------------------------------------
# upload them to pypi
# > twine upload dist/*
#   ...
# (in other machine / virtual env)
# > pip install simple_math_1

import cv2
import numpy as np
import curses
import time

# 16 levels of ASCII characters – high contrast for most terminals
ASCII_CHARS = [' ', '.', ':', '-', '~', '+', '=', '*', 'O', 'o', '&', '#', '@', '%', '$', 'W']

def video_frame_to_ascii(frame, term_w, term_h, term_scale=0.5):
    """
    Convert a video frame to ASCII art scaled to a % of the terminal width.
    """
    height, width, _ = frame.shape
    aspect_ratio = height / width

    # scale based on terminal width × term_scale
    new_width = int(term_w * term_scale)
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for char aspect ratio

    if new_width < 10 or new_height < 5:
        return "Window too small."

    resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # fix: cast to float32 before scaling to avoid overflow
    gray = gray.astype(np.float32)
    brightness_indices = (gray * (len(ASCII_CHARS) - 1) / 255).astype(np.uint8)

    chars = np.take(ASCII_CHARS, brightness_indices)
    return "\n".join("".join(row) for row in chars)


def draw_frame(stdscr, ascii_frame):
    """Draw ASCII frame at top-left of screen without flicker."""
    stdscr.clear()

    try:
        for y, line in enumerate(ascii_frame.split('\n')):
            stdscr.addstr(y, 0, line)
    except curses.error:
        pass 

    stdscr.refresh()


def init_and_play(stdscr, cap, delay, term_scale):
    """Main loop for drawing frames."""
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)  # non-blocking input

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        term_h, term_w = stdscr.getmaxyx()

        # pass terminal size + term_scale to control actual output size
        ascii_frame = video_frame_to_ascii(frame, term_w, term_h, term_scale=term_scale)

        draw_frame(stdscr, ascii_frame)
        time.sleep(delay)

        # 'q' to quit
        if stdscr.getch() == ord('q'):
            break


def play_ascii_video(video_path, fps=24, term_scale=0.5):
    """Main function to start ASCII video playback."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    delay = 1.0 / fps

    try:
        curses.wrapper(init_and_play, cap, delay, term_scale)
    except Exception as e:
        print(f"Playback error: {e}")
    finally:
        cap.release()
        print("Video playback ended.")


if __name__ == "__main__":
    # video downloaded from: https://www.pexels.com/zh-cn/video/855401/   
    mp4_file = r"D:\Users\paul\Pictures\pexel_855401-uhd_3840_2160_25fps.mp4"

    # play ascii video 
    play_ascii_video(mp4_file, fps=30, term_scale=0.5)  # Now this really scales to 30% of terminal width

