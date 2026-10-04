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
            text = "Engine Paused",
            bg="#c62828",
            fg="white",
            font=("Segoe UI", 10 , "bold"),
            relief="flat",
            pady=8,
            command=self.toggle_engine
        )
        self.powerBtn.pack(fill="x", pady=(10, 5))

        #status label under button
        self.lblStatus = ttk.Label(headerFrame, text="Status: Waiting for Graph API...", font=("Segoe UI", 9 ,"italic"))
        self.lblStatus.pack()

        #Separator Line
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=15, pady=5)

        workflowFrame = ttk.Frame(self.root, padding=15)
        workflowFrame.pack(fill="x")

        ttk.Label(workflowFrame, text="Active Workflows", font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,8))

        self.fileSync = tk.BooleanVar(value=False)
        self.chkFile = ttk.Checkbutton(
            workflowFrame,
            text="OneDrive Organiser",
            variable=self.fileSync,
            command=lambda: self.log_toggle("OneDrive Organiser", self.fileSync.get())
        )
        self.chkFile.pack(anchor="w", pady=4)

        self.noteSync = tk.BooleanVar(value=False)
        self.chkNote = ttk.Checkbutton(
            workflowFrame,
            text = "OneNote Classifier",
            variable = self.noteSync,
            command=lambda: self.log_toggle("OneNote Classifier", self.noteSync.get())
        )
        self.chkNote.pack(anchor = "w", pady=4)
        
        self.meetingSync = tk.BooleanVar(value=False)
        self.chkMeeting = ttk.Checkbutton(
            workflowFrame,
            text="Outlook Meeting Alert",
            variable=self.meetingSync,
            command=lambda: self.log_toggle("Outlook Meeting Alert", self.meetingSync.get())
        )
        self.chkMeeting.pack(anchor="w", pady=4)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=15, pady=5)

        logFrame = ttk.Frame(self.root, padding = 15)
        logFrame.pack(fill="both", expand=True)

        ttk.Label(logFrame, text="Activity Log", font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,5))

        self.logBox = tk.Text(logFrame, height=6, font=("consolas",8), bg="#1e1e1e", fg="#d4d4d4", relief="flat")
        self.logBox.pack(fill="both", expand=True)

        self.addLog("Engine Initialised")

    def toggle_engine(self):
        self.engineActive = not self.engineActive
        if self.engineActive:
            self.powerBtn.config(text="Enginer Active", bg="#2e7d32")
            self.lblStatus.config(text="Status: Polling Graph API...")
            self.addLog("Engine Active")
        else:
            self.powerBtn.config(text="Engine Paused", bg="#c62828")
            self.lblStatus.config(text="Status: Waiting")
            self.addLog("Engine Paused")

    def log_toggle(self, name, state):
        status = "enabled" if state else "disabled"
        self.addLog(f"Worfklow '{name}' {status}")

    def addLog(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logBox.insert(tk.END, f"> [{timestamp}] {text}\n")
        self.logBox.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()