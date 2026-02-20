from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        '''
        Initialise shoe attributes when a new Shoe object is created.
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        '''
        Return the cost of this shoe.
        '''
        return self.cost

    def get_quantity(self):
        '''
        Return the quantity of this shoe.
        '''
        return self.quantity

    def __str__(self):
        '''
        Return a readable string representation of this shoe object.
        '''
        return f"({self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity})"


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


#==========Functions outside the class==============

def read_shoes_data():
    '''
    Open inventory.txt and read each line of shoe data.
    Create a Shoe object from each line and append it to shoe_list.
    Skips the header line. Uses try/except for error handling.
    '''
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
            for line in lines[1:]: # Skip the header line
                try:
                    country, code, product, cost, quantity = line.strip().split(",")
                    shoe = Shoe(country, code, product, int(cost), int(quantity))
                    shoe_list.append(shoe)
                except ValueError as e:
                    print(f"Error processing line: {line.strip()}. Error: {e}")
    except FileNotFoundError:
        print("Error: inventory.txt file not found.")

def capture_shoes():
    '''
    Ask the user to enter details for a new shoe.
    Create a Shoe object and add it to shoe_list and save it to the file.
    '''
    country = input("Enter the country of the shoe: ")
    code = input("Enter the code of the shoe: ")
    product = input("Enter the product name of the shoe: ")
    try:
        cost = int(input("Enter the cost of the shoe: "))
        quantity = int(input("Enter the quantity of the shoe: "))
    except ValueError:
        print("Invalid input. Cost and quantity must be numbers.")
        return
    
    # Create new shoe object and add to the list
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)

    # Save new shoe to file
    with open("inventory.txt", "a") as file:
        file.write(f"\n{country},{code},{product},{cost},{quantity}")
    print("Shoe added successfully!")

def view_all():
    '''
    Display all shoes in shoe_list as a formatted table using tabulate.
    Each row uses the shoe's attributes directly.
    '''
    if not shoe_list:
        print("No shoes in inventory.")
        return
    table = [[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
             for shoe in shoe_list]
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(table, headers, tablefmt="grid"))
    
        

def re_stock():
    '''
    Find the shoe with the lowest quantity and offer to restock it.
    If the user agrees, ask how many to add, update the object in memory,
    and rewrite the entire inventory file with the updated quantity.
    '''
    if not shoe_list:
        print("No shoes in inventory.")
        return
    
    # Find shoe with minimum quantity
    min_quantity = min(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"\nShoe with the lowest quantity: {min_quantity.product} (Quantity: {min_quantity.quantity})")

    # Ask user if they want to restock
    restock = input("Do you want to add more stock for this shoe? (yes/no): ")
    if restock.lower() == "yes":
        try:
            additional_quantity = int(input("Enter the quantity to add: "))
            if additional_quantity <= 0:
                print("Please enter a positive number.")
                return
            
            # Update quantity in memory
            min_quantity.quantity += additional_quantity

            # Rewrite the entire file with updated data
            with open("inventory.txt", "w") as file:
                file.write("Country,Code,Product,Cost,Quantity\n")
                for shoe in shoe_list:
                    file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
            print(f"Updated quantity for {min_quantity.product}: {min_quantity.quantity}")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def search_shoe():
    '''
    Ask the user for a shoe code and search for it in shoe_list.
    Print and return the matching shoe object, or notify if not found.
    Search is case-insensitive.
    '''
    code = input("Enter the shoe code to search: ").strip().upper()
    for shoe in shoe_list:
        if shoe.code.upper() == code:
            print(f"\nShoe found: {shoe}")
            return shoe
    print("No shoe found with that code.")

def value_per_item():
    '''
    Calculate and display the total value of each shoe item.
    Value is calculated as: value = cost * quantity.
    Displayed as a formatted table.
    '''
    if not shoe_list:
        print("No shoes in inventory.")
        return

    # Build table with value calculated for each shoe
    table = [[shoe.product, shoe.cost, shoe.quantity, shoe.cost * shoe.quantity]
             for shoe in shoe_list]
    headers = ["Product", "Cost", "Quantity", "Total Value"]
    print("\n--- Stock Value Per Item ---")
    print(tabulate(table, headers, tablefmt="grid"))

def highest_qty():
    '''
    Find the shoe with the highest quantity in shoe_list.
    Print it as being on sale.
    '''
    if not shoe_list:
        print("No shoes in inventory.")
        return

    # Find shoe with maximum quantity
    max_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"\nShoe with the highest quantity: {max_shoe.product} "
          f"(Quantity: {max_shoe.quantity}) - ON SALE!")


#==========Main Menu=============

def main_menu():
    """
    Display a menu in a loop and call the appropriate function
    based on the user's choice.
    """
    while True:
        print("\nShoe Inventory Management System")
        print("1. Capture new shoe data")
        print("2. View all shoes")
        print("3. Restock shoe with lowest quantity")
        print("4. Search for a shoe by code")
        print("5. Calculate value per item")
        print("6. Show shoe with highest quantity for sale")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            capture_shoes()
        elif choice == "2":
            view_all()
        elif choice == "3":
            re_stock()
        elif choice == "4":
            search_shoe()
        elif choice == "5":
            value_per_item()
        elif choice == "6":
            highest_qty()
        elif choice == "7":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Load shoe data from file automatically when the program starts
if __name__ == "__main__":
    read_shoes_data()  # Load data automatically
    main_menu()