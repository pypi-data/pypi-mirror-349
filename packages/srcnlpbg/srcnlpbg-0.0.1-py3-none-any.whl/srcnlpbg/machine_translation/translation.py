import logging

import pandas as pd
import tensorflow as tf
from transformers import (
    AutoTokenizer,
    GenerationConfig,
    TFAutoModelForSeq2SeqLM,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set to INFO to reduce verbosity

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False


def clean_text(text: str) -> str:
    """
    Cleans a text string by removing surrounding quotes and whitespace.

    :param text: The input string to be cleaned.
    :type text: str
    :return: The cleaned string.
    :rtype: str
    """
    return text.strip().strip('"').strip("'")


def translate_sentences(transcript: list, tf_model_path: str) -> pd.DataFrame:
    """
    Translates Bulgarian sentences to English using a HuggingFace
    MarianMT model.

    :param transcript: List of dictionaries, each containing a 'text'
        field in Bulgarian.
    :type transcript: list[dict]
    :param tf_model_path: Path to the HuggingFace-style folder containing
        the model and tokenizer.
    :type tf_model_path: str
    :return: df containing the translations.
    :rtype: list
    """

    logger.info("Starting sentence translation...")

    try:
        # Load model, tokenizer, and generation config
        tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-bg-en")
        model = TFAutoModelForSeq2SeqLM.from_pretrained(tf_model_path)
        gen_config = GenerationConfig.from_pretrained(tf_model_path)
        logger.info("Tokenizer and model loaded successfully.")
    except Exception:
        logger.exception("Failed to load model or tokenizer.")
        raise

    # Use GPU if available
    device = "/GPU:0" if tf.config.list_physical_devices("GPU") else "/CPU:0"
    logger.info(f"Translation will run on device: {device}")
    translated = []

    with tf.device(device):
        for idx, sentence in enumerate(transcript):
            try:
                logger.debug(f"Translating sentence {idx+1}/{len(transcript)}")
                inputs = tokenizer(
                    clean_text(sentence["text"]),
                    return_tensors="tf",
                    padding=True,
                    truncation=True,
                )
                output = model.generate(**inputs, **gen_config.to_dict())
                sentence["Translation"] = clean_text(
                    tokenizer.decode(output[0], skip_special_tokens=True)
                )
            except Exception as e:
                logger.warning(
                    f"Failed to translate sentence at index {idx}: {e}"
                )
                sentence["Translation"] = "Translation Error"
            translated.append(sentence)

    logger.info("Translation completed.")
    logger.info(pd.DataFrame(translated).head())
    return pd.DataFrame(translated)
