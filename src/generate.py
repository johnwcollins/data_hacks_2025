import random
import pandas as pd

# Load Pokémon names from CSV
try:
    df = pd.read_csv("../pokemon_data.csv")
    pokemon_names = df['Name'].tolist()
except FileNotFoundError:
    # Fallback to a small set of names if the file isn't found
    pokemon_names = [
        "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon",
        "Charizard", "Squirtle", "Wartortle", "Blastoise", "Pikachu",
        "Eevee", "Jigglypuff", "Snorlax", "Mewtwo", "Dragonite"
    ]
    print("Warning: Pokemon data file not found, using built-in name list.")

# Join the names into a single text with newlines as name separators
text = "\n".join(pokemon_names)

# Build a more sophisticated Markov chain dictionary
# Using character pairs as states for better context
order = 2  # The number of characters to use as context
markov_chain = {}

# Pad the text to handle beginnings and endings better
padded_text = "^" * order + text + "$"

for i in range(len(padded_text) - order):
    current_chars = padded_text[i:i+order]
    next_char = padded_text[i+order]
    
    if current_chars not in markov_chain:
        markov_chain[current_chars] = []
    
    markov_chain[current_chars].append(next_char)

# Function to generate a name using the improved Markov chain
def generate_name(start_sequence=None, min_length=4, max_length=12):
    # If no starting sequence provided, choose one from the beginnings of names
    if start_sequence is None:
        # Get valid starting sequences (after padding character)
        start_sequences = []
        for key in markov_chain.keys():
            if key.startswith('^'):
                start_sequences.append(key)
        
        if not start_sequences:  # Fallback if no valid sequences found
            start_sequences = list(markov_chain.keys())
        
        start_sequence = random.choice(start_sequences)
    else:
        # Make sure the start sequence is the right length
        if len(start_sequence) > order:
            start_sequence = start_sequence[-order:]
        elif len(start_sequence) < order:
            # Pad with start character
            start_sequence = '^' * (order - len(start_sequence)) + start_sequence
    
    # Initialize with the non-padding characters from the start sequence
    name = start_sequence.replace('^', '')
    current_sequence = start_sequence
    
    # Generate the rest of the name
    while len(name) < max_length:
        # Check if the current sequence exists in our chain
        if current_sequence in markov_chain:
            next_char = random.choice(markov_chain[current_sequence])
            
            # If we hit an end character or newline, end the name
            if next_char in ['$', '\n']:
                break
                
            # Add the character to our name
            name += next_char
            
            # Update the current sequence (slide the window forward)
            current_sequence = current_sequence[1:] + next_char
        else:
            # If we have no data for the current sequence, try to break nicely
            break
    
    # If the name is too short, try again unless we've tried too many times
    if len(name) < min_length:
        retries = 3
        while len(name) < min_length and retries > 0:
            name = generate_name(start_sequence, min_length, max_length)
            retries -= 1
    
    # Capitalize the first letter and lowercase the rest
    if name:
        name = name[0].upper() + name[1:].lower()
    
    return name

# Generate and print several Pokémon names
print("Generated Pokémon Names:")
for i in range(10):
    print(f"  {i+1}. {generate_name()}")

# Allow user to specify a custom starting sequence
custom_start = input("\nEnter a starting sequence for a name (or press Enter for random): ").strip()
if custom_start:
    print(f"\nNames starting with '{custom_start}':")
    for i in range(5):
        print(f"  {i+1}. {generate_name(custom_start)}")