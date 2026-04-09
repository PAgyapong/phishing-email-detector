import os
import re
import pandas as pd
import numpy as np
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, 'data')
    
    input_path = os.path.join(data_dir, 'raw_emails.csv')
    cleaned_path = os.path.join(data_dir, 'cleaned_emails.csv')
    x_path = os.path.join(data_dir, 'X_features.npy')
    y_path = os.path.join(data_dir, 'y_labels.npy')
    vectorizer_path = os.path.join(data_dir, 'vectorizer.joblib')

    # Ensure required NLTK data is downloaded
    print("Ensuring NLTK stopwords are downloaded...")
    nltk.download('stopwords', quiet=True)
    
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    
    # Drop rows with missing text or labels
    df = df.dropna(subset=['text', 'label'])
    
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    def clean_text(text):
        # 1. Remove non-alphabetic characters
        text = re.sub('[^a-zA-Z]', ' ', str(text))
        # 2. Convert to lowercase
        text = text.lower()
        # 3. Apply stemming and remove stopwords
        words = text.split()
        words = [stemmer.stem(w) for w in words if w not in stop_words]
        return ' '.join(words)
        
    print("Cleaning text data. This may take a moment...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    print(f"Saving cleaned emails to: {cleaned_path}")
    df[['label', 'cleaned_text']].to_csv(cleaned_path, index=False)
    
    print("Vectorizing text features with TF-IDF...")
    # Limiting max_features to 5000 to keep the dense array size reasonable
    vectorizer = TfidfVectorizer(max_features=5000) 
    X = vectorizer.fit_transform(df['cleaned_text'])
    
    # Map labels back to numerical representation if they are strings (1 for phishing, 0 for safe)
    if df['label'].dtype == object:
        df['label_encoded'] = df['label'].map({'phishing': 1, 'safe': 0})
        # If there are different string types, fallback to generic category
        if df['label_encoded'].isnull().any():
            df['label_encoded'] = df['label'].astype('category').cat.codes
    else:
        df['label_encoded'] = df['label']

    y = df['label_encoded'].values
    
    print(f"Saving model features to: {x_path} and {y_path}")
    np.save(x_path, X.toarray())
    np.save(y_path, y)
    
    print(f"Saving TF-IDF vectorizer to: {vectorizer_path}")
    joblib.dump(vectorizer, vectorizer_path)
    
    print("\nPreprocessing complete!")
    print(f"Feature matrix shape: {X.shape}")

if __name__ == '__main__':
    main()
