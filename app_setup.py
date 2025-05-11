import nltk

def download_nltk_resources():
    """Download required NLTK resources"""
    resources = [
        'punkt',
        'stopwords',
        'vader_lexicon'
    ]
    
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")

if __name__ == "__main__":
    download_nltk_resources()
