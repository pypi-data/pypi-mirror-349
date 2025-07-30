import argparse

import pandas as pd

from inference.predictor import load_emotion_model, predict_df
from machine_translation.translation import translate_sentences
from output.output import plot_emotion_distribution, save_df_to_csv
from transcription.transcription import process_input


def run_pipeline(
    input_path: str,
    tf_model_path: str,
    emotion_model_path: str,
    output_csv_path: str,
    output_wav_path: str,
    output_plot: str,
) -> pd.DataFrame:
    """
    Runs the full NLP pipeline: transcribes audio, translates text,
    classifies emotions, saves CSV, and optionally plots emotion distribution.

    :param input_path: Path to input audio/video file or YouTube URL.
    :type input_path: str
    :param tf_model_path: Path to the transformer translation model directory.
    :type tf_model_path: str
    :param emotion_model_path: Path to the emotion classification model.
    :type emotion_model_path: str
    :param output_csv_path: Path where the final output CSV will be saved.
    :type output_csv_path: str
    :param output_wav_path: Path of the extracted audio saved as WAV.
    :type output_wav_path: str
    :param output_plot: Optional path to save emotion distribution plot.
    :type output_plot: str or None
    :return: DF containing transcript, translation, and predicted emotions.
    :rtype: pandas.DataFrame
    """
    # Step 1: Transcribe audio to Bulgarian
    df_transcript = process_input(
        input_path, output_wav=output_wav_path, output_csv=None
    )

    # Step 2: Translate to English
    translation_input = [{"text": s} for s in df_transcript["Sentence"]]
    df_translated = translate_sentences(translation_input, tf_model_path)

    # Step 3: Load emotion model and predict
    tokenizer, model = load_emotion_model(emotion_model_path)
    df_final = predict_df(df_translated, tokenizer, model)

    # Step 4: Save to CSV
    save_df_to_csv(df_final, output_csv_path)

    # Optional: Plot emotion distribution
    plot_emotion_distribution(df_final, output_plot)

    return df_final


if __name__ == "__main__":
    """
    Parses command-line arguments and runs the NLP pipeline.
    """

    parser = argparse.ArgumentParser(
        description="Run full audio-to-emotion pipeline"
    )

    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Path to input audio/video file or YouTube URL",
    )
    parser.add_argument(
        "--tf_model_path",
        type=str,
        required=True,
        help="Path to Transformer model directory (e.g. MarianMT)",
    )
    parser.add_argument(
        "--emotion_model_path",
        type=str,
        required=True,
        help="Path to emotion classification model (e.g. BERT)",
    )
    parser.add_argument(
        "--output_csv_path",
        type=str,
        required=True,
        help="Path to save output CSV with transcripts and emotions",
    )
    parser.add_argument(
        "--output_wav_path",
        type=str,
        required=True,
        help="Path to save extracted WAV audio",
    )
    parser.add_argument(
        "--output_plot",
        type=str,
        required=False,
        default=None,
        help="Optional: Path to save emotion distribution plot",
    )
    args = parser.parse_args()

    args = parser.parse_args()

    run_pipeline(
        input_path=args.input_path,
        tf_model_path=args.tf_model_path,
        emotion_model_path=args.emotion_model_path,
        output_csv_path=args.output_csv_path,
        output_wav_path=args.output_wav_path,
        output_plot=args.output_plot,
    )
