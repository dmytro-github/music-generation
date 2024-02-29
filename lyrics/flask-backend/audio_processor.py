import logging
import subprocess
import sys
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import make_chunks
import wave
import google_api
import os

# Define global constants
CHANGE_RATE = 0.98  # Rate to slow down the audio (lower is slower)
CHUNK_LENGTH_MS = 10000  # Length of audio chunks in milliseconds

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def separate_audio(filename):
    # Set MODEL_PATH environment variable if models are in a custom location
    os.environ['MODEL_PATH'] = '/path/to/your/models'

    python_command = 'python3' if sys.platform != 'win32' else 'python'
    input_path = Path('uploads') / filename
    output_path = 'converted'

    command = [python_command, '-m', 'spleeter', 'separate', '-i', str(input_path), '-o', output_path]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Spleeter separation successful: %s", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Spleeter command failed: %s", e.stderr)
        return False
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        return False


def slow_down_audio(filename):
    filename_without_ext = Path(filename).stem
    slowed_vocals_path = Path('converted') / filename_without_ext / 'slowed_vocals.wav'
    vocals_path = Path('converted') / filename_without_ext / 'vocals.wav'

    try:
        with wave.open(str(vocals_path), 'rb') as audio_file:
            params = audio_file.getparams()
            frames = audio_file.readframes(-1)

        new_params = params._replace(framerate=int(params.framerate * CHANGE_RATE))

        with wave.open(str(slowed_vocals_path), 'wb') as slowed_audio_file:
            slowed_audio_file.setparams(new_params)
            slowed_audio_file.writeframes(frames)
    except Exception as e:
        logging.error("Failed to slow down audio: %s", e)

def audio_to_chunks(filename):
    filename_without_ext = Path(filename).stem
    slowed_vocals_path = Path('converted') / filename_without_ext / 'slowed_vocals.wav'
    output_dir = Path('converted') / filename_without_ext

    try:
        myaudio = AudioSegment.from_file(str(slowed_vocals_path), "wav")
        chunks = make_chunks(myaudio, CHUNK_LENGTH_MS)

        for i, chunk in enumerate(chunks):
            chunk_name = f"{i}_chunk.wav"
            logging.info("Exporting %s", chunk_name)
            chunk.export(output_dir / chunk_name, format="wav")
    except Exception as e:
        logging.error("Error during audio chunking: %s", e)

def chunks_to_text(filename):
    filename_without_ext = Path(filename).stem
    directory = Path('converted') / filename_without_ext
    result_text = {}

    try:
        chunks = [file for file in directory.iterdir() if 'chunk' in file.name and file.suffix == '.wav']
        chunks.sort(key=lambda file: int(file.stem.split("_")[0]))

        for chunk in chunks:
            try:
                response = google_api.transcribe_file(str(chunk), chunk.stem)
                if response:
                    result_text[chunk.stem] = {"text": response[0], "confidence": response[1]}
                else:
                    result_text[chunk.stem] = {"text": "", "confidence": 0}
            except Exception as e:
                logging.error("Failed to transcribe chunk %s: %s", chunk.name, e)
                result_text[chunk.stem] = {"text": "", "confidence": 0}

    except Exception as e:
        logging.error("Failed to organize chunks for transcription: %s", e)

    return result_text
