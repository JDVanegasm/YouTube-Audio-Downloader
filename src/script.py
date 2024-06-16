from pytube import YouTube
from moviepy.editor import *
import os
import tempfile

def download_wav_audio(url, download_address, progress_callback=None):
    """Downloads audio from YouTube and converts it to WAV format"""
    try:
        # Download the YouTube video
        yt = YouTube(url, on_progress_callback=progress_callback)
        stream = yt.streams.filter(only_audio=True).first()
        if stream is None:
            raise Exception("No audio stream found.")

        # Log debug message for the download start
        print(f"Downloading audio from URL: {url}")

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_filename = temp_file.name
            stream.download(filename=temp_filename)
            print(f"Temporary file created: {temp_filename}")

        # Ensure the directory for the download address exists
        download_directory = os.path.dirname(download_address)
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
            print(f"Created directory: {download_directory}")

        # Convert the audio file to WAV format
        try:
            # Open the audio file with AudioFileClip
            audio_clip = AudioFileClip(temp_filename)
            print(f"Audio clip loaded: {audio_clip}")

            # Write the audio file to WAV format
            audio_clip.write_audiofile(download_address + ".wav")
            print(f"Audio file saved to: {download_address}.wav")
        except Exception as e:
            raise Exception(f"Error converting audio: {e}")
        finally:
            # Ensure the temporary file is closed and then remove it
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                    print(f"Temporary file removed: {temp_filename}")
                except PermissionError as e:
                    print(f"Error removing temporary file: {e}")
    except Exception as e:
        raise Exception(f"Error downloading or processing audio: {e}")