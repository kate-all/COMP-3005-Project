# COMP-3005-Project

Hello! Thanks for taking a look at my project! I hope your marking is going well. Here are some instructions on how to use it.

### System Requirements
1. Postgresql
2. Python Packages:
   - psycopg2
   - random
3. PgAdmin (Optional)

## Setup
1. Make sure all the system requirements are downloaded and the python packages are installed in your virtual environment
2. Open `password.txt` and replace `3005proj` with the `postgres` user password on your local machine
3. Run main.py
4. Feel free to run queries on the database in PgAdmin at any time!

## Notes
- This program assumes that the inputs are of valid datatype. Error checking is done for CLI purposes only (Ex. The program checks if an input is `y` or `n`, but not that it's a string)