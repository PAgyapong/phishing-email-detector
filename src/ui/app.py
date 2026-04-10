import streamlit as st
import joblib
import os
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('stopwords', quiet=True)

# Text cleaning function
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text.lower())
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words]
    return ' '.join(words)

st.set_page_config(page_title="Phishing Email Detector", page_icon="🕵️ ", 
layout="centered")

def main():
    st.title("🕵️  Phishing Email Detector")
    st.markdown("Paste the content of an email below to determine if it is **Phishing** or not.")

    # Path handling: try relative first, fallback to absolute
    model_path = 'models/best_phishing_model.pkl'
    vectorizer_path = 'data/vectorizer.joblib'

    if not os.path.exists(model_path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base, 'models', 'best_phishing_model.pkl')
        vectorizer_path = os.path.join(base, 'data', 'vectorizer.joblib')

    @st.cache_resource
    def load_artifacts():
        try:
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            return model, vectorizer
        except FileNotFoundError as e:
            st.error("❌ Model or Vectorizer file not found.\n\nError: " + str(e) + "\n\nTried:\n- " + model_path + "\n- " + vectorizer_path)
            st.stop()

    model, vectorizer = load_artifacts()

    email_input = st.text_area("Email Content:", height=200, placeholder="e.g. You have won $1,000,000...")
    if st.button("Detect", type="primary", use_container_width=True):
        if not email_input.strip():
            st.warning("Please paste some email text.")
        else:
            with st.spinner("Analyzing..."):
                processed = clean_text(email_input)
                vec = vectorizer.transform([processed])

                pred = model.predict(vec)[0]
                     if pred ==1:
                        st.error("🎣 PHISHING DETECTED")
                     else:
                        st.success("✅ SAFE EMAIL")


if __name__ == "__main__":
    main()
