# import nltk
import re
import random
import string


class Tagger:
    def __init__(self, file_path):
        self.tags = set()
        self.load_tags(file_path)

    def load_tags(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                normalized_tag = self.normalize(line.strip())
                self.tags.add(normalized_tag)

    def clean_text(self, text):
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+|ftp://\S+', '', text)
        
        # Sanitize hashtags
        text = text.replace("#", "")

        # Handle mentions by removing them
        text = re.sub(r'@\w+', '', text)

        # Remove emojis
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        
        # Remove punctuation except for hyphens and pipes
        allowed = set('-|')
        punctuation = ''.join(ch for ch in string.punctuation if ch not in allowed)
        text = text.translate(str.maketrans('', '', punctuation))
        
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text.lower()

    def normalize(self, text):
        text = self.clean_text(text)
        return text.strip()

    def tag_string(self, input_string):
        tokens = self.normalize(input_string).split()

        matched_tags = set([token for token in tokens if token in self.tags])

        return ", ".join(matched_tags)
    
    def random_sentence(subtitle):
        sentence = subtitle.split(" ... ")
        sentence = random.choice(sentence)

        sentence = re.sub(r'\s+', ' ', sentence).strip()
        return sentence.lower()
