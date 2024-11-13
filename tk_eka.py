from tkinter import Tk, ttk, constants

class UI:
    def __init__(self, root):
        self._root = root
        self._user_entry = None
        self._pass_entry = None

    def _handle_button_click(self):
        user = self._user_entry.get()
        password = self._pass_entry.get()
        if user == "" or password == "":
            missing = "username and password"
            if user == "" and password != "":
                missing = "username"
            elif password == "" and user != "":
                missing = "password"
            print(f"Missing {missing}!")
        else:
            print(f"{user}:{password}")

    def start(self):
        heading_label = ttk.Label(master=self._root, text="Login")

        username_label = ttk.Label(master=self._root, text="Username")
        self._user_entry = ttk.Entry(master=self._root)

        password_label = ttk.Label(master=self._root, text="Password")
        self._pass_entry = ttk.Entry(master=self._root)

        button = ttk.Button(master=self._root, text="Button", command=self._handle_button_click)

        heading_label.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky=constants.W)

        username_label.grid(padx=5, pady=5)
        self._user_entry.grid(row=1, column=1,  sticky=(constants.E, constants.W), padx=5, pady=5)

        password_label.grid(padx=5, pady=5)
        self._pass_entry.grid(row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)

        button.grid(columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)

        self._root.grid_columnconfigure(1,weight=1, minsize=300)



def main():
    window = Tk()
    window.title("TkInter example")

    ui = UI(window)
    ui.start()

    window.mainloop()

main()