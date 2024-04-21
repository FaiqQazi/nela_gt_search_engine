import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
# from nltk.corpus import stopwords
import timeit
import hashlib


import os
stopwords = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
    'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
    "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
    "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}
stemmer = SnowballStemmer("english")
stop_words = stopwords
additional_stop_words = ['@', '.', ',', '”', '\'', '“', ';', ':', '-', "and"]
stop_words.update(additional_stop_words)

def clean_query(query):
    words = word_tokenize(query)
    stemmed_words = [stemmer.stem(word) for word in words]
    filtered_stem_words = [word.lower() for word in stemmed_words if word not in stop_words and word.isalnum()]
    cleaned_query = ' '.join(filtered_stem_words)
    return cleaned_query

def hash_to_barrel(word):
    hash_object = hashlib.sha256(word.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    return f'barrel_{hash_value % 4000}'


import math

def calculate_tf_idf(inverted_index_directory, query):
    # Step 1: Calculate TF for each word in the query for each URL
    tf_scores = {}
    for word in query.split():
        print("printing the word")
        print(word)
        input("Press Enter to continue...")
        print("proceded with word", word)
        # first_two_chars = word[:2].lower() if word else None
        barrel = hash_to_barrel(word)

        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)
                print(barrel)
        if word in inverted_index:
            for entry in inverted_index[word]:
                url = entry['u']
                frequency = entry['f']
                if url not in tf_scores:
                    tf_scores[url] = {}
                tf_scores[url][word] = frequency

    # Step 2: Calculate IDF for each word
    idf_scores = {}
    total_documents = 150000
    for word in query.split():
        print("printing the word")
        print(word)
        input("Press Enter to continue...")
        print("proceded with word", word)
        # first_two_chars = word[:2].lower() if word else None
        barrel = hash_to_barrel(word)

        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)
                print(barrel)
        if word in inverted_index:
            documents_containing_word = len(inverted_index[word])
            idf_scores[word] = math.log(total_documents / (1 + documents_containing_word))

    # Step 3: Calculate TF-IDF scores for each URL
    tf_idf_scores = {}
    for url, tf_values in tf_scores.items():
        score = 0
        for word, tf in tf_values.items():
            if word in idf_scores:
                score += tf * idf_scores[word]
        tf_idf_scores[url] = score

    # Step 4: Sort URLs based on their TF-IDF scores
    sorted_urls = sorted(tf_idf_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_urls

def search_inverted_indices(query, inverted_index_directory):
    # Initialize a dictionary to store URLs and their frequencies
    words=query.split(" ")
    url_frequencies = {}
    common_urls=set()

    # Initialize a dictionary to store positions for each URL
    url_positions = {}

    for word in words:
        # Determine the barrel for the word based on the first character
        # print(word)
        

        # first_two_chars = word[:2].lower() if word else None
        # print(first_two_chars)
        barrel=hash_to_barrel(word) 
        # print(barrel)
        # Load the inverted index only if the barrel is relevant
        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)

                # Check if the word is in the inverted index
                if word in inverted_index:
                    word_info = inverted_index[word]
                    # Extract URLs for the current word
                    urls = {entry['u'] for entry in word_info}
                    # If common_urls is empty, set it to the current URLs, else take the intersection
                    common_urls = common_urls.intersection(urls) if common_urls else urls
    return common_urls

def search_inverted_indices_when_common_urls_not_present(query, inverted_index_directory):
    # Initialize a dictionary to store URLs and their frequencies
    words=query.split(" ")
    url_frequencies = {}
    common_urls=set()

    # Initialize a dictionary to store positions for each URL
    url_positions = {}

    for word in words:
        # Determine the barrel for the word based on the first character
        # print(word)
        

        # first_two_chars = word[:2].lower() if word else None
        # print(first_two_chars)
        barrel=hash_to_barrel(word) 
        # print(barrel)
        # Load the inverted index only if the barrel is relevant
        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)

                # Check if the word is in the inverted index
                if word in inverted_index:
                    word_info = inverted_index[word]
                    # Extract URLs for the current word
                    urls = {entry['u'] for entry in word_info}
                    # If common_urls is empty, set it to the current URLs, else take the intersection
                    # common_urls = common_urls.intersection(urls) if common_urls else urls
    return urls


query = "event in saudi arabia"
inverted_index_directory = r'E:\salmandsa\invertedindexdirectory'
common_urls = search_inverted_indices(query, inverted_index_directory)
result = calculate_tf_idf(inverted_index_directory, query)
json_file_path = r'E:\salmandsa\url_list.json'

# Open and read the JSON file
with open(json_file_path, 'r') as file:
    # Load JSON data
    data = json.load(file)

    # Assuming the JSON file contains an array
    # if isinstance(data, list):
    #     # Print the array
    #     print("Array in the JSON file:")
    #     # print(data)
    # else:
    #     print("The JSON file does not contain an array.")


# Print URLs with their TF-IDF scores in sorted order
s=0
print("printing the common urls")
# print(common_urls)
for url, score in result:
    if(s%300==0):
        input("Press Enter to continue...")
    if(url in common_urls):
        print(f"URL: {data[url]}\tScore: {score}")
        s+=1
if(s==0):
    urls=search_inverted_indices_when_common_urls_not_present(query, inverted_index_directory)
    result = calculate_tf_idf(inverted_index_directory, query)
    for url, score in result:
        # if(s%300==0):
        #     input("Press Enter to continue...")
        if(url in urls):
            print(f"URL: {url}\tScore: {score}")
            s+=1
print("printing the size of the array")
print(len(data))