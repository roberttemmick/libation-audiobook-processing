from pydub import AudioSegment
from gtts import gTTS
import glob
import os
import wave
import sys
import subprocess

root_folder = 'Books/'
processed_folder = 'Books-processed/'

# Playback variables
playback_speed = 1.25 if sys.argv[1] is None else sys.argv[1]
lang = 'en'

print('SYS', sys.path)
for subdir in os.scandir(root_folder):
    book_title = subdir.name;
    if not book_title.startswith('.'):
      print('subdir', book_title)
      # Folders containing chapter audio files and TTS announcements
      chapters_folder = f"{root_folder}{book_title}/"
      announcements_folder = f"{chapters_folder}announcements/"
      combined_folder = f"{chapters_folder}combined"

      # Ensure folders exist
      os.makedirs(announcements_folder, exist_ok=True)
      os.makedirs(f"{processed_folder}{book_title}", exist_ok=True)
      os.makedirs(f"{combined_folder}", exist_ok=True)

      # Loop through each chapter file and create an announcement, speed up the track, and combine them
      for idx, chapter_path in enumerate(sorted(glob.glob(chapters_folder + "*.mp3")), start=1):   
          chapter_name = chapter_path.replace(root_folder, '').replace(book_title, '').replace('.mp3', '')
          print('Processing INITIALIZED: ', chapter_path)
          
          # Generate TTS announcement if not already created
          announcement_path = f"{announcements_folder}{chapter_name}.mp3"
          if not os.path.exists(announcement_path):
              print('Creating Announcement file...')
              announcement_text = chapter_path.replace(root_folder, '').replace('.mp3', '')
              tts = gTTS(text=announcement_text, lang=lang)
              tts.save(announcement_path)
          print('Generate announcement files COMPLETE')

          # Load announcement and chapter audio files
          announcement_audio = AudioSegment.from_file(announcement_path)
          chapter_audio = AudioSegment.from_file(chapter_path)

          # Combine announcement with chapter audio
          print('Combining audio INITIALIZED...')
          combined_audio = announcement_audio + chapter_audio
          print('Combining audio COMPLETE')

          # Export the new file
          print('exporting combined audio...')
          combined_audio.export(f"{combined_folder}/{chapter_name}.mp3", format="mp3")

          # Speed up the chapter audio
          print('Speeding up by ' + str(playback_speed) + 'x... INITIALIZED')

          escaped_combined_folder = combined_folder.replace(' ', '\ ')
          escaped_processed_folder = processed_folder.replace(' ', '\ ')
          escaped_chapter_name = chapter_name.replace(' ', '\ ')
          escaped_book_title = book_title.replace(' ', '\ ')
          
          subprocess.run(["ffmpeg", "-i", f"{combined_folder}{chapter_name}.mp3", "-af", f"atempo={playback_speed}", f"{processed_folder}{book_title}{chapter_name}.mp3"])
          print('Speedup COMPLETE')