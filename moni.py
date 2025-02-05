import json
import os
from datetime import datetime
from termcolor import colored # type: ignore

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Path to the balance file (same directory as the script)
def get_balance_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "balance.json")

# Save balance
def save_balance(value):
    file_name = get_balance_file_path()
    with open(file_name, "w") as file:
        json.dump({"balance": value}, file)

# Load balance
def load_balance():
    file_name = get_balance_file_path()
    try:
        with open(file_name, "r") as file:
            return json.load(file)["balance"]
    except (FileNotFoundError, KeyError):
        return 0

# Log a transaction in JSON format
def log_transaction(action, amount, reason, category, log_file="logs.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, log_file)

    # Convert action to "+" or "-" for the log
    if action == "Added":
        action_symbol = "+"
        amount_color = "green"
    elif action == "Withdrawn":
        action_symbol = "-"
        amount_color = "red"
    else:
        action_symbol = ""
        amount_color = "cyan"

    # Create a transaction entry
    transaction = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action_symbol": action_symbol,
        "amount": amount,
        "amount_color": amount_color,
        "reason": reason,
        "category": category
    }

    # Load existing logs, if any
    try:
        with open(log_file_path, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    # Add the new transaction
    logs.append(transaction)

    # Save the updated logs
    try:
        with open(log_file_path, "w") as file:
            json.dump(logs, file, indent=4)
    except IOError:
        print(colored("\nError saving logs.", "red"))

# Display logs from JSON file
def display_logs(log_file="logs.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, log_file)

    try:
        with open(log_file_path, "r") as file:
            logs = json.load(file)
            if logs:
                print(colored("\nTransaction Logs:", "yellow") + "\n" + "="*40)
                
                # Variable pour garder une trace du mois précédent
                previous_month = None
                
                for log in logs:
                    # Récupère le mois de la transaction actuelle
                    current_month = log['timestamp'][:7]  # "YYYY-MM"
                    
                    # Si le mois change, ajoute un espace
                    if previous_month and current_month != previous_month:
                        print(" ")
                    
                    action_symbol_colored = colored(log['action_symbol'], log['amount_color'])
                    amount_colored = colored(f"{log['amount']} €", log['amount_color'])
                    print(f"[{log['timestamp']}] {action_symbol_colored}{amount_colored} - Reason: {log['reason']} - Category: {log['category']}")
                    
                    # Mise à jour du mois précédent
                    previous_month = current_month
            else:
                print(colored("\nNo logs available.", "red") + "\n" + "="*40)
    except (FileNotFoundError, json.JSONDecodeError):
        print(colored("\nNo logs available.", "red") + "\n" + "="*40)

# Categories
def get_categories():
    return [
        "Housing",
        "Transport",
        "Food",
        "Health",
        "Education and Personal Development",
        "Entertainment and Leisure",
        "Clothing and Accessories",
        "Unexpected Expenses",
        "Savings and Investments",
        "Donations and Gifts"
    ]

# Select category (only available in Withdraw Funds)
def select_category():
    categories = get_categories()
    print(colored("\nSelect a category:", "magenta"))
    for i, category in enumerate(categories, start=1):
        print(f"{i}: {category}")

    while True:
        try:
            choice = int(input("Enter the number of the category: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print(colored("Invalid choice. Please select a valid category.", "red"))
        except ValueError:
            print(colored("Invalid input. Please enter a number.", "red"))

# Main menu
user = "Axo"
currency = "€"

def main_menu():
    while True:
        clear_screen()
        print(colored(r" /$$      /$$                           /$$", "yellow"))
        print(colored(r"| $$$    /$$$                          |__/", "yellow"))
        print(colored(r"| $$$$  /$$$$    /$$$$$$    /$$$$$$$    /$$", "yellow"))
        print(colored(r"| $$ $$/$$ $$   /$$__  $$  | $$__  $$  | $$", "yellow"))
        print(colored(r"| $$  $$$| $$  | $$  \ $$  | $$  \ $$  | $$", "yellow"))
        print(colored(r"| $$\  $ | $$  | $$  | $$  | $$  | $$  | $$", "yellow"))
        print(colored(r"| $$ \/  | $$  |  $$$$$$/  | $$  | $$  | $$", "yellow"))
        print(colored(r"|__/     |__/   \______/   |__/  |__/  |__/", "yellow"))
        print(colored("\x1B[3m                                      1.0.0\x1B[0m", "yellow"))
        print("")
        print(colored(f"Welcome back, {user}!", "green"))
        print("="*43)
        balance_colored = colored(f"{load_balance()} {currency}", 'blue')
        print(f"Current Balance: {balance_colored}\n")
        print("1: Add Funds")
        print("2: Withdraw Funds")
        print("3: View Logs")
        print("4: Exit")
        print("="*43)

        choice = input("Please select an option (1-4): ")

        # Check if the input is a valid number
        try:
            choice = int(choice)
        except ValueError:
            print(colored("\nInvalid input. Please enter a number.", "red"))
            input("\nPress Enter to return to the menu.")
            continue

        if choice == 1:
            add_funds()
        elif choice == 2:
            withdraw_funds()
        elif choice == 3:
            clear_screen()
            display_logs()
            input("\nPress Enter to return to the menu.")
        elif choice == 4:
            clear_screen()
            print(colored("\nGoodbye! See you next time.", "blue") + "\n" + "="*40)
            break
        else:
            print(colored("\nInvalid choice. Please select a valid option.", "red"))
            input("\nPress Enter to return to the menu.")

def add_funds():
    clear_screen()
    print(colored("Add Funds", "yellow") + "\n" + "="*40)
    while True:
        try:
            add = float(input("Enter the amount to add: "))
            if add <= 0:
                print(colored("\nInvalid amount. Please enter a positive number.", "red"))
                continue  # Demander à nouveau si l'entrée est invalide

            reason = input("Enter the reason for this addition: ")

            current_balance = load_balance()
            new_balance = current_balance + add
            save_balance(new_balance)
            log_transaction("Added", add, reason, "N/A")  # Pas de catégorie pour l'ajout de fonds

            print(colored(f"\nSuccess! {add} {currency} has been added for '{reason}'.", "green"))
            print(f"Your new balance is: {new_balance} {currency}.")
            break  # Sortir de la boucle après une entrée valide
        except ValueError:
            print(colored("\nInvalid amount. Please enter a valid number.", "red"))

def withdraw_funds():
    clear_screen()
    print(colored("Withdraw Funds", "yellow") + "\n" + "="*40)
    while True:
        try:
            withdraw = float(input("Enter the amount to withdraw: "))
            if withdraw <= 0:
                print(colored("\nInvalid amount. Please enter a positive number.", "red"))
                continue  # Demander à nouveau si l'entrée est invalide

            reason = input("Enter the reason for this withdrawal: ")
            category = select_category()  # Sélection de catégorie

            current_balance = load_balance()
            if withdraw > current_balance:
                print(colored(f"\nError: You do not have enough balance to withdraw {withdraw} {currency}.", "red"))
                print(colored(f"Your current balance is: {current_balance} {currency}.", "yellow"))
                continue  # Demander à nouveau si le montant est trop élevé

            new_balance = current_balance - withdraw
            save_balance(new_balance)
            log_transaction("Withdrawn", withdraw, reason, category)

            print(colored(f"\nSuccess! {withdraw} {currency} has been withdrawn for '{reason}' under '{category}'.", "green"))
            print(colored(f"Your new balance is: {new_balance} {currency}.", "green"))
            break  # Sortir de la boucle après une entrée valide
        except ValueError:
            print(colored("\nInvalid amount. Please enter a valid number.", "red"))

# Run the program
if __name__ == "__main__":
    main_menu()
