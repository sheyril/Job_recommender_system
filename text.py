import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

file_path='ResumeAmitKumar.pdf'

import nltk

def run_parse_resume(file_path):
    text = textract.process(file_path)
    content_list = text.splitlines()
    text = text.decode('utf-8')
    tokens = word_tokenize(text)
    punctuations = ['(',')',';',':','[',']',',', '.']
    stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    print(keywords)
    
run_parse_resume(file_path)