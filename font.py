from tkinter import *
import tkinter.font

HEIGHT = 563
WIDTH = 900

def show_font(event):
    selected_font = mylist.get(mylist.curselection())
    example_label.config(text=f"Example: O X", font=(selected_font, 16))

root = Tk()
canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Tạo Frame để chứa Listbox và Scrollbar
frame = Frame(canvas)
frame.place(relx=0, rely=0, relwidth=0.42, relheight=1)

# Tạo Scrollbar
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

# Tạo Listbox và gán Scrollbar cho nó
mylist = Listbox(frame, yscrollcommand=scrollbar.set)
for line in sorted(tkinter.font.families()):
    mylist.insert(END, str(line))

mylist.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=mylist.yview)

# Tạo Label để hiển thị ví dụ phông chữ
example_label = Label(root, text="Example: ", font=("Helvetica", 16))
example_label.place(relx=0.45, rely=0.1)

# Gắn sự kiện chọn phông chữ trong Listbox để hiển thị ví dụ
mylist.bind('<<ListboxSelect>>', show_font)

root.mainloop()
