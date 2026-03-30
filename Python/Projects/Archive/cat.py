def main() :
    number = getnumber()
    meow(number)



def getnumber():
    while True:
        n = int(input("Enter a number: "))
        if n > 0:
            return n


def meow(n) :
    for _ in range(n) :
        print("meow")


main()