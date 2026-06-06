my_list = [
    {
        'a': ["1", "2", "3"],
        'b': 'Hello',
        'c': int("123"[2]) + 3
    },
    {
        'a': ["4", "5", "6"],
        'b': 'World',
        'c': int("456"[2]) + 3
    }
]
print(my_list[1]['a'][1] + str(my_list[1]['c']))  # Output: "56"
print(my_list[0]['b'] + my_list[1]['b'])  # Output: "HelloWorld"