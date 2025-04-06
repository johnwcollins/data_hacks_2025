from flask import Flask, request, jsonify, render_template
import random
import pandas as pd
from PIL import Image
import os

# Create Flask app
app = Flask(__name__)

# Load Pokemon data and build Markov chain
try:
    # Try to load the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), "data/pokemon_data.csv")
    df = pd.read_csv(csv_path)
    pokemon_names = df['Name'].tolist()
except Exception as e:
    # Use a fallback list if file can't be loaded
    pokemon_names = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon"]
    print(f"Using fallback Pokemon names. Error: {e}")

# Join the names into a single text with newlines as separators
text = "\n".join(pokemon_names)

# Build a Markov chain dictionary
markov_chain = {}
for i in range(len(text) - 1):
    current_char = text[i]
    next_char = text[i + 1]
    
    if current_char not in markov_chain:
        markov_chain[current_char] = []
    
    markov_chain[current_char].append(next_char)

# Function to generate a name using the Markov chain
def generate_pokemon_name(start_char=None, max_length=15):
    # If no starting character is provided, choose one from the beginnings of names
    if start_char is None:
        # The first character of the text is a valid starting character
        start_chars = [text[0]]
        
        # Also include characters that follow a newline
        for i in range(1, len(text)):
            if text[i - 1] == "\n":
                start_chars.append(text[i])
        
        start_char = random.choice(start_chars)
    
    name = start_char
    current_char = start_char
    
    # Generate the rest of the name
    for _ in range(max_length - 1):
        if current_char in markov_chain:
            # Randomly choose the next character
            next_char = random.choice(markov_chain[current_char])
            
            # Check if we should end the name
            if next_char == "\n" and len(name) >= 3:
                break
            elif next_char == "\n":
                # If name too short and we hit newline, pick another character
                if markov_chain[current_char]:  # Make sure list isn't empty
                    next_char = random.choice(markov_chain[current_char])
            
            name += next_char
            current_char = next_char
        else:
            break
    
    # If after generation the name is still too short, try to extend it
    while len(name) < 3 and current_char in markov_chain:
        next_char = random.choice(markov_chain[current_char])
        if next_char != "\n":  # Avoid adding newlines
            name += next_char
            current_char = next_char
    
    return name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    # Check if the request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    
    # Check if file is empty
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Just open the image to verify it's valid
        img = Image.open(image_file)
        
        # Generate a Pokemon name using the Markov chain
        pokemon_name = generate_pokemon_name()
        
        # Select a random type image
        random_type_number = random.randint(1, 18)
        
        # This path should match your actual directory structure
        # Based on your screenshot, you have an "images/types" folder
        type_image_path = f"/static/images/types/{random_type_number}.png"
        
        # Return the results
        return jsonify({
            'name': pokemon_name,
            'typeImage': type_image_path
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Test the name generator
    print("Generating sample Pokemon names:")
    for i in range(5):
        print(f"Generated name {i + 1}: {generate_pokemon_name()}")
    
    print("\nStarting Pokemon Image Analyzer on http://localhost:5000")
    app.run(debug=True)
