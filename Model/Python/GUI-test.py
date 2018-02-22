import tkinter as tk


root = tk.Tk()

root.title("empty GUI")
root.size()
greeting = tk.Label(text="start application")
greeting.pack(side='left')

back = tk.Frame(master=mw, width=500, height=500, bg='black')
back.pack(side='bottom')

root.mainloop()