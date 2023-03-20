import tkinter as tk


def answer_yes(event):
    print(event, "Yes")


def answer_no(event):
    print(event, "No")
    

root = tk.Tk()

# start_frame = tk.Frame(root)

lab = tk.Label(root, text="Wil je met zwart spelen?")
lab.pack(side=tk.TOP)

no_btn = tk.Button(root, text="No")
no_btn.pack(side=tk.RIGHT, padx=20, pady=5)


yes_btn = tk.Button(root, text="Yes")
yes_btn.pack(side=tk.RIGHT)

yes_btn.bind('<Button-1>', answer_yes)
no_btn.bind('<Button-1>', answer_no)

root.mainloop()
