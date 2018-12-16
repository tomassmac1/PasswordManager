try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
import tkinter.messagebox
from random import randint
from secrets import randbelow
import json
import os.path
import os
from PIL import Image, ImageTk
from hashlib import pbkdf2_hmac as hl
import InputValidation


class GUI:

    def __init__(self, master):
        # Creates GUI and deals with user directory.
        self.master = master
        self.users = list()
        self.diction = list()
        self.new_password = str()
        self.current_user = str()

        frame = tk.Frame(self.master, width=50, bg="white")
        frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        #frame.pack(padx=100, pady=50)
        user_label = tk.Label(frame, text="Username", bg="white", fg="black")
        self.user_entry = tk.Entry(frame, textvariable=tk.StringVar)
        pass_label = tk.Label(frame, text="Password", bg="white", fg="black")
        self.password_entry = tk.Entry(frame, show="*", textvariable=tk.StringVar)
        self.password_entry.bind("<Return>", lambda event, func=self.validation: func())
        login_button = tk.Label(frame, text="", bg='white')
        self.new_user_button = tk.Label(frame, text="New User?", fg='blue', bg='white')
        self.new_user_button.bind("<Button-1>", lambda event, element=self.new_user_button, func=self.call_new_users:
                                  self.sunken(element, func))
        self.new_user_button.bind("<Enter>", lambda event, element=self.new_user_button:
                                  self.raised(element))
        self.new_user_button.bind("<Leave>", lambda event, element=self.new_user_button:
                                  self.flat(element))
        user_label.grid(row=2, column=0, sticky=tk.E)
        self.user_entry.grid(row=2, column=1)
        pass_label.grid(row=3, column=0, sticky=tk.E)
        self.password_entry.grid(row=3, column=1)
        login_button.grid(row=5, column=1)
        self.new_user_button.grid(row=6, column=1)
        self.image = Image.open("Images/PMAppLogo.jpg")
        self.image = self.image.resize((100, 100), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        self.panel = tk.Label(frame, image=self.img, bg="white")
        self.panel.grid(row=0, column=1)
        self.image2 = Image.open("Images/go_arrow.png")
        self.image2 = self.image2.resize((25, 25), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.image2)
        self.panel2 = tk.Label(frame, image=self.img2, bg="white")
        self.panel2.grid(row=4, column=1)
        self.panel2.bind("<Button-1>", lambda event, element=self.panel2, func=self.validation:
                         self.sunken(element, func))
        self.panel2.bind("<Enter>", lambda event, element=self.panel2:
                         self.raised(element))
        self.panel2.bind("<Leave>", lambda event, element=self.panel2:
                         self.flat(element))

        if os.path.exists('Data/UserDirectory'):  # checks if there is a user database
            with open('Data/UserDirectory', 'r+') as fp:  # if there is, opens it
                try:
                    self.users = json.load(fp)
                except ValueError:  # if empty, ValueError  = True, and 'users' set as empty list
                    self.users = []
        else:
            self.users = []

    def validation(self):

        inp = self.user_entry.get()
        pwd = self.password_entry.get()
        self.check_user = InputValidation.initialise(inp, str, True, 1, 40, True)
        self.check_pwd = InputValidation.initialise(pwd, str, True, 1, 40, True)
        if self.check_user == True:
            if self.check_pwd == True:
                self.login()
        else:
            tkinter.messagebox.showerror("Error!", "Invalid input.")

    def call_new_users(self):

        self.new_window = tk.Toplevel(self.master)
        self.new_user = NewUser(self.new_window)

    def call_main_menu(self):

        self.new_window = tk.Toplevel(self.master)
        self.main_menu = MainMenu(self.new_window, self.current_user, self.diction, self.users)

    @staticmethod
    def format(element: any, option: str) -> None:

        element.config(relief=option)

    @staticmethod
    def sink_and_call(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    @staticmethod
    def raised(element: any) -> None:

        element.config(relief="raised")

    @staticmethod
    def flat(element: any) -> None:

        element.config(relief="flat")

    @staticmethod
    def sunken(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    def login(self) -> None:
        # Handles user login functionality.
        count = 0
        self.current_user = self.user_entry.get()
        input_password = self.password_entry.get()
        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if self.current_user == key and input_password == v[0]:
                if os.path.exists("Data/" + v[1]):  # file existence check for password directory for username
                    with open("Data/" + v[1], 'r') as fp:  # w+ mode = if doesn't exist, then it will create file
                        try:
                            self.diction = json.load(
                                fp)  # opens json file if not empty, sets as variable 'diction'
                            self.call_main_menu()  # call main menu function
                        except ValueError:  # if empty, ValueError  = True, and 'diction' set as empty list
                            self.diction = []
                            self.call_main_menu()  # calls main menu function
                else:
                    self.diction = []  # if password directory doesnt exist, empty list set
                    self.call_main_menu()  # calls main menu
            else:
                count += 1
        if len(self.users) == 0:
            tkinter.messagebox.showinfo("Alert!", "No user data stored.")
        elif count == len(self.users):
            tkinter.messagebox.showinfo("Alert!", "Incorrect username or password.")

    def call_fun(self, func: callable) -> None:

        self.master.destroy()
        func()


class NewUser:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, bg="white")
        self.frame.pack()
        self.new_user_label = tk.Label(self.frame, text="Username", bg="white")
        self.new_user_label.grid(row=1, column=0, sticky=tk.E)
        self.new_user_entry = tk.Entry(self.frame, textvariable=tk.StringVar)
        self.new_user_entry.grid(row=1, column=1)
        self.image3 = Image.open("Images/go_arrow.png")
        self.image3 = self.image3.resize((25, 25), Image.ANTIALIAS)
        self.img3 = ImageTk.PhotoImage(self.image3)
        self.save_button = tk.Label(self.frame, image=self.img3, bg="white")
        self.save_button.grid(row=5, column=1)
        self.save_button.bind("<Button-1>", lambda event, element=self.save_button, func=self.validation:
                              self.sink_and_call(element, func))
        self.save_button.bind("<Enter>", lambda event, element=self.save_button, option="raised":
                              self.format(element, option))
        self.save_button.bind("<Leave>", lambda event, element=self.save_button, option="flat":
                              self.format(element, option))
        v_space = tk.Label(self.frame, text="", bg='white')
        v_space.grid(row=4, column=1)
        new_pass_label = tk.Label(self.frame, text="Password", bg="white")
        new_pass_label.grid(row=2, column=0, sticky=tk.E)
        self.new_password_entry = tk.Entry(self.frame, textvariable=tk.StringVar)
        self.new_password_entry.bind("<Return>", lambda event, element=self.save_button, func=self.validation:
                                     self.sink_and_call(element, func))
        self.new_password_entry.grid(row=2, column=1)

        if os.path.exists('Data/UserDirectory'):  # checks if there is a user database
            with open('Data/UserDirectory', 'r+') as fp:  # if there is, opens it
                try:
                    self.users = json.load(fp)
                except ValueError:  # if empty, ValueError  = True, and 'users' set as empty list
                    self.users = []
        else:
            self.users = []

    def validation(self):

        inp = self.new_user_entry.get()
        pwd = self.new_password_entry.get()
        check_user = InputValidation.initialise(inp, str, True, 1, 40, True)
        check_pwd = InputValidation.initialise(pwd, str, True, 1, 40, True)
        if check_user == True:
            if check_pwd == True:
                self.dump()
        else:
            tkinter.messagebox.showerror("Error!", "Invalid input.")

    def dump(self) -> None:  # Handles writing a new user's info to file.

        new_user_input = self.new_user_entry.get()
        new_password = self.new_password_entry.get()
        count = 0
        match = 0
        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if new_user_input == key:
                match += 1
            else:
                count += 1
        if match > 0:
            tkinter.messagebox.showinfo("Alert!", "Username already exists.")
            self.master.destroy()
        elif count == len(self.users):  # if looped through list and no matches found...
            number = len(self.users) + 1
            filename = "PassDict" + str(number) + '.JSON'
            self.users.append(
                {new_user_input: [new_password, filename]})
            tkinter.messagebox.showinfo("Success!", "Username and password saved.")
            with open('Data/UserDirectory', 'w+') as fp:
                json.dump(self.users, fp)  # dumping to UserDirectory file. 'W+' method creates...
            # ...file if one is not found
            self.master.destroy()

    @staticmethod
    def format(element: any, option: str) -> None:

        element.config(relief=option)

    @staticmethod
    def sink_and_call(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()


class MainMenu:

    def __init__(self, master, current_user, diction, users):

        self.master = master
        self.frame = tk.Frame(self.master, bg="white")
        self.current_user = current_user
        self.diction = diction
        self.users = users
        #self.frame.pack()
        #self.mainframe = tk.Toplevel(width=400, height=400, bg="white")
        #self.mainframe.config(padx=20, pady=20)

        generator_image = Image.open("Images/gear.png")
        generator_image = generator_image.resize((100, 100), Image.ANTIALIAS)
        self.img10 = ImageTk.PhotoImage(generator_image)
        genbutton = tk.Label(self.master, image=self.img10, bg="white")
        genbutton.grid(row=1, column=1, sticky=tk.NSEW)
        genbutton.bind("<Button-1>", lambda event, func=Generator: self.caller(func))

        add_image = Image.open("Images/add.jpg")
        add_image = add_image.resize((35, 35), Image.ANTIALIAS)
        self.img11 = ImageTk.PhotoImage(add_image)
        addbutton = tk.Label(self.master, image=self.img11, bg="white")
        addbutton.grid(row=0, column=2, sticky=tk.NSEW)
        addbutton.bind("<Button-1>", lambda event, func=Adder: self.caller(func))

        search_image = Image.open("Images/search.png")
        search_image = search_image.resize((40, 40), Image.ANTIALIAS)
        self.img12 = ImageTk.PhotoImage(search_image)
        search_button = tk.Label(self.master, image=self.img12, bg="white")
        search_button.grid(row=0, column=0, sticky=tk.NSEW)
        search_button.bind("<Button-1>", lambda event: self.searcher_if)

        clear_img = Image.open("Images/clear.png")
        clear_img = clear_img.resize((30, 30), Image.ANTIALIAS)
        self.img13 = ImageTk.PhotoImage(clear_img)
        clear_button = tk.Label(self.master, image=self.img13, bg="white")
        clear_button.grid(row=2, column=2, sticky=tk.NSEW)
        clear_button.bind("<Button-1>", lambda event: self.clearer)

        up_img = Image.open("Images/edit.png")
        up_img = up_img.resize((50, 30), Image.ANTIALIAS)
        self.img14 = ImageTk.PhotoImage(up_img)
        up_button = tk.Label(self.master, image=self.img14, bg="white")
        up_button.grid(row=2, column=0, sticky=tk.NSEW)
        up_button.bind("<Button-1>", lambda event, func=Updater: self.caller(func))

    def caller(self, class_name):

        diction = self.pass_get()
        self.new_window = tk.Toplevel(self.master)
        self.next = class_name(self.new_window, self.current_user, diction, self.users)

    def pass_get(self):

        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if self.current_user == key:
                if os.path.exists("Data/" + v[1]):  # file existence check for password directory for username
                    with open("Data/" + v[1], 'r') as fp:  # w+ mode = if doesn't exist, then it will create file
                        try:
                            self.diction = json.load(
                                fp)  # opens json file if not empty, sets as variable 'diction'
                        except ValueError:  # if empty, ValueError  = True, and 'diction' set as empty list
                            self.diction = []
                else:
                    self.diction = []  # if password directory doesnt exist, empty list set
        return self.diction

    def searcher_if(self):

        diction = self.pass_get()
        if len(diction) == 0:
            tkinter.messagebox.showinfo("Empty!", "No stored passwords!")
        else:
            self.caller(Searcher)

    def clearer(self):

        clear_4_realz = tkinter.messagebox.askquestion("Sure?", "Are you sure?")
        if clear_4_realz == "yes":
            self.diction = []
            tkinter.messagebox.showinfo("Done.", 'Passwords cleared.')


class Generator:

    def __init__(self, master, current_user, diction, users):

        self.master = master
        self.diction = diction
        self.users = users
        self.current_user = current_user
        self.create_frame(self.master)
        #self.gen_frame = Toplevel(width=400, height=400, bg="white")
        #self.gen_frame.config(padx=20, pady=20)

    def create_frame(self, master):

        self.master = master
        self.frame = tk.Frame(self.master, bg="white")
        new_label = tk.Label(self.master, text="Password Length", bg="white", fg="black")
        self.new_pass_length = tk.Entry(self.master, textvariable=tk.StringVar)
        new_label.grid(row=2, column=0, sticky=tk.E)
        self.new_pass_length.grid(row=2, column=1)
        image4 = Image.open("Images/go_arrow.png")
        image4 = image4.resize((25, 25), Image.ANTIALIAS)
        self.img4 = ImageTk.PhotoImage(image4)
        self.go_button = tk.Label(self.master, image=self.img4, bg="white")
        self.go_button.grid(row=3, column=1)
        self.go_button.bind("<Button-1>", lambda event, element=self.go_button, func=self.check_length:
                            self.sunken(element, func))
        self.go_button.bind("<Enter>", lambda event, element=self.go_button:
                            self.raised(element))
        self.go_button.bind("<Leave>", lambda event, element=self.go_button:
                            self.flat(element))
        self.new_pass_length.bind("<Return>", lambda event, element=self.go_button, func=self.check_length:
                                  self.sunken(element, func))

    @staticmethod
    def raised(element: any) -> None:

        element.config(relief="raised")

    @staticmethod
    def flat(element: any) -> None:

        element.config(relief="flat")

    @staticmethod
    def sunken(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    def check_length(self) -> None:  # checks user input for new password length
        try:
            new_password_length = int(self.new_pass_length.get())
            if type(new_password_length) == int:
                if new_password_length < 6:
                    tkinter.messagebox.showerror("Error!", "Invalid entry. Password must be greater than 6 chars.")
                    self.new_window = tk.Toplevel(self.master)
                    self.next = Generator(self.new_window, self.current_user, self.diction, self.users)
                else:
                    self.generate(new_password_length)
                    self.master.destroy()
        except ValueError:
            tkinter.messagebox.showerror("Error", "Invalid entry!")
            self.master.destroy()

    def generate(self, length) -> None:

        password = []
        self.new_password = []
        alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "1", "2", "3", "4", "5", "6", "7", "8",
                 "9", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        for char in range(0, length):
            c = alpha[randint(0, len(alpha) - 1)]
            password.append(c)
        for _ in password:
            if password.index(_) % randint(2, 4) == 0:
                _ = _.upper()
                self.new_password.append(_)
            else:
                self.new_password.append(_)
        self.new_password = ''.join(str(e) for e in self.new_password)
        tkinter.messagebox.showinfo("New password:", self.new_password)

        answer: str = tkinter.messagebox.askquestion("Store?", "Would you like to store password?")
        if answer == "yes":
            self.referencename()
        elif answer == "no":
            self.master.destroy()

    def referencename(self) -> None:

        self.ref_frame = tk.Toplevel(width=400, height=400, bg="white")
        pass_ref_label = tk.Label(self.ref_frame, text="Password Reference", bg="white", fg="black")
        self.ref_frame.config(padx=20, pady=20)
        self.new_password_ref = tk.Entry(self.ref_frame, textvariable=tk.StringVar)
        pass_ref_label.grid(row=2, column=0, sticky=tk.E)
        self.new_password_ref.grid(row=2, column=1)
        image5 = Image.open("Images/go_arrow.png")
        image5 = image5.resize((25, 25), Image.ANTIALIAS)
        self.img5 = ImageTk.PhotoImage(image5)
        self.ref_button = tk.Label(self.ref_frame, image=self.img5, bg="white")
        self.ref_button.bind("<Button-1>", lambda event, element=self.ref_button, func=self.check_ref:
                             self.sunken(element, func))
        self.ref_button.bind("<Enter>", lambda event, element=self.ref_button:
                             self.raised(element))
        self.ref_button.bind("<Leave>", lambda event, element=self.ref_button:
                             self.flat(element))
        self.new_password_ref.bind("<Return>", lambda event, element=self.ref_button, func=self.check_ref:
                                   self.sunken(element, func))
        self.ref_button.grid(row=3, column=1)

    def check_ref(self) -> None:

        target_key = self.new_password_ref.get()
        total = 0
        key_list = []
        for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
            key_list.append(key)
            if key == target_key:
                total += 1
        if total > 0:
            tkinter.messagebox.showinfo("Oi!", "Password already exists with that reference.")
            self.ref_frame.destroy()
            self.referencename()
        else:
            data = {target_key: self.new_password}
            self.diction.append(data)
            self.dump()
            tkinter.messagebox.showinfo("Success!", "Saved the password.")
            self.ref_frame.destroy()
            self.master.destroy()

    def dump(self):

        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if key == self.current_user:
                with open("Data/" + v[1], 'w+') as f:
                    json.dump(self.diction, f)


class Adder:

    def __init__(self, master, current_user, diction, users):

        self.diction = diction
        self.current_user = current_user
        self.users = users
        self.master = master
        self.frame = tk.Frame(self.master, bg="white")
        #self.add_frame = tk.Toplevel(width=400, height=400, bg="white")
        #self.add_frame.config(padx=20, pady=20)
        add_pass_ref_label = tk.Label(self.master, text="Password Reference", bg="white", fg="black")
        add_pass_ref_label.grid(row=2, column=0, sticky=tk.E)
        self.add_pass_ref = tk.Entry(self.master, textvariable=tk.StringVar)
        self.add_pass_ref.grid(row=2, column=1)
        password_label = tk.Label(self.master, text="Password", bg="white", fg="black")
        password_label.grid(row=3, column=0, sticky=tk.E)
        self.pass1 = tk.Entry(self.master, textvariable=tk.StringVar)
        self.pass1.grid(row=3, column=1)
        image6 = Image.open("Images/go_arrow.png")
        image6 = image6.resize((25, 25), Image.ANTIALIAS)
        self.img6 = ImageTk.PhotoImage(image6)
        self.add_continue_button = tk.Label(self.master, image=self.img6, bg="white")
        self.add_continue_button.bind("<Button-1>",
                                      lambda event, element=self.add_continue_button, func=self.add_new:
                                      self.sunken(element, func))
        self.add_continue_button.bind("<Enter>", lambda event, element=self.add_continue_button:
                                      self.raised(element))
        self.add_continue_button.bind("<Leave>", lambda event, element=self.add_continue_button:
                                      self.flat(element))
        self.add_continue_button.grid(row=4, column=1)
        self.pass1.bind("<Return>", lambda event, element=self.add_continue_button, func=self.add_new:
                        self.sunken(element, func))

    @staticmethod
    def raised(element: any) -> None:

        element.config(relief="raised")

    @staticmethod
    def flat(element: any) -> None:

        element.config(relief="flat")

    @staticmethod
    def sunken(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    def add_new(self) -> None:

        new_ref = self.add_pass_ref.get()
        new_pass = self.pass1.get()
        required = '1234567890;#[]-=,./<>?:@~{})_+&^%$£"!'
        t = False
        for _ in new_pass:
            if _ in required:
                t = True
        if len(new_pass) < 4 or len(new_ref) < 3:
            tkinter.messagebox.showinfo("Error!", "Reference or password too short!")
            self.master.destroy()
        elif t is False:
            tkinter.messagebox.showinfo("Error!", "Password needs at least one special character!")
            self.master.destroy()
        elif self.diction == []:
            data = {new_ref: new_pass}
            self.diction.append(data)
            tkinter.messagebox.showinfo("Yay!", "Password Added.")
            self.dump()
            self.master.destroy()
        else:
            total = 0
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                if new_ref == key:
                    total += 1
            if total > 0:
                tkinter.messagebox.showinfo("Oi!",
                                                        "Reference already taken, select 'edit password' instead.")
                self.master.destroy()
            else:
                if len(new_ref) > 40 or len(new_pass) > 40:
                    tkinter.messagebox.showinfo("Much too much..",
                                                "Password or reference too long.")
                    self.master.destroy()
                else:
                    data = {new_ref: new_pass}  # creating a new dictionary entry
                    self.diction.append(data)  # appending new entry to 'diction'
                    # reason for having 'diction' as list = easy to manipulate objects
                    tkinter.messagebox.showinfo("Yay!", "Password Added.")
                    self.dump()
                    self.master.destroy()

    def dump(self):

        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if key == self.current_user:
                with open("Data/" + v[1], 'w+') as f:
                    json.dump(self.diction, f)


class Updater:

    def __init__(self, master, current_user, diction, users):

        self.users = users
        self.current_user = current_user
        self.master = master
        self.diction = diction
        if len(self.diction) == 0:
            tkinter.messagebox.showinfo("Empty!", "No stored data!")
        else:
            #self.update_frame = tk.Toplevel(width=400, height=400, bg="white")
            #self.update_frame.config(padx=20, pady=20)
            self.frame = tk.Frame(self.master, bg="white")
            add_pass_ref_label = tk.Label(self.master, text="Password Reference (L for List of refs)",
                                          bg="white")
            self.password_ref = tk.Entry(self.master, textvariable=tk.StringVar)
            add_pass_ref_label.grid(row=2, column=0, sticky=tk.E)
            self.password_ref.grid(row=2, column=1)
            image7 = Image.open("Images/go_arrow.png")
            image7 = image7.resize((25, 25), Image.ANTIALIAS)
            self.img7 = ImageTk.PhotoImage(image7)
            self.update_continue = tk.Label(self.master, image=self.img7, bg="white")
            self.update_continue.bind("<Button-1>", lambda event, element=self.update_continue, func=self.update_if:
                                      self.sunken(element, func))
            self.update_continue.bind("<Enter>", lambda event, element=self.update_continue:
                                      self.raised(element))
            self.update_continue.bind("<Leave>", lambda event, element=self.update_continue:
                                      self.raised(element))
            self.update_continue.grid(row=3, column=1)
            self.password_ref.bind("<Return>", lambda event, element=self.update_continue, func=self.update_if:
                                   self.sunken(element, func))

    @staticmethod
    def raised(element: any) -> None:

        element.config(relief="raised")

    @staticmethod
    def flat(element: any) -> None:

        element.config(relief="flat")

    @staticmethod
    def sunken(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    def update_if(self) -> None:

        self.change_ref = self.password_ref.get()
        ref = self.change_ref
        if len(ref) == 0:
            tkinter.messagebox.showinfo("Error!", "Nothing entered.")
            self.master.destroy()
            self.__init__(self.master, self.current_user, self.diction, self.users)
        elif ref == "L" or ref == "l":
            all_keys = []
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                all_keys.append(key)  # appends keys to list of keys ('keylist')
            all_keys = ', '.join(str(keyz) for keyz in all_keys)
            tkinter.messagebox.showinfo("Refs:", all_keys)
            self.master.destroy()
        else:
            total = 0
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                if key == ref:
                    self.master.destroy()
                    self.update_yes()
                else:
                    total += 1
            if total == len(self.diction):
                tkinter.messagebox.showinfo("Oi!", "No matches found.")  # same no match function as before
                self.master.destroy()

    def update_yes(self) -> None:

        self.update_y_frame = tk.Toplevel(width=400, height=400, bg="white")
        self.update_y_frame.config(padx=20, pady=20)
        password_label = tk.Label(self.update_y_frame, text="New Password", bg="white")
        password_label.grid(row=2, column=0, sticky=tk.E)
        self.new_pass_2 = tk.Entry(self.update_y_frame, textvariable=tk.StringVar)
        self.new_pass_2.grid(row=2, column=1)
        image8 = Image.open("Images/go_arrow.png")
        image8 = image8.resize((25, 25), Image.ANTIALIAS)
        self.img8 = ImageTk.PhotoImage(image8)
        self.update_go_button = tk.Label(self.update_y_frame, image=self.img8, bg="white")
        self.update_go_button.bind("<Button-1>",
                                   lambda event, element=self.update_go_button, func=self.update_4_realz:
                                   self.sunken(element, func))
        self.update_go_button.bind("<Enter>", lambda event, element=self.update_go_button:
        self.raised(element))
        self.update_go_button.bind("<Leave>", lambda event, element=self.update_go_button:
        self.flat(element))
        self.update_go_button.grid(row=3, column=1)
        self.new_pass_2.bind("<Return>", lambda event, element=self.update_go_button, func=self.update_4_realz:
        self.sunken(element, func))

    def update_4_realz(self) -> None:

        update_pass = self.new_pass_2.get()
        if len(update_pass) == 0:
            tkinter.messagebox.showinfo("Error!", "Nothing entered.")
            self.update_y_frame.destroy()
        else:
            for key, v in [(key, v) for self.item in self.diction for (key, v) in self.item.items()]:
                if key == self.change_ref:
                    i = self.diction.index(self.item)  # finds index of match in 'diction' list
                    del self.diction[i]
                    new_dic = {self.change_ref: update_pass}  # sets new entry
                    self.diction.append(new_dic)  # updates password/key combo to new entry
                    self.dump()
                    tkinter.messagebox.showinfo("Password updated:", update_pass)
                    self.update_y_frame.destroy()
                    self.master.destroy()

    def dump(self):

        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if key == self.current_user:
                with open("Data/" + v[1], 'w+') as f:
                    json.dump(self.diction, f)


class Searcher:

    def __init__(self, master, current_user, diction, users):

        self.master = master
        self.diction = diction
        self.current_user = current_user
        self.users = users
        self.frame = tk.Frame(self.master, bg="white")
        #self.retrieve_frame = tk.Toplevel(width=400, height=400, bg="white")
        #self.retrieve_frame.config(padx=20, pady=20)
        search_ref_label = tk.Label(self.master, text="Password Reference (L to List All)", bg="white")
        self.pass_ref = tk.Entry(self.master, textvariable=tk.StringVar)
        search_ref_label.grid(row=2, column=0, sticky=tk.E)
        self.pass_ref.grid(row=2, column=1)
        image9 = Image.open("go_arrow.png")
        image9 = image9.resize((25, 25), Image.ANTIALIAS)
        self.img9 = ImageTk.PhotoImage(image9)
        self.continue_button = tk.Label(self.master, image=self.img9, bg="white")
        self.continue_button.bind("<Button-1>", lambda event, element=self.continue_button, func=self.check_ref_2:
                                  self.sunken(element, func))
        self.continue_button.bind("<Enter>", lambda event, element=self.continue_button:
                                  self.raised(element))
        self.continue_button.bind("<Leave>", lambda event, element=self.continue_button:
                                  self.flat(element))
        self.pass_ref.bind("<Return>", lambda event, element=self.continue_button, func=self.check_ref_2:
                           self.sunken(element, func))
        self.continue_button.grid(row=3, column=1)

    @staticmethod
    def raised(element: any) -> None:

        element.config(relief="raised")

    @staticmethod
    def flat(element: any) -> None:

        element.config(relief="flat")

    @staticmethod
    def sunken(element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    def check_ref_2(self) -> None:

        total = 0
        all_keys = []
        pass_ref = self.pass_ref.get()
        if pass_ref == "L" or pass_ref == "l":
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                all_keys.append(key)
            all_keys = '--'.join(str(keyz) for keyz in all_keys)
            tkinter.messagebox.showinfo("Refs", all_keys)
            self.master.destroy()
            self.__init__(self.master, self.current_user, self.diction, self.users)
        else:
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                if key == self.pass_ref:
                    tkinter.messagebox.showinfo("Password Found!", key + " : " + v)
                    self.master.destroy()
                    # if password found, reference and password are printed
                else:
                    total += 1  # in order to avoid multiple "no match" statements, counter increments
            if total == len(self.diction):
                tkinter.messagebox.showinfo("No matches!", "No matches found.")
                self.master.destroy()


#window = tk.Tk()
#window.configure(background="white")
#window.title("Gashlane")
#b = GUI(window)
#window.mainloop()

root = tk.Tk()
root.configure(background="white")
root.title("Gashlane")
app = GUI(root)
root.mainloop()
