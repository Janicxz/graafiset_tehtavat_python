from tkinter import *

root = Tk()
root.tv_on = False
root.tv_volume = 100

def volumeUp():
    if root.tv_volume == 100:
        return

    root.tv_volume += 10
    print(f"Volume increase {root.tv_volume}")

def volumeDown():
    if root.tv_volume == 0:
        return

    root.tv_volume -= 10
    print(f"Volume decrease {root.tv_volume}")


def turnOnTV():
    try:
        if root.tv_on:
            return
    except:
        pass
    root.tv_on = True
    root.tv_window = Toplevel(root)
    root.tv_window.title("TV")
    photo_image = PhotoImage(file="tv.gif")
    original_image = Label(root.tv_window, image=photo_image)
    original_image.image = photo_image
    original_image.pack()

def turnOffTV():
    root.tv_on = False
    root.tv_window.destroy()

def initUI():
    turn_on = Button(root, text="ON", command=turnOnTV)
    turn_on.pack()

    turn_off = Button(root, text="OFF", command=turnOffTV)
    turn_off.pack()

    volume = Label(root, text="VOLUME")
    volume.pack()

    vol_up = Button(root, text="+", command=volumeUp)
    vol_up.pack()

    vol_down = Button(root, text="-", command=volumeDown)
    vol_down.pack()

if __name__ == "__main__":
    initUI()
    root.mainloop()