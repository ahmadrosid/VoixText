import moviepy.editor as mp
import whisper
import argparse
import os

def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    video.close()

def transcribe_audio(audio_path, language=None):
    model = whisper.load_model("base")
    
    if language:
        result = model.transcribe(audio_path, language=language)
    else:
        result = model.transcribe(audio_path)
    
    return result["text"]

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio from a video file.")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("-l", "--language", help="Language code for transcription (e.g., 'en' for English, 'es' for Spanish)")
    args = parser.parse_args()

    video_path = args.video_path
    language = args.language

    if not os.path.isfile(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    audio_path = "extracted_audio.wav"

    print('Extracting audio from video...')
    extract_audio(video_path, audio_path)

    print('Start transcribing audio...')
    transcript = transcribe_audio(audio_path, language=language)

    print("\nTranscription:\n")
    print(transcript)

    # Clean up the temporary audio file
    os.remove(audio_path)

if __name__ == "__main__":
    main()