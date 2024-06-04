import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import hashlib
import os
from datetime import datetime 
import math
stop_words = {
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

additional_stop_words = ['@', '.', ',', '”', '\'', '“', ';', ':', '-', "and"]


def clean_query(query):
    words = word_tokenize(query)
    stemmed_words = [stemmer.stem(word) for word in words]
    filtered_stem_words = [word.lower() for word in stemmed_words if word not in stop_words and word.isalnum()]
    return filtered_stem_words

def hash_to_bucket(word):
    hash_object = hashlib.sha256(word.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    return f'barrel_{hash_value % 4000}'




def load_inverted_index(inverted_index_directory, barrel):
    inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
    with open(inverted_index_path, 'r') as json_file:
        return json.load(json_file)
    
    
def calculate_tf_idf(inverted_index_directory, query):
    # Step 1: Calculate TF for each word in the query for each URL
    tf_scores = {}
    for word in query:
        
        # print("printing the word")
        # print(word)
        # input("Press Enter to continue...")
        # print("proceded with word", word)
        barrel = hash_to_bucket(word)
        inverted_index=load_inverted_index(inverted_index_directory,barrel)

        if word in inverted_index:
            print("barrel ",barrel)
            print("word",word)
            for entry in inverted_index[word]:
                url = entry['u']
                frequency = entry['f']
                if url not in tf_scores:
                    tf_scores[url] = {}
                tf_scores[url][word] = frequency
       

    # Step 2: Calculate IDF for each word
    idf_scores = {}
    total_documents = 150000
    for word in query:
        # print("printing the word")
        # print(word)
        # input("Press Enter to continue...")
        # print("proceded with word", word)
        barrel = hash_to_bucket(word)
        inverted_index=load_inverted_index(inverted_index_directory,barrel)

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

    url_frequencies = {}
    common_urls=set()
    all_urls=set()
    # Initialize a dictionary to store positions for each URL
    url_positions = {}
    query=query.split()
    print("the query after the split is ",query)
    for word in query:
        # Determine the barrel for the word based on the first character
        print("words will appear here")
        print(word)
        

        
        barrel = hash_to_bucket(word)
        # print(barrel)
        # Load the inverted index only if the barrel is relevant
        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_barrel_{barrel}.json')
            print("printing the barrel",(barrel))
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)

                # Check if the word is in the inverted index
                if word in inverted_index:
                    word_info = inverted_index[word]
                    # Extract URLs for the current word
                    urls = {entry['u'] for entry in word_info}
                    all_urls=all_urls.union(urls)
                    # If common_urls is empty, set it to the current URLs, else take the intersection
                    common_urls = common_urls.intersection(urls) if common_urls else urls
    return all_urls

# def searchfinal(query):
#     print ("the query is ",query)
#     time=datetime.now()
#     inverted_index_directory = r'E:\salmandsa\invertedindexdirectory'
#     cleaned_query=clean_query(query)
#     print("the cleaned query is",cleaned_query) 
#     print("the common urls are")
#     url_frequencies = {}
#     common_urls=set()
#     all_urls=set()
#     # Initialize a dictionary to store positions for each URL
#     url_positions = {}
#     query=query.split()
#     print("the query after the split is ",query)
#     for word in query:
#         # Determine the barrel for the word based on the first character
#         print("words will appear here")
#         print(word)
        

        
#         barrel = hash_to_bucket(word)
#         # print(barrel)
#         # Load the inverted index only if the barrel is relevant
#         if barrel != 'other_barrel':
#             inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
#             print("path is ",inverted_index_path)
#             print("printing the barrel",(barrel))
#             with open(inverted_index_path, 'r') as json_file:
#                 inverted_index = json.load(json_file)
#                 print("opened the file sucessfully")
#                 # Check if the word is in the inverted index
#                 if word in inverted_index:
#                     print("entered the word in the inverted index")
#                     word_info = inverted_index[word]
#                     # Extract URLs for the current word
#                     urls = {entry['u'] for entry in word_info}
#                     all_urls=all_urls.union(urls)
#                     # If common_urls is empty, set it to the current URLs, else take the intersection
#                     common_urls = common_urls.intersection(urls) if common_urls else urls
#                     all_urls=all_urls.union(urls)
#                     print("printing the all urls ",all_urls)
#     return all_urls
#     print(common_urls)
#     result = calculate_tf_idf(inverted_index_directory, cleaned_query)
#     print("the result from the seconf function ")
#     print(result)
#     return result
def searchfinal(query):
    inverted_index_directory = r'E:\salmandsa\invertedindexdirectory'
    lexicon_file_path = r"E:\salmandsa\lexicon.json"
    print("The query is", query)
    time = datetime.now()
    cleaned_query = clean_query(query)
    print("The cleaned query is", cleaned_query)
    
    url_frequencies = {}
    common_urls = set()
    all_urls = set()
    
    # Initialize a dictionary to store positions for each URL
    url_positions = {}
    query_words = query.split()
    print("The query after the split is", query_words)
    
    for word in query_words:
        barrel = hash_to_bucket(word)
        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            try:
                with open(inverted_index_path, 'r') as json_file:
                    inverted_index = json.load(json_file)
                    if word in inverted_index:
                        word_info = inverted_index[word]
                        urls = {entry['u'] for entry in word_info}
                        all_urls = all_urls.union(urls)
                        common_urls = common_urls.intersection(urls) if common_urls else urls
            except FileNotFoundError:
                continue

    url_mapping = {}
    try:
        with open(lexicon_file_path, 'r') as lexicon_file:
            lexicon = json.load(lexicon_file)
            url_mapping = {str(v): k for k, v in lexicon.items()}
    except FileNotFoundError:
        print("Lexicon file not found.")
    
    result_urls = {url_mapping.get(str(num), num) for num in all_urls}
    print(result_urls)
    return list(result_urls)