alphabet = input("")
alpha = list(alphabet)
letters_heard = input("")
letters = list(letters_heard)

remaining_letters = letters.copy()
pass_count = 0

while len(remaining_letters) > 0:
    pass_count += 1
    letters_to_remove = []
    
    # Go through alphabet from left to right
    for letter in alpha:
        if letter in remaining_letters:
            letters_to_remove.append(letter)
    
    # Remove all matched letters
    for letter in letters_to_remove:
        remaining_letters.remove(letter)
    
    # If no letters were found in this pass, break to avoid infinite loop
    if len(letters_to_remove) == 0:
        break

print(f"Number of passes through alphabet: {pass_count}")



