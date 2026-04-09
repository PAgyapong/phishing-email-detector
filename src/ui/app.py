import os
import re
import joblib
import streamlit as st
import nltk

# Safely download NLTK data required for cleaning
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Text cleaning function strictly re-using the logic from our training dataset preprocessing
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Keep only alphabetic characters
    text = re.sub('[^a-zA-Z]', ' ', str(text))
    # Lowercase everything
    text = text.lower()
    # Apply tokenization, stemming and stopword removal
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words]
    return ' '.join(words)

# Streamlit aesthetic configurations
st.set_page_config(page_title="Phishing Email Detector", page_icon="🕵️", layout="centered")

def main():
    st.title("🕵️ Phishing Email Detector")
    st.markdown("Paste the content of an
email below to determine if it is 
**Phishing** or not.")
    
    # Robust path handling for both local and Streamlit Cloud
# First, try simple relative paths (works on Streamlit Cloud because working dir = repo root)
    model_path = 'models/
best_phishing_model.pkl'
    vectorizer_path = 'data/
vectorizer.joblib'

# If not found (e.g., when running locally from src/ui/ folder), fallback to absolute path from this file
    if not os.path.exists(model_path):
     base = 
  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base, 'models', 'best_phishing_model.pkl')
    vectorizer_path = os.path.join(base, 'data', 'vectorizer.joblib')

@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer
    except FileNotFoundError as e:
        st.error(f"❌ Model or Vectorizer file not found.\n\nError: {e}\n\nTried:\n- {model_path}\n- 
{vectorizer_path}")
        st.stop() 
       # stops execution here

     model, vectorizer = load_artifacts()    

    
    email_input = st.text_area("Email Content:", height=200, placeholder="e.g. You have won $10,000, click here to claim...")

    if st.button("Detect", type="primary", use_container_width=True):
        if not email_input.strip():
            st.warning("Please paste some email text you'd like to analyze first.")
        else:
            with st.spinner("Analyzing semantics & linguistics..."):
                # 1. Text Preprocessing 
                processed_text = clean_text(email_input)
                
                # 2. Vectorization (mapping text tokens to numerical weights)
                features = vectorizer.transform([processed_text])
                
                # 3. Model Prediction (0 = Safe, 1 = Phishing)
                prediction = model.predict(features)[0]
                
                st.divider()
                if prediction == 1:
                    st.error("### ⚠️ Phishing detected!")
                    st.write("This email triggered several malicious keywords and structures. Proceed with extreme caution and do not click any links!")
                else:
                    st.success("### ✅ Safe (Legitimate)")
                    st.write("Our model didn't detect any overt spoofing or phishing indicators in this block of text.")

if __name__ == '__main__':
    main()
