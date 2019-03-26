import glob
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

stop = stopwords.words('english')

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

phone_data = {}
email_data = {}
name_data = {}

#for files whose names are formatted like C:\\my_files\name_100.txt
#makes a dictionary entry for every file ie. "name":[email1@gmail.com...]

for filename in glob.glob('my_files/*.txt'):
    with open(filename, 'r', encoding="utf-8") as myfile:
        string=myfile.read().replace('\n', '')
        name = filename.split('\\')
        length = len(name[1])
        name = (name[1][:length-4]).split('_')[0]
        phone_data[name] = extract_phone_numbers(string)
        print("processing",name,"numbers")
        email_data[name] = extract_email_addresses(string)
        print("processing",name,"emails")
        name_data[name] = extract_names(string)
        print("processing",name,"names")
