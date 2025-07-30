import logging
import os

import pandas as pd
import torch
import whisper
from pydub import AudioSegment
from pytubefix import YouTube

# -----------------------------
# LOGGING CONFIGURATION
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


# -----------------------------
# CONFIGURATION
# -----------------------------


# Supported file formats
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".ogg"]

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------


def clean_text(text: str) -> str:
    """
    Strips quotes and whitespace from a string.

    :param text: Text to be cleaned.
    :type text: str
    :return: Cleaned text string.
    :rtype: str
    """

    cleaned = text.strip().strip('"').strip("'")
    logger.debug(f"Cleaned text: '{text}' -> '{cleaned}'")
    return cleaned


def check_gpu() -> bool:
    """
    Checks whether a CUDA-enabled GPU is available for PyTorch.

    :return: True if a GPU is available, False otherwise.
    :rtype: bool
    """
    available = torch.cuda.is_available()
    logger.debug(f"GPU available: {available}")
    return available


def is_youtube_url(input_path: str) -> bool:
    """
    Checks if the input string is a YouTube URL.

    :param input_path: Input path or URL.
    :type input_path: str
    :return: True if input is a YouTube link.
    :rtype: bool
    """
    result = "youtube.com" in input_path or "youtu.be" in input_path
    logger.debug(f"Checked YouTube URL: {input_path} -> {result}")
    return result


def is_supported_file(input_path: str) -> bool:
    """
    Checks whether the file extension is a supported audio or video format.

    :param input_path: File path.
    :type input_path: str
    :return: True if format is supported.
    :rtype: bool
    """
    ext = os.path.splitext(input_path)[1].lower()
    result = ext in SUPPORTED_VIDEO_FORMATS or ext in SUPPORTED_AUDIO_FORMATS
    logger.debug(
        f"Checked format: {ext} -> {'supported' if result else 'unsupported'}"
    )
    return result


# -----------------------------
# STEP 1: DOWNLOAD/PREPARE AUDIO
# -----------------------------


def download_audio(youtube_link: str, output_path: str) -> str:
    """
    Downloads a YouTube video's audio and converts it to WAV format.

    :param youtube_link: YouTube video URL.
    :type youtube_link: str
    :param output_path: File path to save the extracted WAV audio.
    :type output_path: str
    :return: Path to the saved WAV audio file.
    :rtype: str
    """
    logger.info("Step 1: Downloading video and extracting audio...")
    logger.debug(f"Downloading from URL: {youtube_link}")

    yt = YouTube(youtube_link)
    stream = yt.streams.filter(only_audio=True).first()

    # Download as .mp4 (default behavior)
    downloaded_file = stream.download(
        output_path=os.path.abspath("../audio/"), filename="temp_download.mp4"
    )
    logger.debug(f"Downloaded file: {downloaded_file}")

    # Convert to .wav using pydub
    logger.info(f"Reading Mp4 File to path: {downloaded_file}")
    audio = AudioSegment.from_file("../audio/temp_download.mp4", format="mp4")
    abs_path = os.path.abspath(output_path)
    logger.info(f"Saving Wav File to path: {abs_path}")
    audio.export(abs_path, format="wav")
    logger.debug(f"Exported audio to WAV: {output_path}")

    # Clean up
    os.remove(downloaded_file)
    logger.debug("Temporary download file removed.")
    return output_path


def extract_audio_from_video(video_path: str, output_path: str) -> str:
    """
    Extracts audio from a local video file and saves it as WAV.

    :param video_path: Path to the video file.
    :type video_path: str
    :param output_path: Path to save the extracted audio file.
    :type output_path: str
    :return: Path to the extracted WAV file.
    :rtype: str
    """
    logger.info("Step 1: Extracting audio from video...")
    logger.debug(f"Input video path: {video_path}")
    audio = AudioSegment.from_file(video_path)
    audio.export(output_path, format="wav")
    logger.debug(f"Exported audio to WAV: {output_path}")
    return output_path


def prepare_audio(input_path: str, output_path: str) -> None:
    """
    Prepares an audio file from various input sources (YouTube, video, audio).

    :param input_path: YouTube URL or local file path.
    :type input_path: str
    :param output_path: Path to save the output WAV file.
    :type output_path: str
    :return: Path to the processed audio file.
    :rtype: str
    :raises ValueError: If the input format is unsupported.
    """
    logger.info("Preparing audio...")
    logger.debug(f"Input path: {input_path}, Output path: {output_path}")
    if is_youtube_url(input_path):
        return download_audio(input_path, output_path)
    elif is_supported_file(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext in SUPPORTED_AUDIO_FORMATS:
            logger.debug("No audio conversion needed.")
            return input_path  # No conversion needed
        return extract_audio_from_video(input_path, output_path)
    else:
        logger.error("Unsupported input format.")
        raise ValueError(
            "Unsupported input format. Supported formats: "
            "                 YouTube URLs, "
            + ", ".join(SUPPORTED_VIDEO_FORMATS + SUPPORTED_AUDIO_FORMATS)
        )


# -----------------------------
# STEP 2: TRANSCRIBE AUDIO
# -----------------------------


def transcribe_audio(
    audio_path: str, output_csv: str = None, language: str = "bg"
) -> pd.DataFrame:
    """
    Transcribes speech from an audio file using Whisper
    and saves results to CSV.

    :param audio_path: Path to the input audio file.
    :type audio_path: str
    :param output_csv: Optional path to save the transcription CSV.
    :type output_csv: str or None
    :param language: Language code for transcription (default is "bg").
    :type language: str
    :return: DF with transcription including start time, end time and sentence.
    :rtype: pandas.DataFrame
    """
    logger.info("Step 2: Transcribing audio...")
    logger.debug(f"Audio path: {audio_path}, Language: {language}")

    # Check for GPU availability
    use_gpu = check_gpu()
    device = "cuda" if use_gpu else "cpu"
    logger.info(f"Using {'GPU' if use_gpu else 'CPU'} for transcription...")

    # Load model
    model = whisper.load_model("large").to(device)
    logger.debug("Whisper model loaded.")

    # Transcribe audio
    result = model.transcribe(audio_path, language=language)
    segments = result["segments"]
    logger.debug(f"Number of segments found: {len(segments)}")

    # Format results exactly as in the pipeline.py
    data = []
    for seg in segments:
        start = pd.to_datetime(seg["start"], unit="s").strftime("%H:%M:%S,%f")[
            :-3
        ]
        end = pd.to_datetime(seg["end"], unit="s").strftime("%H:%M:%S,%f")[:-3]
        sentence = clean_text(seg["text"])
        logger.debug(f"Segment: {start} --> {end} | {sentence}")
        data.append([start, end, sentence])

    # Create DataFrame with same column names as pipeline.py
    df = pd.DataFrame(data, columns=["Start Time", "End Time", "Sentence"])

    # Save to CSV if requested
    if output_csv:
        logger.info(f"Saving transcription to {output_csv}...")
        df.to_csv(output_csv, index=False)

    return df


# -----------------------------
# MAIN FUNCTION
# -----------------------------


def process_input(
    input_path: str, output_csv: str, output_wav: str, cleanup: bool = True
) -> pd.DataFrame:
    """
    Handles full pipeline: prepares audio, transcribes it, and saves results.

    :param input_path: YouTube URL or path to video/audio file.
    :type input_path: str
    :param output_csv: File path to save the transcription output CSV.
    :type output_csv: str
    :param cleanup: Whether to delete temporary audio files after processing.
    :type cleanup: bool
    :return: Transcription result as a DataFrame.
    :rtype: pandas.DataFrame
    :raises Exception: For any error encountered in the processing pipeline.
    """
    logger.info("Starting full processing pipeline...")
    logger.debug(
        f"Input: {input_path}, Output CSV: {output_csv}, Cleanup: {cleanup}"
    )

    try:
        # Step 1: Prepare audio
        audio_path = prepare_audio(input_path, output_path=output_wav)
        logger.debug(f"Prepared audio file at: {audio_path}")

        # Step 2: Transcribe
        df = transcribe_audio(audio_path, output_csv=output_csv)

        # Cleanup
        if (
            cleanup and audio_path != input_path
        ):  # Only remove if it's a temporary file
            os.remove(audio_path)
            logger.debug(f"Temporary audio file {audio_path} removed.")

        logger.info("Transcription complete!")
        if output_csv:
            logger.info(f"Results saved to: {output_csv}")
        logger.info(f"Number of segments: {len(df)}")
        return df

    except Exception:
        logger.exception(
            "Error during processing. Please check input format and try again."
        )
        raise
