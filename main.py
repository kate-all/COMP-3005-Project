import business_logic as bl


customer_menu = {"menu": "Show this command menu again",
                 "search <field> <value>": "Search for a book by field. Ex. search genre romance",
                 "search <field> <operator> <value>": "Search for a book by numerical value of price or page count (ex. search page_count < 800",
                 "exit": "Exit this application."
                 }


employee_menu = {"menu": "Show this command menu again",
                 "exit": "Exit this application."}


def print_menu(user_type):
    print("\nWe have a library of commands you can use! (Get it?)\n")

    if user_type == 'c':
        for k,v in customer_menu.items():
            print(k ," - " + v)

    else:
        for k,v in employee_menu.items():
            print(k, " - " + v)

    print("\n")

def main():
    cur = None
    print("Hello! Welcome to LookInnaBook!\n" +
      "There's plenty to explore in our store.\n")


    first_time = ""
    while first_time != "y" and first_time != "n":
        first_time = input("Is this your first time using our CLI app? (y/n) ")
        if first_time != "y" and first_time != "n":
            print("Oops! You have to tell us if it's your first time using the app. I promise it's relevant!")

    if first_time == "y":
        print("Welcome! \nGenerating our database for you... This may take a moment")
        cur = bl.create_database()

    else:
        print("Welcome back!")
        cur = bl.connect_to_db()

    user_type = ""
    while user_type != "c" and user_type != "e":
        user_type = input("To get started, please tell us, are you a customer or an employee? (c/e) ")
        if user_type != "c" and user_type != "e":
            print("Oops! You have to enter c for customer or e for employee")

    print_menu(user_type)

    while True:
        full_command = input("> ").split(" ")
        command = full_command[0]

        if command == "menu":
            print_menu(user_type)

        elif command == "search":
            output = bl.search(cur, full_command[1], full_command[2:])
            if output == []:
                print("There are no books that match your search query.")
            else:
                print(output)

        elif command == "exit":
            is_sure = input("Are you sure you want to exit? Your basket will be emptied. (y/n) ")

            while is_sure != "y" and is_sure != "n":
                is_sure = input("Oops! Please type y to exit and n to continue in this app.")

            if is_sure == 'y':
                break


main()