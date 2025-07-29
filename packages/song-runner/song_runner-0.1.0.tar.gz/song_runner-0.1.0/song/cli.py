import os
import sys
import tempfile
import time
import threading
import argparse
from yt_dlp import YoutubeDL
from ffpyplayer.player import MediaPlayer
from youtubesearchpython import VideosSearch

is_paused = False
is_running = True

def search_youtube(query):
    print("Loading...")
    results = VideosSearch(query, limit=1).result()
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
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        filename = base + ".mp3"
    return filename

def user_input_controller(player):
    global is_running, is_paused
    print("Controls: type [p] to pause, [r] to resume, [q] to quit")
    while is_running:
        command = input(">>> ").strip().lower()
        if command == 'p' and not is_paused:
            player.set_pause(True)
            is_paused = True
            print("Paused")
        elif command == 'r' and is_paused:
            player.set_pause(False)
            is_paused = False
            print("Resumed")
        elif command == 'q':
            is_running = False
            player.close_player()
            print("Quitting...")
            break
        else:
            print("Unknown command. Use p, r, or q.")

def play_audio_file(file_path):
    global is_running
    player = MediaPlayer(file_path)
    controller_thread = threading.Thread(target=user_input_controller, args=(player,))
    controller_thread.start()

    while is_running:
        frame, val = player.get_frame()
        if val == 'eof':
            is_running = False
            break
    player.close_player()
    controller_thread.join()
    time.sleep(1)

def install_dependencies():
    import subprocess
    print("Installing required libraries...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
        "yt-dlp", "ffpyplayer", "youtube-search-python"])
    print("Setup complete.")

def main():
    global is_running

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
    file_path = download_audio_tempfile(url)
    print(f"Playing: {file_path}")

    try:
        play_audio_file(file_path)
    except Exception as e:
        print("Error while playing:", e)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print("Cleaned up audio file.")
        except PermissionError:
            print("Could not delete audio file. Try manually removing:", file_path)

    is_running = True
