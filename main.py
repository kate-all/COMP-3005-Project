import business_logic as bl


customer_menu = {"menu": "Show this command menu again", "search <field> <value>": "Search for a book by field. Ex. search genre romance"}
employee_menu = {"menu": "Show this command menu again"}


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
    while first_time == "":
        first_time = input("Is this your first time using our CLI app? (y/n) ")
        if first_time == "":
            print("Oops! You have to tell us if it's your first time using the app. I promise it's relevant!")

    if first_time == "y":
        print("Welcome! \nGenerating our database for you... This may take a moment")
        cur = bl.create_database()

    else:
        print("Welcome back!")
        cur = bl.connect_to_db()

    user_type = ""
    while user_type == "":
        user_type = input("To get started, please tell us, are you a customer or an employee? (c/e) ")
        if user_type == "":
            print("Oops! You have to enter c for customer or e for employee")

    print_menu(user_type)

    while True:
        full_command = input("> ").split(" ")
        command = full_command[0]

        if command == "menu":
            print_menu(user_type)

        elif command == "search":
            output = bl.search(cur, full_command[1], full_command[2])
            print(output)

        break

main()