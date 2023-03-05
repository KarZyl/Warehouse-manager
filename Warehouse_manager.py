from datetime import date
import logging
logging.basicConfig(level=logging.INFO)
import pickle

head = ["Name", "Quantity", "Unit", "Unit price (zł)"]

with open("database.txt", "rb") as fp:
    database = pickle.load(fp)

a = 1
ex = 0
items_list = []

with open("sold_items.txt", "rb") as fp:
    sold_items = pickle.load(fp)


def validate(arg):
    try:
        arg = float(arg)
        return float(arg)
    except ValueError:
        logging.error("Enter valid number")
        return False
    
def get_unit():
    while True:
        unit = input("Enter products unit ['szt', 'kg', 'm', 'm2', 'm3','l']: ")
        if unit in ["szt", "kg", "m", "m2", "m3","l"]:
            return unit  
   
def add_item():
    name = input("enter product name: ")
    while True:
        quantity  = input("Enter products quantity: ")
        if validate(quantity):
            break
    unit = get_unit()
    while True:
        unit_price = input("Enter product price in PLN: ")
        if validate(unit_price):
            break
    items_list = [name, quantity, unit, unit_price]
    database.append(items_list)
    logging.info(f" Added item: '\n' {(head[0])}- {items_list[0]} '\n' {head[1]} - {items_list[1]} '\n' {head[2]} - {items_list[2]} '\n' {head[3]} - {items_list[3]} zł")
    with open("database.txt", "wb") as fp:
            pickle.dump(database, fp)

def show_database():
    print (head[0] + '\t'*2 + head[1] + '\t' + head[2] + '\t'*2 + head[3])
    print ("--------------------------------------------------------------")
    if database == []: 
        print("\n Current database is empty. Enter 'add' to add item \n")
    for a in database:
        print(*a, sep=(2*'\t'))

def sell_item():
    item = input("Item name: ")
    for var in database:
        check = 1
        if var[0] == item:
            print (f"There is {var[1]} {var[2]} {var[0]} in stock \n How much would you like to sell?: ")
            quantity = validate(input())
            sell_value = quantity * float(var[3])
            end_quantity = float(var[1]) - quantity
            if end_quantity >= 0:
                var[1] = end_quantity
                sold_item = [f"{date.today()}", var[0], quantity, var[2], var[3], sell_value]
                sold_items.append(sold_item)
                if float(var[1]) == 0.0:
                    database.remove(var)  
                with open("sold_items.txt", "wb") as fp:
                    pickle.dump(sold_items, fp)
                    check = 0
                    logging.info(f"You sold {quantity} {var[2]} {var[0]} for {sell_value}")
                    break
            elif quantity == 0:
                print("Quantity = 0, you have not sold anything")
                check = 0
                break
            else:
                print("You are trying to sell more than you have in stock, try again")
                check = 0
                break
    if check == 1:
        print("This item does not occur in database")
    with open("database.txt", "wb") as fp:
        pickle.dump(database, fp)

def show_sold_items():
    with open("sold_items.txt", "rb") as fp:
        for a in pickle.load(fp):
            print ('\t', a)

def show_value():
    sum = 0
    for var in database:
        sum = sum + float(var[1]) * float(var[3])
    logging.info(f"Current stock value is {sum} zł")

def show_sold_value():
    sum = 0
    for var in sold_items:
        sum = sum + float(var[5])
    logging.info(f"Current sold value is {sum} zł")
    
if __name__ == "__main__":
    while ex != 1:
        action = input("What would you like to do?  ")
        if action == "exit":
            print ("Exiting... Bye!")
            exit
            ex = 1
        elif action == "add":
            add_item()
        elif action == "show":
            show_database()
        elif action == "showsold":
            show_sold_items()
        elif action == "sell":
            sell_item()
        elif action == "showvalue":
            show_value()
        elif action == "showsoldvalue":
            show_sold_value()
      

        else:
            print("""
            Possible commands: 
            \n add - Adds new item 
            \n show - Shows current stock 
            \n sell - Choose what and how much to sell
            \n showvalue - Shows current stock value
            \n showsold - Shows sold items
            \n showsoldvalue- Shows sold items value
            \n exit- Exits program 
            
            """)
            
            

    