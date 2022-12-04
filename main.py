import business_logic as bl


def printMenu():
    print("Available Commands:\n")

def main():
    cur = None
    print("Hello! Welcome to LookInnaBook!\n" +
      "There's plenty to explore in our store.\n")

    first_time = input("Is this your first time using our CLI app? (y/n) ")
    if first_time == "y":
        print("Welcome! \nGenerating our database for you... This may take a moment")
        cur = bl.create_database()

    else:
        print("Welcome back!")
        cur = bl.connect_to_db()

    while True:
        full_command = input("> ")
        command = full_command[0]
        break

main()