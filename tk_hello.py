from tkinter import Tk, ttk, constants

class GoodByeView:
    def __init__(self, root, handle_hello):
        self._root = root
        self._handle_hello = handle_hello
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        label = ttk.Label(master=self._frame, text="Good bye!")

        button = ttk.Button(
            master=self._frame,
            text="Say hello",
            command=self._handle_hello
        )

        label.grid(row=0, column=0)
        button.grid(row=1, column=0)

class HelloView:
    def __init__(self, root, handle_good_bye):
        self._root = root
        self._handle_good_bye = handle_good_bye
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        label = ttk.Label(master=self._frame, text="Hello!")

        button = ttk.Button(
            master=self._frame,
            text="Say good bye",
            command=self._handle_good_bye
        )
        label.grid(row=0, column=0)
        button.grid(row=1, column=0)

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_hello_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _handle_good_bye(self):
        self._show_good_bye_view()

    def _handle_hello(self):
        self._show_hello_view()
        
    def _show_good_bye_view(self):
        self._hide_current_view()

        self._current_view = GoodByeView(
            self._root,
            self._handle_hello
        )
        self._current_view.pack()

    def _show_hello_view(self):
        self._hide_current_view()
        
        self._current_view = HelloView(
            self._root, 
            self._handle_good_bye)
        self._current_view.pack()


def main():
    window = Tk()
    window.title("TkInter example")

    ui = UI(window)
    ui.start()

    window.mainloop()

main()