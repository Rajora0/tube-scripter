import os
import torch
import yt_dlp
import moviepy.editor as mp
from transformers import pipeline
from flask import Flask, render_template
from flask import request, send_from_directory, jsonify


app = Flask(__name__)

# Temporary directory configuration
UPLOAD_FOLDER = 'temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Hugging Face pipeline
model_name = "openai/whisper-small"
pipe = pipeline(
    "automatic-speech-recognition",
    model=model_name,
    device=0 if torch.cuda.is_available() else -1,
)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        video_filename = download_video(url)  # Download the video first
        return render_template("index.html", video_filename=video_filename) # Pass filename, not path
    return render_template("index.html")


@app.route('/transcribe_segment', methods=['POST'])
def transcribe_segment():
    video_filename = request.form.get('video_filename')
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    segment_duration = int(request.form.get('segment_duration', 10))
    start_time = int(request.form.get('start_time', 0))

    try:
        video = mp.VideoFileClip(video_path)
        duration = video.duration

        if 0 <= start_time < duration: # Added check for valid start time
            end_time = min(start_time + segment_duration, duration)
            segment = video.subclip(start_time, end_time)

            temp_audio_file = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_segment_{start_time}.wav") 
            segment.audio.write_audiofile(temp_audio_file, codec='pcm_s16le', fps=16000)
            transcription = pipe(temp_audio_file)["text"]

            os.remove(temp_audio_file)

            return jsonify({'transcription': transcription, 'next_start_time': end_time})
        else:
            return jsonify({'transcription': '', 'next_start_time': duration})

    except Exception as e:
        print(f"Error transcribing segment: {e}")
        return jsonify({'error': f"Error transcribing segment: {str(e)}"})


def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            video_filename = os.path.basename(video_path)
            return video_filename
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None # or handle the error appropriately


@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)