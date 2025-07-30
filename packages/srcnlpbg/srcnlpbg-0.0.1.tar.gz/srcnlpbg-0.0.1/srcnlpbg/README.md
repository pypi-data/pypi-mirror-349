# srcnlpbg — Speech-to-Emotion NLP Pipeline

This Python package provides an end-to-end NLP pipeline that:

1. Transcribes audio or YouTube video using Whisper
2. Translates Bulgarian speech to English using MarianMT
3. Classifies emotions using a pre-trained BERT model
4. Outputs structured CSV and plots emotion distribution

---

## Package Structure

```
srcnlpbg/
├── transcription/transcription.py         # Whisper-based transcription
├── machine_translation/translation.py     # Bulgarian to English translation
├── inference/predictor.py                 # Emotion classification
├── output/output.py                       # CSV and plot saving
├── main.py                                # CLI entry point
```

---

## Installation

First, clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/BredaUniversityADSAI/2024-25d-fai2-adsai-group-cv3
cd srcnlpbg
poetry install
```

Make sure `ffmpeg` is installed on your system:
- Windows: https://ffmpeg.org/download.html (add `ffmpeg/bin` to PATH)
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`  

Install the package:
```bash
pip install srcnlpbg
```

---

## Usage

To run the full pipeline open a Terminal and run the following command:

```bash
poetry run python srcnlpbg/main.py
  --input_path "https://www.youtube.com/watch?v=SRdnqxV5Qoc"
  --tf_model_path "../models/tf_model"
  --emotion_model_path "../models/bert"
  --output_csv_path "../results/final_output.csv"
  --output_wav_path "../audio/temp_audio.wav"
  --output_plot "../results/emotion_distribution.png"
```

### Required Arguments

- `--input_path`: YouTube URL or local video/audio file path
- `--tf_model_path`: Path to pre-trained translation (bg-en) model folder
- `--emotion_model_path`: Path to fine-tuned BERT classifier
- `--output_csv_path`: Output CSV file (Transcription, Translation, Emotion)
- `--output_wav_path`: Intermediate `.wav` file, that gets deleted after transcription
- `--output_plot`: Path to save emotion distribution plot

---

## Publishing to PyPI

### 1. Dependencies

Example `pyproject.toml`:

```toml
[tool.poetry]
name = "srcnlpbg"
version = "0.0.1"
description = "Poetry Python package for NLP-BG project pipeline for emotion classification deployment"
authors = ["MarioVelichkov, Vladislav Stoimenov, Petar Paskalev, Raya-Neda Borisova"]
packages = [{ include = "srcnlpbg" }]
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.10,<3.11"
pandas = "2.2.3"
tensorflow = "2.10.0"
tensorflow-io-gcs-filesystem = "0.31.0"
transformers = "4.49.0"
datasets = "3.3.2"
evaluate = "0.4.3"
sentencepiece = "0.2.0"
numpy = "1.26"
scikit-learn = "1.6.1"
seaborn = "0.13.2"
matplotlib = "3.9.4"
openai-whisper = "20240930"
moviepy = "2.1.2"
pydub = "0.25.1"
pytubefix = "8.12.1"
sphinx = "7.2.6"
sphinx-autobuild = "2021.3.14"
sphinx-rtd-theme = "1.3.0"
tqdm = "^4.67.1"
typer = "^0.15.4"
rich = "^14.0.0"

torch = [
  { version = "^2.2.0", markers = "sys_platform == 'darwin'" },
  { version = "2.6.0", source = "pytorch-cu118", markers = "sys_platform != 'darwin'" }
]

torchvision = [
  { version = "^0.17.0", markers = "sys_platform == 'darwin'" },
  { version = "0.21.0", source = "pytorch-cu118", markers = "sys_platform != 'darwin'" }
]

torchaudio = [
  { version = "^2.2.0", markers = "sys_platform == 'darwin'" },
  { version = "2.6.0", source = "pytorch-cu118", markers = "sys_platform != 'darwin'" }
]

[[tool.poetry.source]]
name = "pytorch-cu118"
url = "https://download.pytorch.org/whl/cu118"
priority = "explicit"

[tool.poetry.group.dev.dependencies]
black = "^25.1.0"
flake8 = "^7.2.0"
isort = "^6.0.1"
pytest = "^8.3.5"
ipykernel = "^6.29.5"

[tool.black]
line-length = 79

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```



## 📄 License

MIT License