import tkinter as tk
from tkinter import messagebox
from scheduler import fcfs_scheduling, sjf_scheduling, priority_scheduling, round_robin
from visualize import draw_gantt_chart

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduler Simulator")
        
        self.process_list = []
        
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()
        
        tk.Label(self.input_frame, text="PID").grid(row=0, column=0)
        tk.Label(self.input_frame, text="Arrival Time").grid(row=0, column=1)
        tk.Label(self.input_frame, text="Burst Time").grid(row=0, column=2)
        tk.Label(self.input_frame, text="Priority").grid(row=0, column=3)
        
        self.pid_entry = tk.Entry(self.input_frame)
        self.arrival_entry = tk.Entry(self.input_frame)
        self.burst_entry = tk.Entry(self.input_frame)
        self.priority_entry = tk.Entry(self.input_frame)
        
        self.pid_entry.grid(row=1, column=0)
        self.arrival_entry.grid(row=1, column=1)
        self.burst_entry.grid(row=1, column=2)
        self.priority_entry.grid(row=1, column=3)
        
        tk.Button(self.input_frame, text="Add Process", command=self.add_process).grid(row=1, column=4)
        tk.Button(self.input_frame, text="Run FCFS", command=self.run_fcfs).grid(row=2, column=0)
        tk.Button(self.input_frame, text="Run SJF", command=self.run_sjf).grid(row=2, column=1)
        tk.Button(self.input_frame, text="Run Priority", command=self.run_priority).grid(row=2, column=2)
        tk.Button(self.input_frame, text="Run Round Robin", command=self.run_rr).grid(row=2, column=3)
        
    def add_process(self):
        try:
            pid = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get()) if self.priority_entry.get() else 0
            self.process_list.append((pid, arrival, burst, priority))
            messagebox.showinfo("Success", f"Process {pid} added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter numeric values.")
    
    def run_fcfs(self):
        processes = [Process(*p) for p in self.process_list]
        scheduled = fcfs_scheduling(processes)
        draw_gantt_chart(scheduled)

    def run_sjf(self):
        processes = [Process(*p) for p in self.process_list]
        scheduled = sjf_scheduling(processes)
        draw_gantt_chart(scheduled)

    def run_priority(self):
        processes = [Process(*p) for p in self.process_list]
        scheduled = priority_scheduling(processes)
        draw_gantt_chart(scheduled)

    def run_rr(self):
        try:
            quantum = int(tk.simpledialog.askstring("Quantum", "Enter Quantum Time:"))
            processes = [Process(*p) for p in self.process_list]
            scheduled = round_robin(processes, quantum)
            draw_gantt_chart(scheduled)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantum value.")

root = tk.Tk()
app = SchedulerApp(root)
root.mainloop()
