import logging

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ----------------------------------------
# Configure logger
# ----------------------------------------


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ----------------------------------------
# Load model and tokenizer
# ----------------------------------------


def load_emotion_model(model_path: str) -> None:
    """
    Loads a pre-trained Hugging Face emotion classification model
    and tokenizer from a local path.

    The model is moved to GPU, otherwise to CPU, and set to evaluation mode.
    Logging is used to report the status of the loading process.

    :param model_path: directory containing the tokenizer and model files.
    :type model_path: str
    :return: A tuple containing the tokenizer and the model.
    :rtype: tuple
    :raises Exception: If the model or tokenizer cannot be loaded.
    """
    logger.info(f"Loading model and tokenizer from: {model_path}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_path, local_files_only=True
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            model_path, local_files_only=True
        )

        model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        model.eval()
        logger.info("Model and tokenizer loaded successfully.")
        return tokenizer, model
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


# ----------------------------------------
# Predict emotions from a list of sentences
# ----------------------------------------
def predict_emotions(sentences: list, tokenizer: str, model: str) -> list:
    """
    Predicts emotion labels for a list of input sentences.
    Each sentence is tokenized and passed through the model.

    :param sentences: A list of input sentences to classify.
    :type sentences: list[str]
    :param tokenizer: The tokenizer corresponding to the pre-trained model.
    :type tokenizer: transformers.PreTrainedTokenizer
    :param model: The pre-trained sequence classification model.
    :type model: transformers.PreTrainedModel
    :return: A list of predicted emotion labels.
    :rtype: list[str]
    """
    device = model.device
    predictions = []

    # Normalize label_map keys to int
    label_map = (
        {int(k): v for k, v in model.config.id2label.items()}
        if hasattr(model.config, "id2label")
        else {i: str(i) for i in range(model.config.num_labels)}
    )

    logger.info(f"Running inference on {len(sentences)} sentences.")

    for sentence in sentences:
        inputs = tokenizer(
            sentence.strip(),
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=56,
        ).to(device)

        with torch.no_grad():
            logits = model(**inputs).logits
        pred = torch.argmax(logits, dim=1).item()
        predictions.append(label_map.get(pred, str(pred)))

    logger.info("Inference complete.")
    return predictions


# ----------------------------------------
# Predict emotions for a DataFrame
# ----------------------------------------


def predict_df(
    df: pd.DataFrame, tokenizer: str, model: str, save_path: str = None
) -> pd.DataFrame:
    """
    Predicts emotion labels for each sentence in the 'Translation' column.
    The function adds a new column, 'Prediction',
    with the inferred emotion labels.

    :param df: The input DataFrame containing a 'Translation' column.
    :type df: pandas.DataFrame
    :param tokenizer: The tokenizer associated with the pre-trained model.
    :type tokenizer: transformers.PreTrainedTokenizer
    :param model: The pre-trained model for emotion classification.
    :type model: transformers.PreTrainedModel
    :param save_path: Optional path to save the resulting DataFrame.
    :type save_path: str, optional
    :return: The DataFrame with an added 'Emotion' column.
    :rtype: pandas.DataFrame
    :raises ValueError: If 'Translation' column is missing
    or file format is unsupported.
    :raises Exception: If prediction or saving fails.
    """
    logger.info("Received DataFrame for prediction.")

    if "Translation" not in df.columns:
        logger.error("Missing 'Translation' column in input DataFrame.")
        raise ValueError(
            "Input DataFrame must contain a 'Translation' column."
        )

    try:
        df["Emotion"] = predict_emotions(
            df["Translation"].tolist(), tokenizer, model
        )
        logger.info("Predictions added to DataFrame.")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise

    if save_path:
        ext = save_path.lower().split(".")[-1]
        try:
            if ext == "csv":
                df.to_csv(save_path, index=False)
            elif ext in ["xls", "xlsx"]:
                df.to_excel(save_path, index=False)
            elif ext == "json":
                df.to_json(save_path, orient="records", indent=2)
            else:
                raise ValueError(f"Unsupported file format: .{ext}")
            logger.info(f"DataFrame saved to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save DataFrame: {e}")
            raise

    return df
