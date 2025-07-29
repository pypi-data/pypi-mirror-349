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
# upload them to pypi (register from https://pypi.org, get API token)
# > twine upload dist/*
#   ...
#   https://pypi.org/project/ascii-mp4-video-player-exp/0.15
#
# (in other machine / virtual env)
# > pip install simple_math_1


import cv2
import numpy as np
import curses
import time
import os

ASCII_CHARS = [
    ' ', '·', '.', ':', '-', '+', '=', '*', 'O', 'o', 'I',
    'i', '?', '!', '[', ']', '{', '}', '(', ')', '<', '>',
    'v', 'x', 'X', '&', '#', '%', '$', '@', 'M', 'W'
]

def video_frame_to_ascii(frame, term_w, term_h, term_scale=0.5):
    height, width, _ = frame.shape
    aspect_ratio = height / width

    new_width = int(term_w * term_scale)
    new_height = int(aspect_ratio * new_width * 0.55)

    if new_width < 10 or new_height < 5:
        return "Window too small."

    resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    gray = gray.astype(np.float32)
    brightness_indices = (gray * (len(ASCII_CHARS) - 1) / 255).astype(np.uint8)

    chars = np.take(ASCII_CHARS, brightness_indices)
    return "\n".join("".join(row) for row in chars)

def format_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def draw_frame(stdscr, ascii_frame, status, progress_footer):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    try:
        for y, line in enumerate(ascii_frame.split('\n')):
            if y >= h - 1:
                break
            stdscr.addstr(y, 0, line)

        # Footer
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(h - 1, 0, progress_footer.ljust(w - 1))
        stdscr.attroff(curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()

def init_and_play(stdscr, cap, video_fps, term_scale, loop_on):
    curses.curs_set(0)
    stdscr.nodelay(True)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_duration = total_frames / video_fps if video_fps > 0 else 0

    paused = False
    current_frame = 0
    status = "Playing"
    loop = loop_on
    should_quit = False

    while True:
        # Read the current frame only if not paused
        if not paused:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if not ret:
                if loop:
                    current_frame = 0
                    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                    ret, frame = cap.read()
                    if not ret:
                        break
                else:
                    break
        else:
            # When paused, keep displaying the current frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()

        term_h, term_w = stdscr.getmaxyx()
        ascii_frame = video_frame_to_ascii(frame, term_w, term_h, term_scale=term_scale)

        current_time = current_frame / video_fps if video_fps > 0 else 0
        loop_status = "Loop On" if loop else "Loop Off"
        progress_footer = f"[{status}] {format_time(current_time)}/{format_time(total_duration)} | [{loop_status}]"

        draw_frame(stdscr, ascii_frame, status, progress_footer)

        key = stdscr.getch()
        delay = 1.0 / video_fps if video_fps > 0 else 1.0 / 30

        # Handle 'q' to quit immediately
        if key == ord('q') or key == ord('Q'):
            should_quit = True
            break

        # Handle spacebar to toggle pause/resume
        elif key == ord(' '):
            paused = not paused
            status = "Paused" if paused else "Playing"

        # Handle loop toggle
        elif key == ord('l') or key == ord('L'):
            loop = not loop

        # Handle seeking backward
        elif key == curses.KEY_LEFT:
            step = max(int(0.01 * total_frames), int(video_fps * 5))
            current_frame = max(0, current_frame - step)
            paused = False
            status = "Playing"

        # Handle seeking forward
        elif key == curses.KEY_RIGHT:
            step = max(int(0.01 * total_frames), int(video_fps * 5))
            current_frame = min(total_frames - 1, current_frame + step)
            paused = False
            status = "Playing"

        # Advance frame only if not paused
        if not paused:
            current_frame += 1
            status = "Playing"
            if current_frame >= total_frames and not loop:
                break
            elif current_frame >= total_frames and loop:
                current_frame = 0

        time.sleep(delay)

    return should_quit  # Return only should_quit to control outer loop

def play_ascii_video(video_path, fps=30, term_scale=0.8, loop=False):
    if not os.path.exists(video_path):
        print(f"Error: File not found - {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    video_fps = cap.get(cv2.CAP_PROP_FPS) or fps

    try:
        should_quit = curses.wrapper(init_and_play, cap, video_fps, term_scale, loop)
        if should_quit:
            print("Video playback ended.")
            return
        if not loop:
            print("Video playback ended.")
            return
        print("Restarting video (loop mode)...")
        # Recursively call to restart video if loop is True and not quitting
        play_ascii_video(video_path, fps, term_scale, loop)
    except Exception as e:
        print(f"Playback error: {e}")
    finally:
        cap.release()

if __name__ == "__main__":
    # video downloaded from: https://www.pexels.com/zh-cn/video/855401/   
    mp4_file = r"D:\Users\paul\Pictures\pexels_855401-uhd_3840_2160_25fps.mp4"

    # Controls:
    # - Space: Pause/Resume
    # - ← Left Arrow: Seek Backward
    # - → Right Arrow: Seek Forward
    # - L: Toggle Loop Mode
    # - Q: Quit

    play_ascii_video(mp4_file, fps=30, term_scale=0.5, loop=True)