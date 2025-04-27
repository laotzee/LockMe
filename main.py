import tkinter
import tkinter as tk
from tkinter import ttk, messagebox
import string
from secrets import choice
import json

UPPER = list(string.ascii_uppercase)
LOWER = list(string.ascii_lowercase)
DIGITS = list(string.digits)
PUNC = list(string.punctuation)

UPPER_NUM = 4
LOWER_NUM = 4
DIGITS_NUM = 4
PUNC_NUM = 4

X = 15
Y = 15
IMG = "resources/lockmeLogo.png"
WIDTH = 630
HEIGHT = 500
MINT = "#E0F7E9"
YELLOW = "#F2CB30"
DEFAULT_FILE = "pass.json"

FILL_ERROR_TITLE = "Empty fields"
FILL_ERROR_MESSAGE = "You must fill all the fields"
WEBSITE_ERROR_TITLE = "Empty website"
WEBSITE_ERROR_MESSAGE = "You have to provide website of the credentials"
USER_ERROR_TITLE = "Empty username"
USER_ERROR_MESSAGE = "You have to provide username of the credentials"
REGISTER_ERROR_TITLE = "Credentials not found"
REGISTER_ERROR_MESSAGE = "There are not such credentials in the database"
CREDENTIALS_TITLE = "Credentials"
SUCCESSFUL_CREATION_MESSAGE = "Record saved to file"
SUCCESSFUL_CREATION_TITLE = "Operation successful"
VERIFY_TITLE = "Information integrity"
VERIFY_MESSAGE = "Are credentials correct?\n"

## -- Password generation --


def gen_password():

    upper_char = [choice(UPPER) for n in range(UPPER_NUM)]
    lower_char = [choice(LOWER) for n in range(LOWER_NUM)]
    digit_char = [choice(DIGITS) for n in range(DIGITS_NUM)]
    punc_char = [choice(PUNC) for n in range(PUNC_NUM)]

    total_char = upper_char + lower_char + digit_char + punc_char
    remaining = len(total_char)
    final_pass = ""

    while remaining:
        index = choice(range(remaining))
        char = total_char.pop(index)
        final_pass += char
        remaining -= 1

    return final_pass

def gui_pass_gen():
    """Generates password into password entry box and copies contents to
    clipboard"""

    password = gen_password()
    root.clipboard_append(string=password)
    password_input.set(value=password)


# -- File managing --

def invalid_input(website, username, password):
    """Raises alert if a field is left empty"""

    return len(website) == 0 or len(username) == 0 or len(password) == 0

assert invalid_input("", "", "") == True
assert invalid_input("Facebook", "carmen@gmail.com", "carmen123") == False

def get_entries():
    """Retrieves input from user"""

    password = entry_password.get()
    username = entry_username.get().lower()
    website = entry_website.get().lower()


    return {"website": website,
            "username": username,
            "password": password,
            }


def get_new_entry():
    """Returns formatted entries from GUI to be saved"""

    inf = get_entries()

    if invalid_input(inf["website"], inf["username"], inf["password"]):
        messagebox.showerror(title=FILL_ERROR_TITLE,
                             message=FILL_ERROR_MESSAGE)
    elif verify_notif(inf["website"], inf["username"], inf["password"]):
        return inf

def format_for_existing_website(data):
    """Formats information to be store in JSON file with an already created
    website"""

    return data["website"]

def verify_notif(website, username, password):
    """Ask the user to confirm entry information"""

    answer = messagebox.askyesno(title=VERIFY_TITLE,
                                 message=VERIFY_MESSAGE)

    return answer

def add_entry(data, entry):
    """Saves entry onto a data tupple"""

    credentials = {
        entry["username"] : entry["password"]
    }
    try:
        data[entry["website"]].update(credentials)
    except KeyError:
        data[entry["website"]] = credentials

def save_to_file(f):
    """Saves entry to the file"""

    entry = get_new_entry()

    if entry:
        try:
            with (open(f, "r") as read_file):
                data = json.load(read_file)
                add_entry(data, entry)
        except FileNotFoundError:
            with open(f, "w") as write_file:
                data = {}
                add_entry(data, entry)
                json.dump(data, write_file, indent=4)
        else:
            with open(f, "w") as write_file:
                json.dump(data, write_file, indent=4)
        finally:
            reset_boxes()

def reset_boxes():

    entry_website.delete(0, tkinter.END)
    entry_password.delete(0, tkinter.END)
    entry_username.delete(0, tkinter.END)

def show_credentials(inf):
    """Creates notification to show username and password"""
    for key, val in inf.items():
        credentials_message = f"Email/user: {key}\npassword: {val}"
        tkinter.messagebox.showinfo(CREDENTIALS_TITLE,
                                    detail=credentials_message)

def look_up():
    inf = get_entries()
    print(f'"{inf["website"]}"')
    if not inf["website"]:
        tkinter.messagebox.showerror(WEBSITE_ERROR_TITLE,
                                     details=WEBSITE_ERROR_MESSAGE)
    else:
        with open(DEFAULT_FILE) as read_file:
            data = json.load(read_file)
            x = data.get(inf["website"])
            print(f"x = {x}")
            if len(x) > 1:
                password = x.get(inf["username"])
                print(password)
                if not inf["username"]:
                    tkinter.messagebox.showerror(USER_ERROR_TITLE,
                                                 detail=USER_ERROR_MESSAGE)
                elif not password:
                    tkinter.messagebox.showerror(REGISTER_ERROR_TITLE,
                                                 detail=REGISTER_ERROR_MESSAGE)
                else:
                    show_credentials({inf["username"]: password})

            else:
                show_credentials(x)

# -- GUI ---
root = tk.Tk()

password_input = tk.StringVar()

main_frame = tk.Frame(root, bg=MINT)

main_frame.rowconfigure(0, weight=5)
main_frame.rowconfigure(1)
main_frame.rowconfigure(2)
main_frame.rowconfigure(3)
main_frame.rowconfigure(4)
main_frame.columnconfigure(0)
main_frame.columnconfigure(1, weight=4)

frame1 = tk.Frame(main_frame, bg=MINT)
frame2 = tk.Frame(main_frame, bg=MINT)

label_website = tk.Label(main_frame, text="Website", bg=MINT)
label_username = tk.Label(main_frame, text="Username/Email", bg=MINT)
label_password = tk.Label(main_frame, text="Password", bg=MINT)

entry_website = ttk.Entry(frame2)
entry_username = ttk.Entry(main_frame)
entry_password = ttk.Entry(frame1, textvariable=password_input)

button_password = tk.Button(frame1, text="Generate password", bg=YELLOW,
                            command=gui_pass_gen)
button_search = tk.Button(frame2, text="Search", bg=YELLOW, command=look_up)
button_add = tk.Button(main_frame, text="Add record", bg=YELLOW,
                       command=lambda: save_to_file(DEFAULT_FILE))

logo = tkinter.PhotoImage(file=IMG)
canvas = tk.Canvas(master=main_frame, width=WIDTH, height=HEIGHT,
                   highlightthickness=0, bg=MINT)
canvas.create_image(WIDTH/2, HEIGHT/2, image=logo)


label_website.grid(row=1, column=0, padx=X, pady=Y)
label_username.grid(row=2, column=0, padx=X, pady=Y)
label_password.grid(row=3, column=0, padx=X, pady=Y)

canvas.grid(row=0, column=1)
entry_website.pack(side=tk.LEFT, fill=tkinter.X, expand=True)
button_search.pack(side=tk.LEFT, padx=(0, X))
entry_website.focus()
entry_username.grid(row=2, column=1, padx=(X, X*2), sticky="ew")
button_add.grid(row=4,column=1, sticky="ew", padx=(X, X*2), pady=(0, Y))

frame1.grid(row=3, column=1, padx=X, pady=Y)
frame2.grid(row=1, column=1, padx=X, pady=Y, sticky="ew")
entry_password.pack(side="left",  expand=True)
button_password.pack(side="left", padx=(0, X), pady=Y)


main_frame.pack()

root.mainloop()