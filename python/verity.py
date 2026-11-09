def verity1():
    print("Hey")
    print("It's me")
    print("It's Verity")
    print("Ask me anything!")
    print("I know about a million things...")
    print("I'll do everything")
    response = input("What's the capitol of [ Germany / France ]? (Enter A / B) ")
    if response == "B":
        verity2()
    else:
        evilverity()

def verity2():
    print("Oh, oui oui oui")
    print("It is Paris")
    response = input("Okay, what does the [ cow / chicken ] say?  (Enter A / B) ")
    if response == "A":
        verity3()
    else:
        evilverity()

def verity3():
    print("Oh, moo moo moo")
    print("I speak that too")
    print("All day")
    print("Do you live alone? Is anybody home?")
    print("One, two, three and so, where did everybody go?")
    
def evilverity():
    print("Wrong question.")
    print("*Vores you*")

def main():
    verity1()

if __name__ == "__main__":
    main()
