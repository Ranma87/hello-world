stock = [400, 540, 120, 9, 550]     # water, milk, beans, cups, money


def coffee_machine():
    while True:
        action = input('Write action (buy, fill, take, remaining, exit):\n')
        print('')
        if action == 'exit':
            break
        elif action == 'remaining':
            state()
        elif action == 'buy':
            sell()
        elif action == 'fill':
            fill()
        elif action == 'take':
            take()
        else:
            print("Option doesn't exist")
        pass


def state():
    global stock
    print(f'The coffee machine has\n'
          f'{stock[0]} of water\n'
          f'{stock[1]} of milk\n'
          f'{stock[2]} of coffee beans\n'
          f'{stock[3]} of disposable cups\n'
          f'${stock[4]} of money\n')


def sell():
    global stock
    inputs_names = ['water', 'milk', 'coffee beans', 'disposable cups', 'price']
    inputs = [['espresso', 'latte', 'cappuccino'],
              [250, 0, 16, 1, 4],   # espresso needs
              [350, 75, 20, 1, 7],  # latte needs
              [200, 100, 12, 1, 6]]     # cappuccino needs
    coffee_type = (input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n'))
    if coffee_type != 'back':
        coffee_type = int(coffee_type)
        a = True
        for i in range(0, 4):
            if stock[i] < int(inputs[coffee_type][i]):
                print(f'Sorry, not enough {inputs_names[i]}!')
                a = False
        if a:
            print('I have enough resources, making you a coffee!')
            for i in range(0, 4):
                stock[i] -= inputs[coffee_type][i]
            stock[4] += inputs[coffee_type][4]
    print('')
    pass


def fill():
    global stock
    stock[0] += int(input(f'Write how many ml of water do you want to add:\n'))
    stock[1] += int(input(f'Write how many ml of milk do you want to add:\n'))
    stock[2] += int(input(f'Write how many grams of coffee beans do you want to add:\n'))
    stock[3] += int(input(f'Write how many disposable cups of coffee do you want to add:\n'))
    print('')
    pass


def take():
    global stock
    print(f'I gave you ${stock[4]}\n')
    stock[4] = 0
    pass


coffee_machine()

#
# req_cups = int(input('Write how many cups of coffee you will need:\n'))
# pos_cups = []
# for i in [0, 1, 2]:
#     pos_cups.append(stock[i] // inputs_cup[i])
# if min(pos_cups) == req_cups:
#     print('Yes, I can make that amount of coffee')
# elif min(pos_cups) > req_cups:
#     extra = min(pos_cups) - req_cups
#     print(f'Yes, I can make that amount of coffee (and even {extra} more than that)')
# else:
#     print(f'No, I can make only {min(pos_cups)} cups of coffee')
