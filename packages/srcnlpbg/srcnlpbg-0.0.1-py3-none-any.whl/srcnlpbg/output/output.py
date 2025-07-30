import logging

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def save_df_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Saves a DataFrame to a CSV file.

    :param df: The DataFrame to save.
    :type df: pandas.DataFrame
    :param output_path: Path to save the CSV file.
    :type output_path: str
    """
    try:
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        logger.info(f"Saved DataFrame to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save DataFrame: {e}")
        raise


def plot_emotion_distribution(
    df: pd.DataFrame, output_path: str = "output"
) -> None:
    """
    Plots a bar chart of the emotion distribution based on a DataFrame column.

    This function visualizes the frequency of each unique value in the
    'Emotion' column of the provided DataFrame using a bar plot.

    :param df: A pandas DataFrame that must include an 'Emotion' column.
    :type df: pd.DataFrame

    :raises ValueError: If the 'Emotion' column is not in the DataFrame.

    :return: None
    :rtype: None
    """

    if "Emotion" not in df.columns:
        logger.error("Missing 'Emotion' column in input CSV.")
        raise ValueError("CSV file must contain an 'Emotion' column.")

    emotion_counts = df["Emotion"].value_counts()

    logger.info("Plotting emotion distribution bar chart.")
    emotion_counts.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.title("Emotion Distribution")
    plt.xlabel("Emotion")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Saved emotion distribution plot to {output_path}")
    plt.close()
