import sqlite3
from random import randint
import os.path

# check if the database already exists
if not os.path.isfile('card.s3db'):
    conn = sqlite3.connect('card.s3db')     # Make the connection with the database
    c = conn.cursor()                       # Create a cursor
    # Create table
    c.execute('''CREATE TABLE card(
                        id INTEGER,
                        number TEXT,
                        pin TEXT,
                        balance INTEGER DEFAULT 0
                        );''')
else:
    # Make connection with the database and create a cursor
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()


class Bank:

    def main_menu(self):
        while True:
            print("1. Create an account", "2. Log into account", "0. Exit", sep='\n')
            main_choice = input()

            if main_choice == '0':
                break
            if main_choice == '1':
                self.create_account()
            elif main_choice == '2':
                self.log_in()

    def create_account(self):
        new_card_number = self.card_number_generator()
        new_pin = str(randint(10000, 19999))
        new_pin = new_pin[1:]
        self.save_new_account(new_card_number, new_pin)
        print('\nYour card has been created\nYour card number:')
        print(new_card_number)
        print('Your card PIN:')
        print(new_pin)
        print()

    def log_in(self):
        login_card = input('\nEnter your card number:\n')
        login_pin = input('Enter your PIN:\n')
        c.execute(f'SELECT * FROM card WHERE number = ? AND pin = ?', (login_card, login_pin))
        user = c.fetchone()
        if user is None:
            print('\nWrong card number or PIN!\n')
        else:
            print("You have successfully logged in!\n")
            while True:
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                logged_choice = input()

                if logged_choice == '0':
                    print('\nBye!')
                    exit()
                if logged_choice == '5':
                    print('\nYou have successfully logged out!\n')
                    return
                if logged_choice == '1':
                    print('\nBalance: ' + self.balance(user) + '\n')
                if logged_choice == '2':
                    self.add_income(user)
                if logged_choice == '3':
                    self.do_transfer(user)
                if logged_choice == '4':
                    self.close_account(user)
                    return

    def close_account(self, account):
        c.execute('DELETE FROM card WHERE number = ?', (account[1],))
        conn.commit()
        print('\nThe account has been closed!\n')

    def balance(self, account):
        c.execute('SELECT balance FROM card WHERE number = ?', (account[1],))
        return str(c.fetchone()[0])

    def do_transfer(self, account):
        receiver = input('Transfer\nEnter card number:\n')
        if receiver[-1] != self.checksum(receiver[:-1]):
            print('Probably you made mistake in the card number. Please try again!\n')
            return
        c.execute('SELECT * FROM card WHERE number = ?', (receiver,))
        receiver_account = c.fetchone()
        if receiver_account is None:
            print('Such a card does not exist.\n')
            return
        transfer = int(input('\nEnter how much money you want to transfer:\n'))
        c.execute('SELECT balance FROM card WHERE number = ?', (account[1],))
        sender_money = c.fetchone()[0]
        if sender_money < transfer:
            print('Not enough money!\n')
            return
        # subtract the money from the user
        c.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (transfer, account[1]))
        conn.commit()
        # add the money to the receiver
        c.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (transfer, receiver))
        conn.commit()
        print('Success!\n')

    def add_income(self, account):
        income = int(input('\nEnter income:\n'))
        c.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (income, account[1]))
        conn.commit()
        print('Income was added!\n')

    def card_number_generator(self):
        iin = '400000'
        can = ''
        for i in range(9):
            n = str(randint(0, 9))
            can += n
        checksum = self.checksum(iin + can)
        return iin + can + checksum

    def checksum(self, number):
        number_list = [int(num) for num in number]
        for index in range(0, 15, 2):
            number_list[index] *= 2
            if number_list[index] > 9:
                number_list[index] -= 9
        checker = 0
        while (checker + sum(number_list)) % 10 != 0:
            checker += 1
        return str(checker)

    def save_new_account(self, card_number, pin):
        c.execute(f'INSERT INTO card(number, pin) VALUES (?,?)', (card_number, pin))
        conn.commit()


if __name__ == '__main__':
    my_bank = Bank()
    my_bank.main_menu()


conn.close()
