import json
import os

def create_url_lexicon(input_directory, output_file):
    url_to_id = {}
    unique_id = 0

    # List all JSON files in the input directory
    all_files = [os.path.join(input_directory, file) for file in os.listdir(input_directory) if file.endswith('.json')]

    for file_path in all_files:
        with open(file_path, 'r') as inputFile:
            articles = json.load(inputFile)

            for article in articles:
                url = article['url']
                if url not in url_to_id:
                    url_to_id[url] = unique_id
                    unique_id += 1

    # Save the URL to ID mapping to the output file
    with open(output_file, 'w') as json_file:
        json.dump(url_to_id, json_file, indent=2)

    print(f"Lexicon created with {unique_id} unique URLs.")

# Define paths
input_directory_path = r'C:\Users\Asus\Downloads\dataverse_files\nela-gt-2022.json\nela-gt-2022\newsdata'
output_file_path = r'E:\salmandsa\lexicon.json'

# Create the URL lexicon
create_url_lexicon(input_directory_path, output_file_path)
