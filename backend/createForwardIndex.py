#nltk used for tokenization,stemming and frequency distribution 
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

# json module to work with json files
import json 

# os module to work with the file system
import os

# global variables initialized
count = 0 #counts total number of documents processed
batch_count = 0 #counts number of batches 

# Function to create forward index
# Arguments:
# input_directory - Directory containing newsdata in json files
# output_directory - Directory in which forward index is saved
# output_prefix - foward_index files created with this prefix
# batch_size - maximum number of articles allowed to be saved in a single forward_index json file 
def Create_Forward_Index(input_directory,output_directory,output_prefix='forward_index', batch_size=10000):
    global count
    global batch_count
    
    # list initialized to hold forward index entries
    forward_index_list = [] 

    # English stemmer initialized
    stemmer = SnowballStemmer("english")  

    # some stop words are added and saved in a set (as they allow faster memberhsip tests) 
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
    "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'@', '.', ',', '”', '\'', '“', ';', ':', '-', "and"
}
    # additional_stop_words = ['@', '.', ',', '”', '\'', '“', ';', ':', '-', "and"]

    # news articles loaded in articles variable
    with open(input_directory, 'r') as inputFile:
        articles = json.load(inputFile)

        # loop to iterate through all articles in the input file
        for article in articles:

            # content and title of each article is tokenized and saved in words list
            words = word_tokenize(article['content'])
            title = word_tokenize(article['title'])
            words.extend(title)
            
            # each word in the words list is reduced to its base form and saved in list 
            stemmed_words = [stemmer.stem(word) for word in words]
            # words converted to lower case and saved if they are not stop words and are alpha numeric
            filtered_stem_words = [word.lower() for word in stemmed_words if word not in stopwords and word.isalnum()]
            #frequency distribution of words created 
            freq_dist = FreqDist(filtered_stem_words)

            # Increase frequency of title words (helps in ranking algorithm later)
            for word in title:
                freq_dist[word.lower()] += 10
            
            # dictioray to store forward index entry of a single article
            # url saved (serves as doc id as its unique)
            # empty dictionary for word (to store position and frequency)
            forward_index = {"url": article['url'], "words": {}}

            #loops thtough each word in the filtered stem words
            #if word is not in the dictionary, add its frequency and position
            #if word is already in the dictionary,just append its postion 
            #as a result of this loop, a dictoinary for one article is created
            for position, word in enumerate(filtered_stem_words):
                if word in forward_index["words"]:
                    forward_index["words"][word]["positions"].append(position)
                else:
                    forward_index["words"][word] = {"frequency": freq_dist[word], "positions": [position]}

            #append this forward_index dict to fowrard_index list
            forward_index_list.append(forward_index)
            #counts and prints articles process
            count += 1#counts docs
            print(f"\ndocs processed: {count}\n")

            # if 10000 aritcles processed, create a json file using the prfix and batch count
            # dump the list of dictionaries in that file
            if count % batch_size == 0:
                print(f"10000 done\n")
                batch_count += 1
                output_file = os.path.join(output_directory, f"{output_prefix}_{batch_count}.json")
                with open(output_file, 'w') as json_file:
                    json.dump(forward_index_list, json_file, indent=2)
                forward_index_list = [] #list reset for next batch

        # if some newsdata file didnt had 10k articles,
        # dump it's forward index in the same way as above   
        if forward_index_list:
            batch_count += 1
            output_file = os.path.join(output_directory, f"{output_prefix}_{batch_count}.json")
            with open(output_file, 'w') as json_file:
                json.dump(forward_index_list, json_file, indent=2)
    

# path to directory in which forward_index is saved
output_directory=r'E:\salmandsa\DSA_Project\forward_index_directory'
# output prefix
output_prefix='forward_index_combined'

#path to input directory containing newsdata
input_directory_path =r'C:\Users\Asus\Downloads\dataverse_files\nela-gt-2022.json\nela-gt-2022\newsdata'


# List of all josn files in the input directory
all_files = [os.path.join(input_directory_path, file) for file in os.listdir(input_directory_path) if file.endswith('.json')]


# counts number of files created for forward_index
fcount=0

# loop to create forward index of all files 
for file_path in all_files:
    # Create forward index with batch size 10000 in the specified output directory
    Create_Forward_Index(file_path, output_directory, output_prefix, batch_size=10000)
    
    print(f"\nFILE = {fcount+1} \n")
    fcount+=1
    # loop terminates if 100,000 articles processes
    if count>=125000:
        break





    