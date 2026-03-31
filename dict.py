# dict.py
import re
import inflect
import string

def remove_punctuation(text):
    punctuation_to_remove = r'[.,:!]'
    text_without_punctuation = re.sub(punctuation_to_remove, '', text)
    return text_without_punctuation

def clean_text(text):
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return cleaned_text

# SECTION 1
def process_text(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            text = input_file.read()
            print(text)
        
        mapping_array = []
        sentences = re.split(r'[\.\n]+', text)
        
        title_found = False
        
        for sentence in sentences:
            # Skip empty lines or separators
            if not sentence.strip() or sentence.strip().startswith('-'):
                continue
            
            # Check if this line starts with "TITLE:"
            if sentence.strip().startswith('TITLE:'):
                # Add "TITLE" as a spoken word
                mapping_array.append(['TITLE', sentence])
                
                # Extract and add the actual title text (WITHOUT "TITLE:")
                title_text = sentence.replace('TITLE:', '').strip()
                split_word = title_text.split(" ")
                for word in split_word:
                    if word == "" or word == " ":
                        continue
                    mapping_array.append([word, sentence])
                title_found = True
                
            # Check if this line starts with "CONTENT:"
            elif sentence.strip().startswith('CONTENT:'):
                # DON'T add "CONTENT" - just add the content text
                content_text = sentence.replace('CONTENT:', '').strip()
                split_word = content_text.split(" ")
                for word in split_word:
                    if word == "" or word == " ":
                        continue
                    mapping_array.append([word, sentence])
            
            # Regular sentence (no prefix)
            else:
                split_word = sentence.split(" ")
                for word in split_word:
                    if word == "" or word == " ":
                        continue
                    mapping_array.append([word, sentence])
        
        # Remove punctuation
        for arr in mapping_array:
            arr[0] = remove_punctuation(arr[0])
        
        # Write each word to the output file
        with open(output_filename, 'w') as output_file:
            with open("texts/image_overlay.txt", "w") as test_file:
                for arr in mapping_array:
                    arr[0] = clean_text(arr[0])
                    output_file.write(arr[0].upper() + '\n')
                    test_file.write(arr[1] + '\n')
        
        print(f"Output written to {output_filename} successfully.")
    
    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# SECTION 2
def process_text_section2(input_file_path, output_file_path):
    p = inflect.engine()
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except:
        raise TypeError
    
    words = text.split()
    
    def convert_number(word):
        original_word = word
        lw = word.lower()
        if lw.isdigit() or re.match(r'^\d+(st|nd|rd|th)$', lw):
            return convert_ordinal_to_words(lw)
        return original_word
    
    def convert_ordinal_to_words(ordinal):
        try:
            cardinal = re.sub(r'(st|nd|rd|th)$', '', ordinal.lower())
            word = p.number_to_words(cardinal)
            text = p.ordinal(word).upper()
            text = text.translate(str.maketrans('', '', string.punctuation.replace('-', '')))
            text = text.replace('-', ' ')
            return text
        except ValueError:
            return "Invalid input"
    
    words = [convert_number(word) for word in words]
    
    processed_words = []
    for word in words:
        for sub_word in word.split():
            processed_words.append(sub_word.upper())
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for word in processed_words:
            v = ''
            for letter in word:
                if letter.isnumeric() or letter.isalpha():
                    v += letter
            file.write(v + ' ')