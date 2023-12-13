import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
# from nltk.corpus import stopwords

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

def get_barrel(char):
    if 'a' <= char <= 'z':
        return f'barrel_{ord(char) - ord("a")}'
    elif '0' <= char <= '9':
        return 'numeric_barrel'
    else:
        return 'other_barrel'
    
def get_metadata(url, metadata):
    # Search for the metadata corresponding to the given URL
    for entry in metadata:
        if entry["url"] == url:
            return entry
    return None


# def search_inverted_indices(query, inverted_index_directory):
#bheeme bheeme 
#     # Initialize a set to store common URLs
#     common_urls = set()

#     for word in query:
#         # Determine the barrel for the word based on the first character
#         first_char = word[0].lower() if word else None
#         barrel = get_barrel(first_char)

#         # Load the inverted index only if the barrel is relevant
#         if barrel != 'other_barrel':
#             inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
#             with open(inverted_index_path, 'r') as json_file:
#                 inverted_index = json.load(json_file)


#                 # Check if the word is in the inverted index
#                 if word in inverted_index:
#                     word_info = inverted_index[word]
#                     # Extract URLs for the current word
#                     urls = {entry['url'] for entry in word_info}
#                     # If common_urls is empty, set it to the current URLs, else take the intersection
#                     common_urls = common_urls.intersection(urls) if common_urls else urls

#     return list(common_urls)
# def search_inverted_indices(query, inverted_index_directory):
#     # Initialize a dictionary to store URLs and their frequencies
#     url_frequencies = {}

#     for word in query:
#         # Determine the barrel for the word based on the first character
#         first_char = word[0].lower() if word else None
#         barrel = get_barrel(first_char)

#         # Load the inverted index only if the barrel is relevant
#         if barrel != 'other_barrel':
#             inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
#             with open(inverted_index_path, 'r') as json_file:
#                 inverted_index = json.load(json_file)

#                 # Check if the word is in the inverted index
#                 if word in inverted_index:
#                     word_info = inverted_index[word]

#                     # Update URL frequencies
#                     for entry in word_info:
#                         url = entry['url']
#                         frequency = entry['frequency']
#                         if url in url_frequencies:
#                             url_frequencies[url] += frequency
#                         else:
#                             url_frequencies[url] = frequency

#     # Sort URLs based on total frequency in descending order
#     sorted_urls = sorted(url_frequencies.items(), key=lambda x: x[1], reverse=True)

#     return [url for url, _ in sorted_urls]

# import os
# import json

# def get_barrel(first_char):
#     # Implement the logic for determining the barrel based on the first character
#     # This function is not provided, so you need to define it according to your needs
#     pass

# def search_inverted_indices(query, inverted_index_directory):
#     # Initialize a dictionary to store URLs and their frequencies
#     url_frequencies = {}

#     # Initialize a dictionary to store positions for each URL
#     url_positions = {}

#     for word_index, word in enumerate(query):
#         # Determine the barrel for the word based on the first character
#         first_char = word[0].lower() if word else None
#         barrel = get_barrel(first_char)

#         # Load the inverted index only if the barrel is relevant
#         if barrel != 'other_barrel':
#             inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
#             with open(inverted_index_path, 'r') as json_file:
#                 inverted_index = json.load(json_file)

#                 # Check if the word is in the inverted index
#                 if word in inverted_index:
#                     word_info = inverted_index[word]

#                     # Update URL frequencies and positions
#                     for entry in word_info:
#                         url = entry['url']
#                         frequency = entry['frequency']
#                         positions = entry['positions']

#                         if url in url_frequencies:
#                             # Update frequency score
#                             url_frequencies[url] += frequency

#                             # Update positions for the URL
#                             if url in url_positions:
#                                 url_positions[url].append(positions)
#                             else:
#                                 url_positions[url] = [positions]

#                         else:
#                             # Initialize scores for a new URL
#                             url_frequencies[url] = frequency
#                             url_positions[url] = [positions]

#     # Sort URLs based on total frequency in descending order
#     sorted_urls = sorted(url_frequencies.items(), key=lambda x: x[1], reverse=True)

#     # Extract positions for each URL from the url_positions dictionary
#     url_positions_result = {url: positions for url, positions in url_positions.items()}

#     return [url for url, _ in sorted_urls], url_positions_result

import os
import json
def get_barrel(chars):
    # Combine the two characters to form a two-letter string
    char = chars.lower()  # Ensure lowercase for consistency

    # Check if the combined string is alphabetic
    if char.isalpha() and len(char) == 2:
        # Calculate a unique barrel number based on the ASCII values of the two characters
        barrel_number = ((ord(char[0]) - ord("a"))* 26) + (ord(char[1]) - ord("a")) 
        # Check if the barrel number is within the expected range
        if 0 <= barrel_number <= 675:
            return f'barrel_{barrel_number}'
    elif char.isdigit():
        # Numbers stored in numeric barrels
        return 'numeric_barrel'
    # Other characters in other barrels
    return 'other_barrel'

def calculate_score(frequency, positions):
    # Flatten the list of positions
    flat_positions = [pos for sublist in positions for pos in sublist]

    # Count the number of ones resulting from the differences of consecutive numbers
    ones_count = sum(1 for i, j in zip(flat_positions, flat_positions[1:]) if j - i == 1)

    # Calculate the score based on frequency and ones count
    score = frequency + ones_count
    return score


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
        

        first_two_chars = word[:2].lower() if word else None
        # print(first_two_chars)
        barrel = get_barrel(first_two_chars)
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
                    urls = {entry['url'] for entry in word_info}
                    # If common_urls is empty, set it to the current URLs, else take the intersection
                    common_urls = common_urls.intersection(urls) if common_urls else urls

    # Sort URLs based on total score (frequency + ones count) in descending order
    # sorted_urls = sorted(url_frequencies.items(), key=lambda x: calculate_score(x[1], url_positions[x[0]]), reverse=True)

    # # Extract positions for each URL from the url_positions dictionary
    # url_positions_result = {url: positions for url, positions in url_positions.items()}

    # return [url for url, _ in sorted_urls], url_positions_result
    return common_urls
def search_inverted_indices_lite(query, inverted_index_directory):
    words = query.split(" ")
    url_frequencies = {}
    url_positions = {}

    for word in words:
        # print("printing the word")
        # print(word)
        # input("Press Enter to continue...")
        # print("proceded with word", word)
        first_two_chars = word[:2].lower() if word else None
        barrel = get_barrel(first_two_chars)

        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)
                # print(barrel)
                if word in inverted_index:
                    word_info = inverted_index[word]
                    # print(word)
                    print("now working on this word")
                    # input("Press Enter to continue...")
                    for entry in word_info:
                        url = entry['url']
                        frequency = entry['frequency']
                        positions = entry['positions']
                        if url not in url_frequencies:
                            url_frequencies[url] = 0

                        url_frequencies[url] += frequency

                        if url in url_positions:
                            # Update positions for the URL with word information
                            if url in url_positions:
                                # Update positions for the URL with word information
                                if url_positions[url].get(word):
                                    url_positions[url][word].extend(positions)
                                else:
                                    url_positions[url][word] = positions
                            else:
                                url_positions[url] = {word: positions}
                        else:
                            url_positions[url] = {word: positions}

    return url_frequencies, url_positions

def rank_and_print_urls(sorted_urls, url_positions_result):
    # Print the sorted URLs based on the calculated score
    print("\nRanked URLs based on score:")
    for url in sorted_urls:
        print("url")
        print("Positions:")
        positions = url_positions_result[url[0]]
        for position in positions:
            print(position)
        print(f"Frequency: {url[1]}")
        print(f"Score: {calculate_score(url[1], positions)}")

# Example usage
# query="middle east booming"
# print(query)
# print(query)
# query=clean_query(query)
# print(query)
# input("Press Enter to continue...")
def thesearch(query):
        
    inverted_index_directory = r'E:\salmandsa\DSA_Project\inverted_index_directory'
    common_urls = search_inverted_indices(query, inverted_index_directory)
    url_frequencies, url_positions = search_inverted_indices_lite(query, inverted_index_directory)
    # print(common_urls)
    # print("now giving the psoitions of all words in the query   ")
    # for u in common_urls:
        # print(u)
        # print(url_positions[u])
        # print("---------------------------------------------")
    # input("Press Enter to continue...")
    # print("frequencies")
    # for u in common_urls:
    #     print(u)
    #     print(url_frequencies[u])
    #     print("---------------------------------------------")
    # cc=0
    # url_positions=sorted_urls = {k: v for k, v in sorted(url_positions.items())}

    transformed_positions = {}

    # Iterate over each URL and its word positions
    for url, word_positions in url_positions.items():
        # Iterate over each word and its positions
        for word, positions in word_positions.items():
            # Associate each position with the corresponding word and URL
            
            for position in positions:
                # Create a sub-dictionary for each position
                sub_dict = {word: position}
                transformed_positions.setdefault(url, []).append(sub_dict)
                
                # sorted_urls = {k: v for k, v in sorted(transformed_positions.items())}

        # input("Press Enter to continue...")
    # Print the transformed_positions dictionary
    # for u in common_urls:
    #     print(u)
    #     print(transformed_positions[u])
    #     print("---------------------------------------------")


        #now that we have the transformed urls
        sorted_positions = {}

    # Iterate over each URL and its word positions
    for url, word_positions in transformed_positions.items():
        # Combine all word positions into a single list with names
        all_positions = [{'name': name, 'position': pos} for word_position in word_positions for name, pos in word_position.items()]

        # Sort the positions based on the 'position' key
        all_positions.sort(key=lambda x: x['position'])

        # Assign the sorted positions back to the original word positions
        sorted_positions[url] = all_positions

    # Print the sorted_positions dictionary
    # for u in common_urls:
    #     print(u)
    #     print(sorted_positions[u])

    url_positions_score = {}

    # Convert the query to a list of words
    query_words = query.split()

    # Iterate over each URL and its sorted positions
    for url, positions in sorted_positions.items():
        # Iterate over each position and its name
        for i in range(len(positions) - len(query_words) + 1):
            # Extract a sequence of positions and names matching the length of the query
            sequence = positions[i:i + len(query_words)]

            # Check if positions have a difference of 1 and appear in the same sequence as the query
            if all(sequence[j]['position'] - sequence[j - 1]['position'] == 1 and sequence[j]['name'] == query_words[j]
                for j in range(1, len(query_words))):
                # Increment the position score by 15
                url_positions_score[url] = url_positions_score.get(url, 0) + 15

    # Print the url_positions_score dictionary
    # for url, score in url_positions_score.items():
    #     print(f"URL: {url}, Position Score: {score}")
    #     print("---------------------------------------------")

    url_scores={}
    for url in common_urls:
        # Combine the frequency score and position score for each URL
        frequency_score = url_frequencies[url]
        position_score = url_positions_score.get(url, 0)
        combined_score = frequency_score + position_score

        # Store the combined score in the url_scores dictionary
        url_scores[url] = combined_score

    # Sort the url_scores dictionary based on the frequency score in descending order
    sorted_url_scores = dict(sorted(url_scores.items(), key=lambda item: item[1], reverse=True))
    sorted_urls = list(sorted_url_scores.keys())

    print("sorted results below")
    print(sorted_urls)
    # Print the sorted_url_scores dictionary
    # for url, score in sorted_url_scores.items():
    #     print(f"URL: {url}, Combined Score: {score}")
    #     print("---------------------------------------------")

    # return sorted_urls
    sorted_url_metadata = []
    metadata_file_path = r"E:\salmandsa\DSA_Project\metadata.json"
    with open(metadata_file_path, "r", encoding="utf-8") as metadata_file:
        metadata = json.load(metadata_file)

    print("Metadata for sorted URLs:")
    for url in sorted_urls:
        # Get metadata for the current URL
        url_metadata = get_metadata(url, metadata)
        sorted_url_metadata.append(url_metadata)
        # if url_metadata:
        #     print(f"URL: {url}")
        #     print(f"Title: {url_metadata['title']}")
        #     print(f"Date: {url_metadata['date']}")
        #     print(f"Author: {url_metadata['author']}")
        #     print("---------------------------------------------")
        # else:
        #     print(f"No metadata found for URL: {url}")
        #     print("---------------------------------------------")

    print(sorted_url_metadata)
    return sorted_url_metadata

# middle=thesearch("in the middle of the night")
# print(middle)

    #now we gonna send the frequency and the url to a function to calculate the tf_idf score for each url
    #then we are gonna send the url_positions dictionary into the function that sorts all the positions in order and then the sequences in sorted order that are same as the query will be given a great score 
    #both scores combine to give the final score 
    #urls are then enlisted on the bases of score in the descending order



# Print the sorted URLs based on the calculated score
# print(sorted_urls)
# print("\nRanked URLs based on score:")
# for url, frequency in sorted_urls:
#     positions = url_positions_result[url]
#     print(f"\nURL: {url}")
#     print("Positions:")
#     for position in positions:
#         print(position)
#     print(f"Frequency: {frequency}")
#     print(f"Score: {calculate_score(frequency, positions)}")


# Example usage
# inverted_index_directory = r'E:\salmandsa\DSA_Project\inverted_index_directory'
# query = r'joe biden'
# cleaned_query = clean_query(query)
# result_urls = search_inverted_indices(cleaned_query, inverted_index_directory)
# print("\n".join(result_urls))

# Example usage
# inverted_index_directory = r'E:\salmandsa\DSA_Project\inverted_index_directory'
# query = r'nawaz sharif'
# cleaned_query = clean_query(query)
# result_urls = search_inverted_indices(cleaned_query, inverted_index_directory)
# print("\n".join(result_urls))

# now we are gonna rank these urls 

