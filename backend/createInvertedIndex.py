
# import json
# import os
# from collections import defaultdict


# # This function determines the barrel/folder a word will be saved in
# # based on the first Character's ASCII (alphabetically)
# def get_barrel(char):
#     # Define ASCII ranges for barrels
#     if 'a' <= char <= 'z':
#         # alphaber stored in aplhabet barrel 
#         return f'barrel_{ord(char) - ord("a")}'
#     elif '0' <= char <= '9':
#         # numbers stored in numeric barrels
#         return 'numeric_barrel'
#     else:
#         # other characters in other barrels
#         return 'other_barrel'

# # This is the main function. It loads the forward index files, 
# # processes each word in each article, assigns them to their respective barrels, 
# # and then saves the information in inverted index files. 
# def update_inverted_indices(forward_index_directory, inverted_index_directory):

#     # Initialize inverted indices for each barrel

#     # 26 default dictionaries created 
#     # Each defaultdict will store information related to words starting with the corresponding letter.
#     inverted_indices = {f'barrel_{i}': defaultdict(list) for i in range(26)}
    
#     # defaultdict to store information related to words starting with numeric characters.
#     inverted_indices['numeric_barrel'] = defaultdict(list)

#     # defaultdict to store information related to words starting non alpha numeric characters
#     inverted_indices['other_barrel'] = defaultdict(list)

#     # This defaultdict will store information related to words that contain numeric characters
#     # but don't exclusively start with them.
#     numeric_index = defaultdict(list)

#     # List of all forward index files in the forward_index directory
#     forward_index_files = [f for f in os.listdir(forward_index_directory) if f.endswith('.json')]

#     # Iterating through each forward index file
#     for forward_index_file in forward_index_files:
#         forward_index_file_path = os.path.join(forward_index_directory, forward_index_file)

#         # opening the forward index file
#         with open(forward_index_file_path, 'r') as json_file:
#             forward_index_data = json.load(json_file)

#         # Iterating through each article in the forward index
#         for article in forward_index_data:

#             # url and word information extracted from current article
#             url = article['url']
#             words_info = article['words']

#             # Go through each word in the article
#             for word, info in words_info.items():

#                 # Find the barrel of current word by its first charactere
#                 first_char = word[0].lower() if word else None
#                 barrel = get_barrel(first_char)

#                 # Append information to the respective inverted index barrel
#                 inverted_indices[barrel][word].append({
#                     'url': url,
#                     'frequency': info['frequency'],
#                     'positions': info['positions']
#                 })

#     # Save the updated inverted indices
#     for barrel, inverted_index in inverted_indices.items():
#         # find out the path of the barrel(file) in which current inverted_index is to be saved 
#         inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')

#         # open that barrel and append the inverted index entry
#         with open(inverted_index_path, 'a') as json_file:
#             json.dump(inverted_index, json_file, indent=2)
#             json_file.write('\n')  # Add newline for each new entry

#     # Save the numeric index
#     # numeric_index_path = os.path.join(numeric_index_directory, 'numeric_index.json')
#     # with open(numeric_index_path, 'a') as json_file:
#     #     json.dump(numeric_index, json_file, indent=2)
#     #     json_file.write('\n')  # Add newline for each new entry

# # input and output paths specified 
# forward_index_directory = r'E:\salmandsa\DSA_Project\forward_index_directory'
# inverted_index_directory = r'E:\salmandsa\DSA_Project\inverted_index_directory'
# # numeric_index_directory = r'E:\salmandsa\DSA_Project\numeric_index_directory'

# # function to create/update inverted index called
# update_inverted_indices(forward_index_directory, inverted_index_directory)


import json
import os
from collections import defaultdict


# This function determines the barrel/folder a word will be saved in
# based on the first Character's ASCII (alphabetically)
# def get_barrel(chars):
#     # Combine the two characters to form a two-letter string
#     char = chars.lower()  # Ensure lowercase for consistency

#     # Check if the combined string is alphabetic
#     if char.isalpha() and len(char) == 2:
#         # Calculate a unique barrel number based on the ASCII values of the two characters
#         return f'barrel_{((ord(char[0]) - ord("a") )* 26) + (ord(char[1]) - ord("a"))}'
#     elif char.isdigit():
#         # Numbers stored in numeric barrels
#         return 'numeric_barrel'
#     else:
#         # Other characters in other barrels
#         return 'other_barrel'
from datetime import datetime

def print_current_time():
    # Get current date and time
    current_time = datetime.now()

    # Format the current time as a string
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Print the formatted time
    print("Current Time:", formatted_time)

# Call the function to print the current time

count =0
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


# This is the main function. It loads the forward index files, 
# processes each word in each article, assigns them to their respective barrels, 
# and then saves the information in inverted index files. 
def update_inverted_indices(forward_index_directory, inverted_index_directory):
    global count

    # Initialize inverted indices for each barrel
    inverted_indices = {f'barrel_{i}': defaultdict(list) for i in range(26*26)}
    inverted_indices['numeric_barrel'] = defaultdict(list)
    inverted_indices['other_barrel'] = defaultdict(list)
    numeric_index = defaultdict(list)

    # List of all forward index files in the forward_index directory
    forward_index_files = [f for f in os.listdir(forward_index_directory) if f.endswith('.json')]

    # Iterating through each forward index file
    for forward_index_file in forward_index_files:
        forward_index_file_path = os.path.join(forward_index_directory, forward_index_file)

        # Opening the forward index file
        with open(forward_index_file_path, 'r') as json_file:
            forward_index_data = json.load(json_file)

        # Iterating through each article in the forward index
        for article in forward_index_data:
            url = article['url']
            words_info = article['words']

            # Go through each word in the article
            for word, info in words_info.items():
                first_two_chars = word[:2].lower() if word else None
                # print(first_two_chars)
                barrel = get_barrel(first_two_chars)
                # print(barrel)
                count+=1
                if(count%1000==0):
                    print(count)

                # Check if the word is already in the inverted index
                if word in inverted_indices[barrel]:
                    
                    inverted_indices[barrel][word].append({
                        'url': url,
                        'frequency': info['frequency'],
                        'positions': info['positions']
                    })
                else:
    # If the word doesn't exist, create a new entry for it
                    inverted_indices[barrel][word] = [{
                        'url': url,
                        'frequency': info['frequency'],
                        'positions': info['positions']
                    }]


    # Save the updated inverted indices
    for barrel, inverted_index in inverted_indices.items():
        inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')

        with open(inverted_index_path, 'a') as json_file:
            json.dump(inverted_index, json_file, indent=2)
            json_file.write('\n')

# Input and output paths specified 
forward_index_directory = r'E:\salmandsa\DSA_Project\forward_index_directory'
inverted_index_directory = r'E:\salmandsa\DSA_Project\inverted_index_directory'

# Function to create/update inverted index called
print_current_time()
update_inverted_indices(forward_index_directory, inverted_index_directory)
print_current_time()

