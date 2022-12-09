import business_logic as bl


customer_menu = {"menu": "- Show this command menu again",
                 "search": "<field> <value> - Search for a book by field. Ex. search genre romance",
                 "search <field> <operator> <value>": "- Search for a book by numerical value of price or page count (ex. search page_count < 800)\n\t\t\t\t\tDo not include $ in the price",
                 "search available": "- See all available books",
                 "select": "<isbn> - Select a book by its isbn to see more information",
                 "unselect": "- Unselect current selected book",
                 "login": "- Login to your account",
                 "logout": "- Log out of your account",
                 "register": "- Register for an account",
                 "add_to_basket": "- Add the selected book to your basket",
                 "checkout": "- Order the items in your basket",
                 "track": "<order_num> - Get order and tracking info for a given order",
                 "exit": "- Exit this application."
                 }

employee_menu = {"menu": "- Show this command menu again",
                 "search": "<field> <value> - Search for a book by field. Ex. search genre romance",
                 "search <field> <operator> <value>": "- Search for a book by numerical value of price or page count (ex. search page_count < 800)\n\t\t\t\t\tDo not include $ in the price",
                 "search available": "- See all available books",
                 "select": "<isbn> - Select a book by its isbn to see more information",
                 "unselect": "- Unselect current selected book",
                 "add_book": "- Add a book to the catalog",
                 "delete_book": "- Delete a book from the catalog",
                 "view_report": "- View report",
                 "view_reorder_list": "- See list of books waiting for reorder, along with the reorder quantity and publisher email",
                 "exit": "- Exit this application."}

def print_menu(user_type):
    print("\nWe have a library of commands you can use! (Get it?)\n")

    if user_type == 'c':
        for k,v in customer_menu.items():
            print(k, v)

    else:
        for k,v in employee_menu.items():
            print(k, v)

    print()

def print_books(books):
    print("{0:<30}".format("ISBN"), "{0:<30}".format("Title"))
    for book in books:
        isbn = book[0][1:14]
        title = book[0][15:-1].strip('"')
        print("{0:<30}".format(isbn), "{0:<30}".format(title))

def print_cards(cards):
    print("{0:<20}".format("Selection #"), "{0:<30}".format("Card Number"))
    for i in range(len(cards)):
        print("{0:<20}".format(i), "{0:<30}".format(str(cards[i][0])))

def main():
    cur = None
    selected = None
    logged_in = False
    basket = []

    print("Hello! Welcome to LookInnaBook!\n" +
      "There's plenty to explore in our store.\n")

    first_time = input("Is this your first time using our CLI app? (y/n) ")
    while first_time != "y" and first_time != "n":
        print("Oops! You have to tell us if it's your first time using the app. I promise it's relevant!")
        first_time = input("Is this your first time using our CLI app? (y/n) ")

    if first_time == "y":
        print("Welcome! \nGenerating our database for you... This may take a moment")
        cur = bl.create_database()

    else:
        print("Welcome back!")
        cur = bl.connect_to_db()

    user_type = input("To get started, please tell us, are you a customer or an employee? (c/e) ")
    while user_type != "c" and user_type != "e":
        print("Oops! You have to enter c for customer or e for employee")

    print_menu(user_type)

    while True:
        full_command = input("> ").split(" ")
        command = full_command[0]

        if user_type == "c" and command in employee_menu and command not in customer_menu:
            print("This command is for employees only")

        elif user_type == "e" and command in customer_menu and command not in employee_menu:
            print("This command is for customers only")

        elif command == "menu":
            print_menu(user_type)

        elif command == "search":
            output = bl.search(cur, full_command[1], full_command[2:])
            if output == None:
                print("Please enter a valid search field.\nThe options are: title, isbn, page_count, price, genre, author, publisher, and available")
            elif output == []:
                print("There are no books that match your search query.")
            else:
                print_books(output)

        elif command == "select":
            selected = int(full_command[1])
            output = bl.get_book(cur, selected, user_type)

            book_info = output[0][0][1:-1].split(",")
            authors = ""
            for author in output[1]:
                if author[0] == None:
                    authors += author[1] + ","
                else:
                    authors += author[0] + " " + author[1] + ","

            genres = ""
            for genre in output[2]:
                genres += genre[0] + ","

            print("ISBN:", book_info[0])
            print("Title:", book_info[1].strip('"'))
            print("Author(s):",authors[:-1])
            print("Page_Count:", book_info[2])
            print(f"Price: ${book_info[3]}")
            print("Genre(s):",genres[:-1])
            print("Publisher:",book_info[4].strip('"'))
            if user_type == 'e':
                print("Num Sold:",book_info[5])
                print("Num Sold Last Month:",book_info[6])
                print("% for Publisher:",book_info[7])
                print("Wholesale Price",book_info[8])
                print("In Stock:",book_info[9])

        elif command == "unselect":
            if selected == None:
                print("No book is selected")
            else:
                selected = None

        elif command == "login":
            username = input("Username: ")
            password = input("Password: ")
            success = bl.login(cur, username, password)
            if not success:
                print("Username or password incorrect")
            else:
                logged_in = True
                print("Login successful")

        elif command == "logout":
            if not logged_in:
                print("You're not logged in")

            else:
                logged_in = False
                print("Logout successful")

        elif command == "register":
            username = input("Please enter a username: ")
            valid = bl.is_valid_username(cur, username)
            while not valid:
                print(username, "has already been taken.\nLet's get creative!")
                username = input("Please enter a username: ")
                valid = bl.is_valid_username(cur, username)

            password = input("Please enter a password: ")

            success = bl.create_new_account(cur, username, password)
            if not success:
                print("Account registration unsuccessful")
                continue

            print("Account sucessfully created.\nWelcome to the LookInnaBook family!")
            logged_in = True
            add_card = input("Would you like to add a credit card to your account? (y/n) ")
            while add_card != "y" and add_card != "n":
                print("Oops! Please enter a y to add a credit card to your account or n to skip this step")
                add_card = input("Would you like to add a credit card to your account? (y/n) ")

            if add_card == 'y':
                card_num = input("Credit card number: ")
                expiry_date = input("Expiry Date (yyyy-mm-dd): ")
                cvv = input("CVV (3 numbers on back): ")
                bl.add_card(cur, card_num, expiry_date, cvv, username)

            add_address = input("Would you like to add an address to your account? (y/n) ")
            while add_address != "y" and add_address != "n":
                print("Oops! Please enter a y to add an address to your account or n to skip this step")
                add_address = input("Would you like to add an address to your account? (y/n) ")

            if add_address == 'y':
                street_num = input("Street num: ")
                street = input("Street name: ")
                city = input("City: ")
                province = input("Province (In 2 letter format, ex ON): ")
                country = input("Country: ")
                postal_code = input("Postal Code: ")
                bl.add_address(cur, street_num, street, city, province, country, postal_code, username)

        elif command == "add_to_basket":
            if selected == None:
                print("No book selected")

            else:
                if not bl.is_available(cur, selected):
                    print("Sorry! This book is out of stock")
                else:
                    basket.append(selected)
                    print("Added", selected, "to basket")
                    selected = None

        elif command == "checkout":
            if basket == []:
                print("Your basket is empty")
                continue
            if not logged_in:
                print("Please log in to checkout")
                continue

            linked_addresses = bl.get_addresses(cur, username)
            address_for_order = None
            if linked_addresses != []:
                use_linked_address =input("Do you want to use an address linked to your account? (y/n) ")
                while use_linked_address != "y" and use_linked_address != "n":
                    use_linked_address =input("Please type y to use a linked address or n to use a new address_for_order ")

                if use_linked_address == "y":
                    for i in range(len(linked_addresses)):
                        print(i,"-",linked_addresses[i])
                    address_num = int(input(f"Enter a number in the selection menu to select "))
                    while address_num < 0 or address_num >= len(linked_addresses):
                        address_num = int(input(f"Please enter a number in the selection menu to select an address "))

                    address_for_order = linked_addresses[address_num][0][1:-1].split(",")
                    address_for_order[1] = address_for_order[1][1:-1]
                    print("DEBUG",address_for_order)

            if linked_addresses == [] or use_linked_address == "n":
                street_num = input("Street num: ")
                street = input("Street name: ")
                city = input("City: ")
                province = input("Province (In 2 letter format, ex ON): ")
                country = input("Country: ")
                postal_code = input("Postal Code: ")
                address_for_order = (street_num, street, postal_code)
                bl.add_address(cur, street_num, street, city, province, country, postal_code, username)

            linked_cards = bl.get_cards(cur, username)
            use_linked_card = None
            card = None
            if linked_cards != []:
                use_linked_card =input("Do you want to use a credit card linked to your account? (y/n) ")
                while use_linked_card != "y" and use_linked_card != "n":
                    use_linked_card =input("Please type y to use a linked credit card or n to use a new card ")

                if use_linked_card == "y":
                    for i in range(len(linked_cards)):
                        print(i,"-",linked_cards[i])
                    print_cards(linked_cards)
                    card_num = int(input(f"Enter a number in the selection menu to select "))
                    while card_num < 0 or card_num >= len(linked_cards):
                        card_num = int(input(f"Please enter a number in the selection menu to select a credit card "))

                    card = str(linked_cards[card_num])[10:-4]

            if linked_cards == [] or use_linked_card == "n":
                card_num = input("Credit card number: ")
                expiry_date = input("Expiry Date (yyyy-mm-dd): ")
                cvv = input("CVV (3 numbers on back): ")
                card = card_num
                bl.add_card(cur, card_num, expiry_date, cvv, username)

            order_num = bl.create_order(cur, address_for_order[2], address_for_order[1], address_for_order[0], basket, card)
            print("Order", order_num, "created")

        elif command == "exit":
            is_sure = None
            if user_type == "c":
                is_sure = input("Are you sure you want to exit? Your basket will be emptied. (y/n) ")

            else:
                is_sure = input("Are you sure you want to exit? (y/n) ")

            while is_sure != "y" and is_sure != "n":
                is_sure = input("Oops! Please type y to exit and n to continue in this app. ")

            if is_sure == 'y':
                print("Thank you for visiting our bookstore!")
                break

        elif command == "track":
            print(bl.get_order(cur, full_command[1]))

        elif command == "add_book":
            publisher_name = input("Publisher name: ")
            p_id = bl.get_publisher(cur, publisher_name)
            if p_id == []:
                p_email = input("Publisher email: ")
                p_phone_num = input("Publisher phone number (10 digit number): ")
                p_bank_acc = input("Publisher bank account number (17 digit number): ")
                p_id = bl.add_publisher(cur, publisher_name, p_email, p_phone_num, p_bank_acc)

            else:
                p_id = p_id[0][0]

            isbn = input("ISBN: ")
            title = input("Title: ")
            page_count = input("Page count: ")
            price = input("Price (don't add $): ")
            price_wholesale = input("Wholesale price (don't add $): ")
            in_stock = input("Amount in stock: ")
            percent_for_publisher = input("% for publisher (don't add %): ")
            author_names = input("Author name(s) (ex. John Smith,William Shakespeare): ").split(",")
            genres = input("Genre(s) (separate with ,): ").split(",")
            success = bl.add_book(cur, isbn, title, page_count, price, price_wholesale, in_stock, percent_for_publisher, p_id, author_names, genres)
            if not success:
                print(isbn, "is already in our system!")
            else:
                print(isbn, "added")

        elif command=="delete_book":
            isbn = input("ISBN: ")
            success = bl.delete_book(cur,isbn)
            if not success:
                print(isbn,"is not in the system")
            print(isbn, "removed")

        elif command=="view_report":

            report = bl.report(cur)
            print("REPORT")
            print("-" * 50)

            print("Number of books sold last month:",end=" ")
            print(report[0])

            print("Most popular genre last month:",end=" ")
            cur.execute("""SELECT genre, sum(num_sold_last_month) AS sold FROM Book, Has_Genre
        WHERE Book.isbn = Has_Genre.book_isbn
        GROUP BY genre
        ORDER BY sold DESC
        LIMIT 1""")
            print(report[1])

            print("Most popular genre of all time:",end=" ")
            cur.execute("""SELECT genre, sum(num_sold) AS sold FROM Book, Has_Genre
        WHERE Book.isbn = Has_Genre.book_isbn
        GROUP BY genre
        ORDER BY sold DESC
        LIMIT 1""")
            print(report[2])

        elif command=="view_reorder_list":
            print(bl.reorder_list(cur));

        else:
            print("Command not found. Please try again")


main()