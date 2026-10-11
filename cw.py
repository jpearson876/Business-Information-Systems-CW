# csv is imported to read the file of books
# matplotlib is imported to create a chart
import csv
import matplotlib.pyplot as plt

# Load Books function
def load_books(filename):
    books = []
    try:
        # The csv file is opened
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file) # Each row is read as a dictionary

            for row in reader:
                # Spaces are removed and lowercase keys are made
                row = {key.strip().lower(): value.strip() for key, value in row.items()}

                try:
                    cost = float(row.get("cost", 0)) # Cost is converted to float
                except:
                    cost = 0 # Cost will be 0 if it is invalid

                try:
                    stock = int(float(row.get("stock", 0))) # Stock is converted to integer, 0 if invalid
                except:
                    stock = 0

                    # I cleaned the book data after it wasn't picked up
                books.append({
                    "author": row.get("author", ""),
                    "title": row.get("title", ""),
                    "format": row.get("format", ""),
                    "publisher": row.get("publisher", ""),
                    "cost": cost,
                    "stock": stock,
                    "genre": row.get("genre", "")
                })

    except FileNotFoundError:
        # A message tells the user if the file isn't detected
        print("File not found. Starting with empty list.")

    return books


# Save books function
def save_books(filename, books):
    # File is opened in write mode so it can be edited
    with open(filename, "w", newline='', encoding='utf-8') as file:
        fieldnames = ["author", "title", "format", "publisher", "cost", "stock", "genre"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader() # Column headers are written
        writer.writerows(books) # Book data is written


# Menu function
def menu():
    # Once the system is run, the options of functions are shown to the user
    print("\n--- Book Store Inventory System ---")
    print("1. Display all books")
    print("2. Summary report")
    print("3. Genre report")
    print("4. Add new book")
    print("5. Search & update stock")
    print("6. Sort by author")
    print("7. Show genre chart")
    print("8. Quit")


# Display books function
def display_books(books):
    # A check is included in case the list is empty
    if not books:
        print("No books available.")
        return
# A loop is created to print each book and its details
    for b in books:
        print(f"{b['author']} | {b['title']} | {b['format']} | {b['publisher']} | £{b['cost']} | Stock: {b['stock']} | {b['genre']}")


# Summary function
def summary_report(books):
    if not books:
        print("No books available.")
        return

    # The number of books is counted
    total_titles = len(books)
    # Value of stock is calculated
    total_value = sum(b["cost"] * b["stock"] for b in books)
    # Average book price is calculated
    avg_price = sum(b["cost"] for b in books) / total_titles

# All calculations are displayed in the summary
    print("Total titles:", total_titles)
    print("Total stock value: £", round(total_value, 2))
    print("Average price: £", round(avg_price, 2))


# Genre report function
def genre_report(books):
    genres = {} # A dictionary is created to store genre count

    for b in books:
        genres[b["genre"]] = genres.get(b["genre"], 0) + 1
        # Books are counted per genre

    for g, count in genres.items():
        print(g, ":", count)
        # The results of the count are printed

# Add books function
def add_book(books):
    author = input("Author: ").strip()
    title = input("Title: ").strip()
    format_type = input("Format: ")
    publisher = input("Publisher: ")

    # The system is checked to see if the book already exists
    for b in books:
        if b["title"].lower() == title.lower() and b["author"].lower() == author.lower():
            print("This book already exists in the system.")

            choice = input("Do you want to update the stock instead? (y/n): ").lower()
            if choice == "y":
                try:
                    amount = int(input("Enter amount to add to stock: "))
                    b["stock"] += amount
                    print(f"Stock updated. New stock: {b['stock']}")
                except ValueError:
                    print("Invalid number.")
            return  # Stop adding duplicate

    # If book doesn't already exist, it is added
    try:
        cost = float(input("Cost: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Invalid input.")
        return

    genre = input("Genre: ")

    books.append({
        "author": author,
        "title": title,
        "format": format_type,
        "publisher": publisher,
        "cost": cost,
        "stock": stock,
        "genre": genre
    })

    print("Book added successfully!")

# Update stock function
def update_stock(books):
    title = input("Enter book title: ")

    # The book is searched for in the list
    for b in books:
        if b["title"].lower() == title.lower():
            print("Book found!")
            # The user can choose to increase or decrease stock
            choice = input("1. Increase stock\n2. Decrease stock\n")

            try:
                amount = int(input("Amount: "))
            except ValueError:
                print("Invalid number.")
                return

            # Stock is either increased or decreased depending on user choice
            if choice == "1":
                b["stock"] += amount

            elif choice == "2":
                b["stock"] -= amount
                if b["stock"] <= 0:
                    b["stock"] = 0
                    print("Book is now out of stock.")

            return

    print("Book not found")


# Sort by author function
def sort_by_author(books):
    # Books are sorted alphabetically by author surnames
    sorted_books = sorted(books, key=lambda x: x["author"])

    # The list of sorted books is then shown
    for b in sorted_books:
        print(f"{b['author']} - {b['title']}")

# Genre chart function
def plot_genres(books):
    genres = {}

    # The amount of books in each genre is counted
    for b in books:
        genres[b["genre"]] = genres.get(b["genre"], 0) + 1

    # Bar chart is created
    plt.bar(genres.keys(), genres.values())
    plt.xlabel("Genre")
    plt.ylabel("Number of Books")
    plt.title("Books per Genre")
    plt.show()


# Main program
filename = "booksdata.csv"

# The existing book data in the csv file is loaded
books = load_books(filename)

# A loop runs once the user has run the system
# and continues until it is exited
while True:
    menu()
    choice = input("Choose option (1-8): ").strip()

    if choice == "1":
        display_books(books)

    elif choice == "2":
        summary_report(books)

    elif choice == "3":
        genre_report(books)

    elif choice == "4":
        add_book(books)
        save_books(filename, books)

    elif choice == "5":
        update_stock(books)
        save_books(filename, books)

    elif choice == "6":
        sort_by_author(books)

    elif choice == "7":
        plot_genres(books)

    elif choice == "8":
        print("System closed.")
        break

    else:
        print("Invalid option. Please choose a number between 1 and 8.")