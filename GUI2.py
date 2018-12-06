# GUI


from tkinter import *
import tkinter.messagebox
from random import randint
import json
import os.path
import os
from PIL import Image, ImageTk
import bcrypt


class GUI:

    def __init__(self, master):
        # Creates GUI and deals with user directory.
        self.users = list()
        self.diction = list()
        self.new_password = str()
        frame = Frame(master, width=50, bg="white")
        frame.grid(column=0, row=0, sticky=(N, W, E, S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.pack(padx=100, pady=50)
        user_label = Label(frame, text="Username", bg="white", fg="black")
        self.user_entry = Entry(frame, textvariable=StringVar)
        pass_label = Label(frame, text="Password", bg="white", fg="black")
        self.password_entry = Entry(frame, show="*", textvariable=StringVar)
        self.password_entry.bind("<Return>", lambda event, func=self.login: func())
        login_button = Label(frame, text="", bg='white')
        self.new_user_button = Label(frame, text="New User?", fg='blue', bg='white')
        self.new_user_button.bind("<Button-1>", lambda event, element=self.new_user_button, func=self.new_user:
                                  self.sunken(element, func))
        self.new_user_button.bind("<Enter>", lambda event, element=self.new_user_button:
                                  self.raised(element))
        self.new_user_button.bind("<Leave>", lambda event, element=self.new_user_button:
                                  self.flat(element))
        user_label.grid(row=2, column=0, sticky=E)
        self.user_entry.grid(row=2, column=1)
        pass_label.grid(row=3, column=0, sticky=E)
        self.password_entry.grid(row=3, column=1)
        login_button.grid(row=5, column=1)
        self.new_user_button.grid(row=6, column=1)
        self.image = Image.open("Images/PMAppLogo.jpg")
        self.image = self.image.resize((100, 100), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        self.panel = Label(frame, image=self.img, bg="white")
        self.panel.grid(row=0, column=1)
        self.image2 = Image.open("Images/go_arrow.png")
        self.image2 = self.image2.resize((25, 25), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.image2)
        self.panel2 = Label(frame, image=self.img2, bg="white")
        self.panel2.grid(row=4, column=1)
        self.panel2.bind("<Button-1>", lambda event, element=self.panel2, func=self.login:
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

    def raised(self, element: any) -> None:

        element.config(relief="raised")

    def flat(self, element: any) -> None:

        element.config(relief="flat")

    def sunken(self, element: any, func: callable) -> None:

        element.config(relief="sunken")
        func()

    def login(self) -> None:
        # Handles user login functionality.
        count = 0
        current_user = self.user_entry.get()
        input_password = self.password_entry.get()
        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if current_user == key and input_password == v[0]:
                if os.path.exists("Data/" + v[1]):  # file existence check for password directory for username
                    with open("Data/" + v[1], 'r') as fp:  # w+ mode = if doesn't exist, then it will create file
                        try:
                            self.diction = json.load(
                                fp)  # opens json file if not empty, sets as variable 'diction'
                            self.main_menu()  # call main menu function
                        except ValueError:  # if empty, ValueError  = True, and 'diction' set as empty list
                            self.diction = []
                            self.main_menu()  # calls main menu function
                else:
                    self.diction = []  # if password directory doesnt exist, empty list set
                    self.main_menu()  # calls main menu
            else:
                count += 1
        if len(self.users) == 0:
            tkinter.messagebox.showinfo("Alert!", "No user data stored.")
        elif count == len(self.users):
            tkinter.messagebox.showinfo("Alert!", "Incorrect username or password.")

    def new_user(self) -> None:  # Handles creation of new user interface.

        self.new_user_frame = Toplevel(width=400, height=400, bg="white")
        self.new_user_frame.config(padx=50, pady=50)
        new_user_label = Label(self.new_user_frame, text="Username", bg="white")
        new_user_label.grid(row=1, column=0, sticky=E)
        self.new_user_entry = Entry(self.new_user_frame, textvariable=StringVar)
        self.new_user_entry.grid(row=1, column=1)
        self.image3 = Image.open("Images/go_arrow.png")
        self.image3 = self.image3.resize((25, 25), Image.ANTIALIAS)
        self.img3 = ImageTk.PhotoImage(self.image3)
        self.save_button = Label(self.new_user_frame, image=self.img3, bg="white")
        self.save_button.grid(row=5, column=1)
        self.save_button.bind("<Button-1>", lambda event, element=self.save_button, func=self.dump:
                              self.sunken(element, func))
        self.save_button.bind("<Enter>", lambda event, element=self.save_button:
                              self.raised(element))
        self.save_button.bind("<Leave>", lambda event, element=self.save_button:
                              self.flat(element))
        v_space = Label(self.new_user_frame, text="", bg='white')
        v_space.grid(row=4, column=1)
        new_pass_label = Label(self.new_user_frame, text="Password", bg="white")
        new_pass_label.grid(row=2, column=0, sticky=E)
        self.new_password_entry = Entry(self.new_user_frame, textvariable=StringVar)
        self.new_password_entry.bind("<Return>", lambda event, element=self.save_button, func=self.dump:
                                self.sunken(element, func))
        self.new_password_entry.grid(row=2, column=1)

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
            self.new_user_frame.destroy()
            self.new_user()
        elif count == len(self.users):  # if looped through list and no matches found...
            number = len(self.users) + 1
            filename = "PassDict" + str(number) + '.JSON'
            self.users.append(
                {new_user_input: [new_password, filename]})
            tkinter.messagebox.showinfo("Success!", "Username and password saved.")
            with open('Data/UserDirectory', 'w+') as fp:
                json.dump(self.users, fp)  # dumping to UserDirectory file. 'W+' method creates...
            # ...file if one is not found
            self.new_user_frame.destroy()

    def main_menu(self) -> None:  # depending on option chosen, calls appropriate methods

        self.mainframe = Toplevel(width=400, height=400, bg="white")
        self.mainframe.config(padx=20, pady=20)

        generator_image = Image.open("Images/gear.png")
        generator_image = generator_image.resize((100, 100), Image.ANTIALIAS)
        self.img10 = ImageTk.PhotoImage(generator_image)
        genbutton = Label(self.mainframe, image=self.img10, bg="white")
        genbutton.grid(row=1, column=1, sticky=NSEW)
        genbutton.bind("<Button-1>", lambda event, func=self.gen: self.call_fun(func))

        add_image = Image.open("Images/add.jpg")
        add_image = add_image.resize((35, 35), Image.ANTIALIAS)
        self.img11 = ImageTk.PhotoImage(add_image)
        addbutton = Label(self.mainframe, image=self.img11, bg="white")
        addbutton.grid(row=0, column=2, sticky=NSEW)
        addbutton.bind("<Button-1>", lambda event, func=self.add_another: self.call_fun(func))

        search_image = Image.open("Images/search.png")
        search_image = search_image.resize((40, 40), Image.ANTIALIAS)
        self.img12 = ImageTk.PhotoImage(search_image)
        search_button = Label(self.mainframe, image=self.img12, bg="white")
        search_button.grid(row=0, column=0, sticky=NSEW)
        search_button.bind("<Button-1>", lambda event, func=self.retrieve: self.call_fun(func))

        clear_img = Image.open("Images/clear.png")
        clear_img = clear_img.resize((30, 30), Image.ANTIALIAS)
        self.img13 = ImageTk.PhotoImage(clear_img)
        clear_button = Label(self.mainframe, image=self.img13, bg="white")
        clear_button.grid(row=2, column=2, sticky=NSEW)
        clear_button.bind("<Button-1>", lambda event, func=self.clear: self.call_fun(func))

        up_img = Image.open("Images/edit.png")
        up_img = up_img.resize((50, 30), Image.ANTIALIAS)
        self.img14 = ImageTk.PhotoImage(up_img)
        up_button = Label(self.mainframe, image=self.img14, bg="white")
        up_button.grid(row=2, column=0, sticky=NSEW)
        up_button.bind("<Button-1>", lambda event, func=self.update: self.call_fun(func))

        current_user = self.user_entry.get()
        for key, v in [(key, v) for item in self.users for (key, v) in item.items()]:
            if key == current_user:
                with open("Data/" + v[1], 'w+') as f:
                    json.dump(self.diction, f)

    def call_fun(self, func: callable) -> None:

        self.mainframe.destroy()
        func()

    def gen(self) -> None:  # Creates password generation GUI

        self.gen_frame = Toplevel(width=400, height=400, bg="white")
        self.gen_frame.config(padx=20, pady=20)
        new_label = Label(self.gen_frame, text="Password Length", bg="white", fg="black")
        self.new_pass_length = Entry(self.gen_frame, textvariable=StringVar)
        new_label.grid(row=2, column=0, sticky=E)
        self.new_pass_length.grid(row=2, column=1)
        image4 = Image.open("Images/go_arrow.png")
        image4 = image4.resize((25, 25), Image.ANTIALIAS)
        self.img4 = ImageTk.PhotoImage(image4)
        self.go_button = Label(self.gen_frame, image=self.img4, bg="white")
        self.go_button.grid(row=3, column=1)
        self.go_button.bind("<Button-1>", lambda event, element=self.go_button, func=self.check_length:
                            self.sunken(element, func))
        self.go_button.bind("<Enter>", lambda event, element=self.go_button:
                            self.raised(element))
        self.go_button.bind("<Leave>", lambda event, element=self.go_button:
                            self.flat(element))
        self.new_pass_length.bind("<Return>", lambda event, element=self.go_button, func=self.check_length:
                                  self.sunken(element, func))

    def check_length(self) -> None:  # checks user input for new password length
        try:
            new_password_length = int(self.new_pass_length.get())
            if type(new_password_length) == int:
                if new_password_length < 6:
                    tkinter.messagebox.showerror("Error!", "Invalid entry. Password must be greater than 6 chars.")
                    self.gen()
                else:
                    self.generate(new_password_length)
                    self.gen_frame.destroy()
        except ValueError:
            tkinter.messagebox.showerror("Error", "Invalid entry!")
            self.gen_frame.destroy()
            self.gen()

    def generate(self, length) -> None:

        password = []
        new_password = []
        alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "1", "2", "3", "4", "5", "6", "7", "8",
                 "9", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        for char in range(0, length):
            c = alpha[randint(0, len(alpha) - 1)]
            password.append(c)
        for _ in password:
            if password.index(_) % randint(2, 4) == 0:
                _ = _.upper()
                new_password.append(_)
            else:
                new_password.append(_)
        new_password = ''.join(str(e) for e in new_password)
        tkinter.messagebox.showinfo("New password:", new_password)

        answer: str = tkinter.messagebox.askquestion("Store?", "Would you like to store password?")
        if answer == "yes":
            self.referencename()
        elif answer == "no":
            self.main_menu()

    def referencename(self) -> None:

        self.ref_frame = Toplevel(width=400, height=400, bg="white")
        pass_ref_label = Label(self.ref_frame, text="Password Reference", bg="white", fg="black")
        self.ref_frame.config(padx=20, pady=20)
        self.new_password_ref = Entry(self.ref_frame, textvariable=StringVar)
        pass_ref_label.grid(row=2, column=0, sticky=E)
        self.new_password_ref.grid(row=2, column=1)
        image5 = Image.open("Images/go_arrow.png")
        image5 = image5.resize((25, 25), Image.ANTIALIAS)
        self.img5 = ImageTk.PhotoImage(image5)
        self.ref_button = Label(self.ref_frame, image=self.img5, bg="white")
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
            tkinter.messagebox.showinfo("Success!", "Saved the password.")
            self.ref_frame.destroy()
            self.mainframe.destroy()
            self.main_menu()

    def retrieve(self) -> None:

        if len(self.diction) == 0:
            tkinter.messagebox.showinfo("Empty!", "No stored passwords!")
            self.mainframe.destroy()
            self.main_menu()
        else:
            self.retrieve_frame = Toplevel(width=400, height=400, bg="white")
            self.retrieve_frame.config(padx=20, pady=20)
            search_ref_label = Label(self.retrieve_frame, text="Password Reference (L to List All)", bg="white")
            self.pass_ref = Entry(self.retrieve_frame, textvariable=StringVar)
            search_ref_label.grid(row=2, column=0, sticky=E)
            self.pass_ref.grid(row=2, column=1)
            image9 = Image.open("go_arrow.png")
            image9 = image9.resize((25, 25), Image.ANTIALIAS)
            self.img9 = ImageTk.PhotoImage(image9)
            self.continue_button = Label(self.retrieve_frame, image=self.img9, bg="white")
            self.continue_button.bind("<Button-1>", lambda event, element=self.continue_button, func=self.check_ref_2:
                                      self.sunken(element, func))
            self.continue_button.bind("<Enter>", lambda event, element=self.continue_button:
                                      self.raised(element))
            self.continue_button.bind("<Leave>", lambda event, element=self.continue_button:
                                      self.flat(element))
            self.pass_ref.bind("<Return>", lambda event, element=self.continue_button, func=self.check_ref_2:
                               self.sunken(element, func))
            self.continue_button.grid(row=3, column=1)

    def check_ref_2(self) -> None:

        total = 0
        all_keys = []
        pass_ref = self.pass_ref.get()
        if pass_ref == "L" or pass_ref == "l":
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                all_keys.append(key)
            all_keys = '--'.join(str(keyz) for keyz in all_keys)
            tkinter.messagebox.showinfo("Refs", all_keys)
            self.retrieve_frame.destroy()
            self.retrieve()
        else:
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                if key == self.pass_ref:
                    tkinter.messagebox.showinfo("Password Found!", key + " : " + v)
                    self.retrieve_frame.destroy()
                    self.main_menu()
                    # if password found, reference and password are printed
                else:
                    total += 1  # in order to avoid multiple "no match" statements, counter increments
            if total == len(self.diction):
                tkinter.messagebox.showinfo("No matches!", "No matches found.")
                self.retrieve_frame.destroy()
                self.mainframe.destroy()
                self.main_menu()

    def add_another(self) -> None:

        self.add_frame = Toplevel(width=400, height=400, bg="white")
        self.add_frame.config(padx=20, pady=20)
        add_pass_ref_label = Label(self.add_frame, text="Password Reference", bg="white", fg="black")
        add_pass_ref_label.grid(row=2, column=0, sticky=E)
        self.add_pass_ref = Entry(self.add_frame, textvariable=StringVar)
        self.add_pass_ref.grid(row=2, column=1)
        password_label = Label(self.add_frame, text="Password", bg="white", fg="black")
        password_label.grid(row=3, column=0, sticky=E)
        self.pass1 = Entry(self.add_frame, textvariable=StringVar)
        self.pass1.grid(row=3, column=1)
        image6 = Image.open("Images/go_arrow.png")
        image6 = image6.resize((25, 25), Image.ANTIALIAS)
        self.img6 = ImageTk.PhotoImage(image6)
        self.add_continue_button = Label(self.add_frame, image=self.img6, bg="white")
        self.add_continue_button.bind("<Button-1>", lambda event, element=self.add_continue_button, func=self.add_new:
                                      self.sunken(element, func))
        self.add_continue_button.bind("<Enter>", lambda event, element=self.add_continue_button:
                                      self.raised(element))
        self.add_continue_button.bind("<Leave>", lambda event, element=self.add_continue_button:
                                      self.flat(element))
        self.add_continue_button.grid(row=4, column=1)
        self.pass1.bind("<Return>", lambda event, element=self.add_continue_button, func=self.add_new:
                        self.sunken(element, func))

    def add_new(self) -> None:

        new_ref = self.add_pass_ref.get()
        new_pass = self.pass1.get()
        required = '1234567890;#[]-=,./<>?:@~{})_+&^%$£"!'
        t = False
        for _ in new_pass:
            if _ in required:
                t = True
        if len(new_pass) < 8 or len(new_ref) < 3:
            tkinter.messagebox.showinfo("Error!", "Reference or password too short!")
            self.add_frame.destroy()
            self.add_another()
        elif t is False:
            tkinter.messagebox.showinfo("Error!", "Password needs at least one special character!")
            self.add_frame.destroy()
            self.add_another()
        else:
            total = 0
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                if new_ref == key:
                    total += 1
            if total > 0:
                choice = tkinter.messagebox.askquestion("Oi!",
                                                        "Reference already taken, would you like to update pwd?")
                if choice == "yes":
                    self.mainframe.destroy()
                    self.add_frame.destroy()
                    self.update()
                else:
                    self.add_another()
            else:
                if len(new_ref) > 40 or len(new_pass) > 40:
                    tkinter.messagebox.showinfo("Much too much..",
                                                "Password or reference too long.")
                    self.add_frame.destroy()
                    self.add_another()
                else:
                    data = {new_ref: new_pass}  # creating a new dictionary entry
                    self.diction.append(data)  # appending new entry to 'diction'
                    # reason for having 'diction' as list = easy to manipulate objects
                    tkinter.messagebox.showinfo("Yay!", "Password Added.")
                    self.mainframe.destroy()
                    self.add_frame.destroy()
                    self.main_menu()

    def update(self) -> None:

        if len(self.diction) == 0:
            tkinter.messagebox.showinfo("Empty!", "No stored data!")
            self.mainframe.destroy()
            self.main_menu()
        else:
            self.update_frame = Toplevel(width=400, height=400, bg="white")
            self.update_frame.config(padx=20, pady=20)
            add_pass_ref_label = Label(self.update_frame, text="Password Reference (L for List of refs)", bg="white")
            self.password_ref = Entry(self.update_frame, textvariable=StringVar)
            add_pass_ref_label.grid(row=2, column=0, sticky=E)
            self.password_ref.grid(row=2, column=1)
            image7 = Image.open("Images/go_arrow.png")
            image7 = image7.resize((25, 25), Image.ANTIALIAS)
            self.img7 = ImageTk.PhotoImage(image7)
            self.update_continue = Label(self.update_frame, image=self.img7, bg="white")
            self.update_continue.bind("<Button-1>", lambda event, element=self.update_continue, func=self.update_if:
                                      self.sunken(element, func))
            self.update_continue.bind("<Enter>", lambda event, element=self.update_continue:
                                      self.raised(element))
            self.update_continue.bind("<Leave>", lambda event, element=self.update_continue:
                                      self.raised(element))
            self.update_continue.grid(row=3, column=1)
            self.password_ref.bind("<Return>", lambda event, element=self.update_continue, func=self.update_if:
                                   self.sunken(element, func))

    def update_if(self) -> None:

        self.change_ref = self.password_ref.get()
        ref = self.change_ref
        if len(ref) == 0:
            tkinter.messagebox.showinfo("Error!", "Nothing entered.")
            self.update_frame.destroy()
            self.update()
        elif ref == "L" or ref == "l":
            all_keys = []
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                all_keys.append(key)  # appends keys to list of keys ('keylist')
            all_keys = ', '.join(str(keyz) for keyz in all_keys)
            tkinter.messagebox.showinfo("Refs:", all_keys)
            self.update_frame.destroy()
            self.update()
        else:
            total = 0
            for key, v in [(key, v) for item in self.diction for (key, v) in item.items()]:
                if key == ref:
                    self.update_frame.destroy()
                    self.update_yes()
                else:
                    total += 1
            if total == len(self.diction):
                tkinter.messagebox.showinfo("Oi!", "No matches found.")  # same no match function as before
                self.update_frame.destroy()
                self.update()

    def update_yes(self) -> None:

        self.update_y_frame = Toplevel(width=400, height=400, bg="white")
        self.update_y_frame.config(padx=20, pady=20)
        password_label = Label(self.update_y_frame, text="New Password", bg="white")
        password_label.grid(row=2, column=0, sticky=E)
        self.new_pass_2 = Entry(self.update_y_frame, textvariable=StringVar)
        self.new_pass_2.grid(row=2, column=1)
        image8 = Image.open("Images/go_arrow.png")
        image8 = image8.resize((25, 25), Image.ANTIALIAS)
        self.img8 = ImageTk.PhotoImage(image8)
        self.update_go_button = Label(self.update_y_frame, image=self.img8, bg="white")
        self.update_go_button.bind("<Button-1>", lambda event, element=self.update_go_button, func=self.update_4_realz:
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
            self.update()
        else:
            for key, v in [(key, v) for self.item in self.diction for (key, v) in self.item.items()]:
                if key == self.change_ref:
                    i = self.diction.index(self.item)  # finds index of match in 'diction' list
                    del self.diction[i]
                    new_dic = {self.change_ref: update_pass}  # sets new entry
                    self.diction.append(new_dic)  # updates password/key combo to new entry
                    tkinter.messagebox.showinfo("Password updated:", update_pass)
                    self.update_y_frame.destroy()
                    self.update_frame.destroy()
                    self.mainframe.destroy()
                    self.main_menu()

    def clear(self) -> None:

        clear_4_realz = tkinter.messagebox.askquestion("Sure?", "Are you sure?")
        if clear_4_realz == "yes":
            self.diction = []
            tkinter.messagebox.showinfo("Done.", 'Passwords cleared.')
            self.mainframe.destroy()
            self.main_menu()
        else:
            self.mainframe.destroy()
            self.main_menu()


window = Tk()
window.configure(background="white")
window.title("Gashlane")
b = GUI(window)
window.mainloop()
