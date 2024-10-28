## YouTube Video Downloader and Transcriber

This project provides a web application that downloads YouTube videos and transcribes their audio content using the Whisper speech recognition model.  The application utilizes Flask for the backend and HTML, CSS, and Javascript for the frontend.


### Project Structure

```
└── 📁 templates
    └── 📄 index.html
└── 📄 app.py
└── 📄 requirements.txt
```

* **`templates/index.html`**: The HTML template for the user interface.  Handles user input, displays the video player, and shows the transcription.
* **`app.py`**: The main Flask application file.  Handles video downloads using `yt-dlp`, audio extraction using `moviepy`, transcription using the `transformers` library's Whisper model, and serving the video and handling AJAX requests.
* **`requirements.txt`**: Lists the necessary Python packages for the project.


### Setup and Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This installs Flask, yt-dlp, transformers, torch, and moviepy.

2. **Run the Application:**
   ```bash
   python app.py
   ```
   This starts the Flask development server.

3. **Access the Application:** Open your web browser and go to `http://127.0.0.1:5000/` (or the port specified if you changed it).


### Usage

1. **Enter YouTube URL:** Paste the URL of the YouTube video you want to download and transcribe into the provided input field.

2. **Process Video:** Click the "Process" button. The application will download the video, extract the audio, and then transcribe the audio using the Whisper model. This may take some time depending on the video length.

3. **View Video and Transcription:** The video will be displayed, along with a continuously updating transcription of the audio.  You can adjust the transcription segment length (in seconds) to control the processing speed and memory usage.

### Notes

* The application uses a temporary directory (`temp`) to store downloaded videos and intermediate files.  These files will be deleted after processing.
* The transcription accuracy depends on the audio quality of the YouTube video and the Whisper model's capabilities.
*  Ensure you have a stable internet connection for downloading the video.
* Error handling is implemented to catch potential issues during video download and transcription.  Error messages will be displayed to the user.
*  The `transformers` library requires a CUDA-enabled GPU for optimal performance; otherwise, it will fall back to CPU processing, which can be significantly slower.


###  Further Development

This project could be extended with features such as:

* **Improved UI:**  A more sophisticated and user-friendly interface.
* **Multiple Language Support:**  Support for transcription in languages other than English (requires different Whisper models).
* **Progress Indicators:**  Display progress bars to show the download and transcription status.
* **Download Transcription:** Add a feature to download the transcription as a text file.
* **Advanced Audio Processing:** Incorporate audio preprocessing techniques to improve transcription accuracy.


This documentation provides a clear and concise guide to setting up, running, and using the YouTube video downloader and transcriber application.  Remember to consult the documentation for the libraries used (Flask, yt-dlp, transformers, moviepy) for more advanced usage and customization.
