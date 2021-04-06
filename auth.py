# create a mock bank interface

# sets up a mock bank account
# takes a user's first and last name, email and a password
# user logins with an account number generated when registering

import random  # imports the random module to be used in generating an account number
import json    # imports the json module to be used in saving the contents of the database to a file

bank_database = {}  # a dictionary that stores a user details. used as a database


# the main function. starts the app
def main():
    print('Welcome to Union Bank')
    read_from_file()

    print('Do you have an account with us?\nEnter 1 for Yes\nEnter 2 for No')
    have_account = input('Please enter an option\n')

    if have_account == '1':
        login()

    elif have_account == '2':
        register()

    else:
        print('You entered an invalid option. Please try again')
        main()


def login():  # the bank login function. takes a user account number and password
    print('***** Login to your account *****')

    user_account = input('Please enter your account number\n')
    for account_number, userDetails in bank_database.items():
        if user_account == str(account_number):
            print('Hi %s! Please enter your password to login' % userDetails[0])
           
            wrong_password = True   # checks to see if password entered by user matches the one in the database
            
            while wrong_password:   # loops the enter a password input
                password = input('Enter password\n')
                if password == userDetails[3]:
                    print('Login Successful!')
                    bank_operations(userDetails)
                else:
                    print('Wrong password entered. Please try again')
            
    print('No account found. Please try again')
    login()

def register():  # the register function. takes a user details and saves that in the database
    print('***** Register *****')
    first_name = input('Enter your First Name\n')
    last_name = input('Enter your Last Name\n')
    email = input('Enter your Email address\n')
    password = input('Create a password\n')

    #   this tries to check if the account number generated is already in the system
    #   if it is, it generates another random number

    if len(bank_database) > 0:

        duplicate_account = True

        while duplicate_account:
            account_number = generate_account_number()

            for account in bank_database:
                if account == account_number:
                    duplicate_account = True
                    break
                else:
                    duplicate_account = False

    else:
        account_number = generate_account_number()

    # this is the details saved in the database. the last index is for the user's balance
    # a user starts with zero bank balance
    bank_database[account_number] = [first_name, last_name, email, password, 0]

    print('Hi %s %s! Your account has been created successfully' % (first_name, last_name))
    print('Your account number is %s. Please keep it safe' % account_number)
    print('Login to your account to continue')
    login()


def generate_account_number():  # this generates a random account number
    print('Generating Account Number')
    return random.randrange(0000000000, 9999999999)


def bank_operations(user):  # this are the bank operations function. links to various other functions
    print('Welcome %s %s' % (user[0], user[1]))
    print('What would you like to do?')
    print('Please select an option\n1. Withdrawal\n2. Deposit\n3. Check Balance\n4. Logout\n5. Exit')
    selected_option = input('Enter an option\n')

    if selected_option == '1':
        withdrawal(user)

    elif selected_option == '2':
        deposit(user)

    elif selected_option == '3':
        check_balance(user)

    elif selected_option == '4':
        print('You have logged out successfully')
        login()

    elif selected_option == '5':
        print('Thanks for banking with us. Goodbye!')
        save_to_file()
        exit()

    else:
        print('You entered an invalid option. Please try again')
        bank_operations(user)


def withdrawal(user):  # this is the withdrawal functions. withdraws a sum the user inputs from the user balance
    print('How much would you like to withdraw?')

    try:
        withdrawal_amount = int(input('Please enter an amount\n'))
        if user[4] - withdrawal_amount >= 0:  # this checks if the user has sufficient balance to effect the withdrawal
            print('Please take your cash')  # gives the user the sum if they do
            user[4] = user[4] - withdrawal_amount  # updates the user balance
            bank_operations(user)
        else:
            print('Insufficient cash')  # prints an Insufficient Cash message if the withdrawal amount exceeds the
            # user balance
            bank_operations(user)

    except ValueError:  # exception to catch a ValueError which occurs when the user inputs strings instead of integers
        print('Please enter an amount in figures')
        withdrawal(user)


def deposit(user):  # the deposit function. collects a deposit amount and updates the user balance
    print('How much would you like to deposit? Enter an amount in figures')
    try:
        deposit_amount = int(input('Enter amount\n'))
        user[4] = user[4] + deposit_amount
        print('Deposit of %s successful!' % deposit_amount)
        check_balance(user)
        bank_operations(user)

    except ValueError:
        print('Please enter an amount in figures and try again')
        deposit(user)


def check_balance(user):  # the check balance function. checks the user available balance and prints that
    print('Your current account balance is', user[4])
    bank_operations(user)


def save_to_file():  # the save to file function. saves the content of the bank database dictionary to a file
    with open('database.txt', 'w') as file:
        file.write(json.dumps(bank_database))
        file.close()


def read_from_file():  # the read file function. reads the file at the start of the app and saves to bank_database
    global bank_database
    try:
        bank_database = json.load(open('database.txt'))

    except FileNotFoundError:
        pass


if __name__ == '__main__':  # only start app if the module is being run directly and not when imported
    main()
