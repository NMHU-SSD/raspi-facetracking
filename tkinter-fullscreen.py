import tkinter as tk

root = tk.Tk()
root.geometry('1000x1000')
root.title("NMHU Face Recognition Project")

text1 = tk.Text(root, height=10, width=50)

text1.config(state = "normal")
text1.insert(tk.INSERT, "New Mexico Highlands Univeristy\n")
text1.config(state = "disabled")

text1.pack()

root.mainloop()
