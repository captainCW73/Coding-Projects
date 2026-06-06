user_profile = {
    'age': 30,
    'username': 'john_doe',
    'weapons': ['sword', 'bow', 'dagger'],
    'is_active': True,
    'clan': 'Shadow Warriors'
}
print(user_profile.keys())
user_profile['weapons'] = 'Katana'
user_profile.update({'is_banned': False})
user_profile['is_banned'] = True
user2 = user_profile.copy()
user2['username'] = 'jane_doe'
user2['age'] = 25
print(user_profile)
print(user2)