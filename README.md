# Phishing Email Detector

A machine learning web app that classifies emails as **Phishing** or **Safe** using TF-IDF and a Naive Bayes classifier.

## Features

- Paste any email text for instant prediction.
- Built with scikit-learn, NLTK, and Streamlit.
- Trained on the SMS Spam Collection (5,572 messages).

## Quick Start

Run these commands one by one:

```bash
git clone https://github.com/PAgyapong/phishing-email-detector.git
cd phishing-email-detector
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/features/preprocess.py
python src/models/train.py
streamlit run src/ui/app.py
