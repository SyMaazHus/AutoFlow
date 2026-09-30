import tkinter as tk
from tkinter import ttk
from datetime import datetime

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoFlow")
        self.root.geometry("380x480")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        #create header in root, fill it whole horizontally
        headerFrame = ttk.Frame(self.root, padding=15)
        headerFrame.pack(fill="x")

        #create text label within frame
        ttk.Label(headerFrame, text="AutoFlow Desktop", font=("Segoe UI", 14, "bold")).pack()

        #initial engine state paused
        self.engineActive = False
        #create button for the enging
        self.powerBtn = tk.Button(
            headerFrame,
            text = "ENGINE PAUSED",
            bg="#c62828",
            fg="white",
            font=("Seoge UI", 10 , "bold"),
            relief="flat",
            pady=8,
            #need to add command
        )
        self.powerBtn.pack(fill="x", pady=(10, 5))

        self.lblStatus = ttk.Label(headerFrame, text="Status: Waiting for Graph API...", font=("Segeo UI", 9 ,"italic"))
        self.lblStatus.pack()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()