def checkDriverAge(age = 0):
    
    if int(age) < 18:
        return("Sorry, you are too young to drive this car. Powering off")
    elif int(age) > 18:
        return("Powering On. Enjoy the ride!")
    elif int(age) == 18:
        return("Congratulations on your first year of driving. Enjoy the ride!")
print(checkDriverAge(17))
