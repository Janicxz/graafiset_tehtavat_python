from tkinter import Tk, ttk, StringVar

class UI:
    def __init__(self, root):
        self._root = root
        self._label_var = None

    def start(self):
        self._label_var = StringVar()
        self._label_var.set("0")

        label = ttk.Label(master=self._root,
                          textvariable=self._label_var)
        increase_button = ttk.Button(master=self._root,
                                     text="Increase",
                                     command=self._increase)
        decrease_button = ttk.Button(master=self._root,
                                     text="Decrease",
                                     command=self._decrease)

        increase_button.grid()
        label.grid(row=0, column=1)
        decrease_button.grid(row=0, column=2)

    def _increase(self):
        value = self._label_var.get()
        value = str(int(value) + 1)
        self._label_var.set(value)

    def _decrease(self):
        value = self._label_var.get()
        value = str(int(value) - 1)
        self._label_var.set(value)
def main():
    window = Tk()
    window.title("TkInter example")

    ui = UI(window)
    ui.start()

    window.mainloop()

main()