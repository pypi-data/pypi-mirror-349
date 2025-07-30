import os
import sys
import tempfile
import time
import threading
import argparse
from yt_dlp import YoutubeDL
from ffpyplayer.player import MediaPlayer
from youtubesearchpython import VideosSearch
import msvcrt
import logging # Import the logging module

is_paused = False
is_running = True
stop_event = threading.Event()

# Custom logger to suppress warnings from yt-dlp
class YTDLQuietLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        # Prevent default handlers from adding logs to stderr
        self.propagate = False

    def debug(self, msg):
        pass # Ignore debug messages

    def warning(self, msg):
        # You can choose to log these to a file or just ignore them completely
        # For full suppression, simply pass
        pass
        # If you wanted to log them silently to a file:
        # with open('yt-dlp_warnings.log', 'a') as f:
        #     f.write(f"WARNING: {msg}\n")

    def error(self, msg):
        # You might still want to see errors, or log them
        # For full suppression, simply pass
        pass
        # print(f"Error from yt-dlp: {msg}") # Or print to console if critical

# Instantiate your custom logger
ytdl_logger = YTDLQuietLogger('yt_dlp_quiet')

def search_youtube(query):
    print("Loading...")
    results = VideosSearch(query, limit=1).result()
    if not results['result']: # Added error handling as discussed previously
        print(f"No results found for '{query}'.")
        return None
    video_url = results['result'][0]['link']
    return video_url

def download_audio_tempfile(video_url):
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, 'song.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': temp_file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': ytdl_logger, # <--- IMPORTANT: Use your custom logger here
        'noplaylist': True, # Good practice for single video downloads
        'noprogress': True, # Suppress progress bar during download
        'no_warnings': True, # Also explicitly tell yt-dlp to suppress warnings
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True) # Ensure download=True for downloading
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        filename = base + ".mp3"
    return filename

def user_input_controller(player):
    global is_paused
    print("Controls: [p] pause, [r] resume, [q] quit")

    while not stop_event.is_set():
        if msvcrt.kbhit():
            key = msvcrt.getwch().lower()
            if key == 'p' and not is_paused:
                player.set_pause(True)
                is_paused = True
                print("Paused")
            elif key == 'r' and is_paused:
                player.set_pause(False)
                is_paused = False
                print("Resumed")
            elif key == 'q':
                stop_event.set()
                player.close_player()
                print("Quitting...")
                break
        time.sleep(0.1)

def play_audio_file(file_path):
    player = MediaPlayer(file_path)
    controller_thread = threading.Thread(target=user_input_controller, args=(player,))
    controller_thread.start()

    while not stop_event.is_set():
        frame, val = player.get_frame()

        if val == 'eof':
            print("Playback finished.")
            stop_event.set()  # signal controller to stop
            break

        if val == 'paused':
            time.sleep(0.1)
        elif frame is None:
            time.sleep(0.01)

    player.close_player()
    controller_thread.join()

def install_dependencies():
    import subprocess
    print("Installing required libraries...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "yt-dlp", "ffpyplayer", "Youtube-python"])
        print("Setup complete. You can now play songs, e.g., 'song your favorite track'.") # Improved message
    except subprocess.CalledProcessError as e:
        print(f"Error during dependency installation: {e}")
        print("Please ensure you have Python and pip installed correctly.")

def main():
    parser = argparse.ArgumentParser(description="Play a song from YouTube or install dependencies")
    parser.add_argument('--setup', action='store_true', help="Install all required dependencies")
    parser.add_argument('song', nargs='*', help="Song name to search and play")
    args = parser.parse_args()

    if args.setup:
        install_dependencies()
        return

    if not args.song:
        print("Usage: song <song name> OR song --setup")
        return

    query = ' '.join(args.song)
    url = search_youtube(query)
    if url is None: # Handle no search results
        return

    file_path = download_audio_tempfile(url)
    if not file_path: # Handle potential download failure if no usable format was found
        print("Failed to download audio file.")
        return

    print(f"Playing: {os.path.basename(file_path)}") # Print just the filename, not full temp path
    try:
        play_audio_file(file_path)
    except Exception as e:
        print("Error while playing:", e)
    finally: # Ensure cleanup even if playback errors
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print("Cleaned up audio file.")
            except PermissionError:
                print("Could not delete audio file. Try manually removing:", file_path)
        stop_event.clear() # Clear event for next run if script were to loop
