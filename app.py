from flask import Flask, render_template, request, send_file
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "audios"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    output_name = request.form['name']
    
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    audio_path = download_youtube_audio(video_url, DOWNLOAD_FOLDER)
    final_audio = convert_to_wav(audio_path, output_name)
    os.remove(audio_path)  # Remover o arquivo original de áudio baixado
    
    return send_file(final_audio, as_attachment=True)

def download_youtube_audio(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    audio_path = stream.download(output_path)
    return audio_path

def convert_to_wav(audio_path, output_name):
    audio_clip = AudioFileClip(audio_path)
    output_wav_path = os.path.join(os.path.dirname(audio_path), f"{output_name}.wav")
    audio_clip.write_audiofile(output_wav_path, codec='pcm_s16le')
    return output_wav_path

if __name__ == "__main__":
    app.run(debug=True)