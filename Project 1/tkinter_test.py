import Tkinter
import random

root = Tkinter.Tk(  )
root.title("Simple Prog")
for r in range(5):
    for c in range(5):
        i = random.randint(0,5)
        Tkinter.Label(root, text='%s'%(i),
            borderwidth=10 ).grid(row=r,column=c)
root.mainloop(  )

root = Tkinter.Tk(  )
root.title("Simple Prog")
for r in range(7):
    for c in range(7):
        i = random.randint(0,5)
        Tkinter.Label(root, text='%s'%(i),
            borderwidth=10 ).grid(row=r,column=c)
root.mainloop(  )
