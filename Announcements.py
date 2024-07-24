#!/usr/bin/env python3

import sounddevice as sd
import numpy as np
import sys
import time
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
log_file_path = './Announcement.log'
threshold = 50
max_wait = 300
def log_message(message):
    print(message)
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

def rms_level(data):
    return np.sqrt(np.mean(np.square(data)))

def play_sound(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

def analyze_audio(file_path, wait_seconds, threshold, device_index):
    start_time = time.time()
    total_start_time = time.time()
    total_time = time.time()
    levels = []
    last_below_threshold_time = None

    # Initialize sounddevice input stream
    with sd.InputStream(device=device_index, channels=1, samplerate=44100, callback=lambda indata, frames, time_info, status: levels.append(rms_level(indata) * 1000)):
        while True:
            # Wait for 1 second
            time.sleep(1)
            
            # Calculate average RMS level for the past second
            if levels:
                avg_level = np.mean(levels)
                levels.clear()

                # Calculate elapsed time
                elapsed_time = time.time() - start_time
                total_time = time.time() - total_start_time
                if total_time > max_wait: 
                    log_message(f"{now} \033[31m Terminated - Max wait elapsed\033[0m")
                    break

                if avg_level > threshold:
                    log_message(f"\t-> [{int(elapsed_time):03d}s / {int(total_time):03d}s] - Avg RMS: [{int(round(avg_level, 0)):03d}/{threshold}] \033[31mABOVE, resetting timer\033[0m")
                    last_below_threshold_time = None
                    start_time = time.time()  # Restart timer

                else:
                    log_message(f"\t-> [{int(elapsed_time):03d}s / {int(total_time):03d}s] - Avg RMS: [{int(round(avg_level, 0)):03d}/{threshold}] \033[32mBELOW\033[0m")
                    if last_below_threshold_time is None:
                        last_below_threshold_time = time.time()

                    elapsed_below_threshold = time.time() - last_below_threshold_time

                    if elapsed_below_threshold >= wait_seconds:
                        log_message(f"Elapsed Time: {elapsed_time:.1f}s | Total Time: {total_time:.1f}s - \033[32mCondition met. Playing sound...\033[0m")
                        play_sound(file_path)
                        xnow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        log_message(f"{now} \033[32mComplete {sound_file}\033[0m")
                        break

            # Exit after the specified duration if not condition met
            if elapsed_time >= wait_seconds and last_below_threshold_time is None:
                log_message(f"Elapsed Time: {elapsed_time:.1f}s | Total Time: {total_time:.1f}s - Duration elapsed. Exiting.")
                break

# Main function to handle command-line arguments and call the analysis function
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: Announcements.py <sound_file> <seconds> <device_index>")
        sys.exit(1)

    sound_file = sys.argv[1]
    wait_seconds = int(sys.argv[2])
    device_index = int(sys.argv[3])

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message(f"{now} Announcements.py {sound_file} {wait_seconds} {device_index} threshold={threshold}")
    analyze_audio(sound_file, wait_seconds, threshold, device_index)