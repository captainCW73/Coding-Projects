#password generator problem
import random
import string

special_char = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
letters = string.ascii_lowercase  # "abcdefghijklmnopqrstuvwxyz"
numbers = string.digits  # "0123456789"

num_letters_to_use = random.randint(1, 10)  # Random number of letters (1-10)
num_numbers_to_use = random.randint(1, 5)  # Random number of digits (1-5)
num_special_to_use = random.randint(1, 3)  # Random number of special chars (1-3)

random_letter = random.choice(letters) * num_letters_to_use
random_number = random.choice(numbers) * num_numbers_to_use
random_special = random.choice(special_char) * num_special_to_use
print(random_letter + random_number + random_special)




