import random
import pandas as pd

try:
    # Try to load the CSV file
    df = pd.read_csv("../data/pokemon_data.csv")
    pokemon_names = df['Name'].tolist()
except Exception as e:
    # Print error and use a fallback list if file can't be loaded
    print(f"Error loading CSV: {e}")
    pokemon_names = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon"]
    print("Using fallback Pokemon names")

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
def generate_name(start_char=None, max_length=15):
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
    for _ in range(max_length - 1):  # Fixed syntax error: * → _
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

# Generate and print several Pokémon names
if __name__ == "__main__":  # Only run when script is executed directly
    print("Generating Pokemon names...")
    for i in range(5):
        print(f"Generated name {i + 1}: {generate_name()}")