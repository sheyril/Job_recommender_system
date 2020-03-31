import textract
import metapy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

file_path='ResumeAbhishekPatil.pdf'

def run_parse_resume(file_path):
    # text = process_pdf(file_path)
    text = textract.process(file_path)
    # print(text)
    content_list = text.splitlines()
    # text = ' '.join(content_list)
    # print(text)
    text = text.decode('utf-8')
    tokens = word_tokenize(text)
    punctuations = ['(',')',';',':','[',']',',']
    stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    print(keywords)

run_parse_resume(file_path)