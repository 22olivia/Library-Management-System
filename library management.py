import mysql.connector
from tkinter import *
from tkinter import messagebox  # Import messagebox module
from PIL import Image, ImageTk

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#olivia@2005",
    database="library"
)

# Create database cursor
cursor = db.cursor()

# Create table for books if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), available BOOLEAN)")

# GUI Functions
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    if title and author:
        cursor.execute("INSERT INTO books (title, author, available) VALUES (%s, %s, %s)", (title, author, True))
        db.commit()
        title_entry.delete(0, END)
        author_entry.delete(0, END)
        messagebox.showinfo("Success", "Book added successfully")
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def search_book():
    title = title_entry.get()
    if title:
        cursor.execute("SELECT * FROM books WHERE title LIKE %s", ('%' + title + '%',))
        books = cursor.fetchall()
        if books:
            book_list.delete(0, END)
            for book in books:
                book_list.insert(END, book)
        else:
            messagebox.showinfo("Info", "No books found")
    else:
        messagebox.showerror("Error", "Please enter a title to search")

def borrow_book():
    selected_book = book_list.curselection()
    if selected_book:
        book_id = book_list.get(selected_book[0])[0]
        cursor.execute("UPDATE books SET available = False WHERE id = %s", (book_id,))
        db.commit()
        messagebox.showinfo("Success", "Book borrowed successfully")
    else:
        messagebox.showerror("Error", "Please select a book to borrow")

def return_book():
    selected_book = book_list.curselection()
    if selected_book:
        book_id = book_list.get(selected_book[0])[0]
        cursor.execute("UPDATE books SET available = True WHERE id = %s", (book_id,))
        db.commit()
        messagebox.showinfo("Success", "Book returned successfully")
    else:
        messagebox.showerror("Error", "Please select a book to return")

def display_borrowed_books():
    cursor.execute("SELECT * FROM books WHERE available = False")
    borrowed_books = cursor.fetchall()
    if borrowed_books:
        book_list.delete(0, END)
        for book in borrowed_books:
            book_list.insert(END, book)
    else:
        messagebox.showinfo("Info", "No books are currently borrowed")

def display_all_books():
    cursor.execute("SELECT * FROM books")
    all_books = cursor.fetchall()
    if all_books:
        book_list.delete(0, END)
        for book in all_books:
            book_list.insert(END, book)
    else:
        messagebox.showinfo("Info", "No books in the library")

# GUI Setup
root = Tk()
root.title("Library Management System")

# Define colors
primary_color = "black"
secondary_color = "white"
button_color = "teal"
text_color = "red"

# background_image = Image.open("book.jpeg")
# background_image = background_image.resize((120, 120))
# background_photo = ImageTk.PhotoImage(background_image)

# background_label = Label(root, image=background_photo)
# background_label.place(x=-650,y=-325, relwidth=1, relheight=1)
# Left grid
left_frame = Frame(root, bg=primary_color)
left_frame.grid(row=0, column=0, padx=10, pady=5)

title_label = Label(left_frame, text="Title:", bg=primary_color, fg=text_color)
title_label.grid(row=0, column=0, padx=10, pady=5)
title_entry = Entry(left_frame, bg=secondary_color)
title_entry.grid(row=0, column=1, padx=10, pady=5)

author_label = Label(left_frame, text="Author:", bg=primary_color, fg=text_color)
author_label.grid(row=1, column=0, padx=10, pady=5)
author_entry = Entry(left_frame, bg=secondary_color)
author_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = Button(left_frame, text="Add Book", command=add_book, bg=button_color, fg=text_color)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

search_button = Button(left_frame, text="Search Book", command=search_book, bg=button_color, fg=text_color)
search_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="WE")

# Middle grid
middle_frame = Frame(root, bg=primary_color)
middle_frame.grid(row=0, column=1, padx=10, pady=5)

book_list_label = Label(middle_frame, text="Books:", bg=primary_color, fg=text_color)
book_list_label.grid(row=0, column=0, padx=10, pady=5)

book_list = Listbox(middle_frame, width=50, bg=secondary_color, fg=text_color)
book_list.grid(row=1, column=0, padx=10, pady=5)

borrow_button = Button(middle_frame, text="Borrow Book", command=borrow_book, bg=button_color, fg=text_color)
borrow_button.grid(row=2, column=0, padx=10, pady=5, sticky="WE")

return_button = Button(middle_frame, text="Return Book", command=return_book, bg=button_color, fg=text_color)
return_button.grid(row=3, column=0, padx=10, pady=5, sticky="WE")

display_borrowed_button = Button(middle_frame, text="Display Borrowed Books", command=display_borrowed_books, bg=button_color, fg=text_color)
display_borrowed_button.grid(row=4, column=0, padx=10, pady=5, sticky="WE")

display_all_button = Button(middle_frame, text="Display All Books", command=display_all_books, bg=button_color, fg=text_color)
display_all_button.grid(row=5, column=0, padx=10, pady=5, sticky="WE")

# Right grid (for future expansion)
right_frame = Frame(root, bg=primary_color)
right_frame.grid(row=0, column=2, padx=10, pady=5)

root.mainloop()