import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from scheduler import fcfs, round_robin, sjf, priority_scheduling, preemptive_sjf, priority_preemptive
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Arial", 9), padx=4, pady=2)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def add_hover_effect(widget):
    widget.bind("<Enter>", lambda e: widget.configure(style="Hover.TButton"))
    widget.bind("<Leave>", lambda e: widget.configure(style="TButton"))

process_list = []

def add_process():
    pid = entry_pid.get()
    arrival = entry_arrival.get()
    burst = entry_burst.get()
    priority = entry_priority.get() if algorithm_var.get() == "Priority Scheduling" or algorithm_var.get() == "Priority Scheduling (Preemptive)" else "0"

    if not pid or not arrival or not burst:
        messagebox.showerror("Input Error", "Please enter PID, Arrival Time, and Burst Time.")
        return

    try:
        process = {
            'pid': pid,
            'arrival': int(arrival),
            'burst': int(burst),
            'priority': int(priority)
        }
    except ValueError:
        messagebox.showerror("Input Error", "Arrival, Burst, and Priority must be integers.")
        return

    process_list.append(process)

    # Display process table header once
    if len(process_list) == 1:
        process_text.insert(tk.END, f"{'PID':<8}{'Arrival':<10}{'Burst':<10}{'Priority':<10}\n")
        process_text.insert(tk.END, "-" * 40 + "\n")

    # Display the newly added process in tabular format
    row = f"{process['pid']:<8}{process['arrival']:<10}{process['burst']:<10}{process['priority']:<10}\n"
    process_text.insert(tk.END, row)

    # Optional: Status message in output_text
    # output_text.insert(tk.END, f"Added process: {process['pid']}\n")

    # Clear input fields
    entry_pid.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)
    entry_priority.delete(0, tk.END)

def reset_all():
    process_list.clear()
    process_text.delete('1.0', tk.END)
    output_text.delete('1.0', tk.END)

def delete_process():
    pid_to_delete = entry_pid.get()
    if not pid_to_delete:
        messagebox.showerror("Input Error", "Enter the PID to delete.")
        return

    # Remove process with matching PID
    initial_len = len(process_list)
    process_list[:] = [p for p in process_list if p['pid'] != pid_to_delete]

    if len(process_list) == initial_len:
        messagebox.showinfo("Delete Process", f"No process found with PID {pid_to_delete}.")
    else:
        messagebox.showinfo("Delete Process", f"Deleted process with PID {pid_to_delete}.")

    # Refresh the process list display
    process_text.delete('1.0', tk.END)
    if process_list:
        process_text.insert(tk.END, f"{'PID':<8}{'Arrival':<10}{'Burst':<10}{'Priority':<10}\n")
        process_text.insert(tk.END, "-" * 40 + "\n")
        for process in process_list:
            row = f"{process['pid']:<8}{process['arrival']:<10}{process['burst']:<10}{process['priority']:<10}\n"
            process_text.insert(tk.END, row)

def run_simulation():
    algorithm = algorithm_var.get()

    if algorithm == "FCFS":
        result, timeline = fcfs(process_list)
        output_text.delete('1.0', tk.END)
        
        total_wt = 0
        total_tat = 0
        for r in result:
            output_text.insert(tk.END, f"{r['pid']} -> CT: {r['completion']} | TAT: {r['turnaround']} | WT: {r['waiting']}\n")
            total_wt += r['waiting']
            total_tat += r['turnaround']
        
        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        output_text.insert(tk.END, f"\nAverage Waiting Time: {avg_wt:.2f}")
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}")
        if is_animated.get():
            draw_animated_gantt_chart(timeline)
        else:
            draw_gantt_chart(timeline)
    
    elif algorithm == "Round Robin":
        try:
            quantum = int(quantum_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for time quantum.")
            return

        result, timeline = round_robin(process_list, quantum)
        output_text.delete('1.0', tk.END)

        total_wt = 0
        total_tat = 0
        for r in result['processes']:
            output_text.insert(tk.END, f"{r['pid']} -> CT: {r['completion']} | TAT: {r['turnaround']} | WT: {r['waiting']}\n")
            total_wt += r['waiting']
            total_tat += r['turnaround']

        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        output_text.insert(tk.END, f"\nAverage Waiting Time: {avg_wt:.2f}")
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}")
        # print("Timeline Data:", timeline) # debugging line
        
        if is_animated.get():
            draw_animated_gantt_chart(timeline)
        else:
            draw_gantt_chart(timeline)
    
    elif algorithm == "SJF":
        result, timeline = sjf(process_list)
        output_text.delete('1.0', tk.END)

        total_wt = 0
        total_tat = 0
        for r in result:
            output_text.insert(tk.END, f"{r['pid']} -> CT: {r['completion']} | TAT: {r['turnaround']} | WT: {r['waiting']}\n")
            total_wt += r['waiting']
            total_tat += r['turnaround']

        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        output_text.insert(tk.END, f"\nAverage Waiting Time: {avg_wt:.2f}")
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}")

        if is_animated.get():
            draw_animated_gantt_chart(timeline)
        else:
            draw_gantt_chart(timeline)
    
    elif algorithm == "Priority Scheduling":
        result, timeline = priority_scheduling(process_list)
        output_text.delete('1.0', tk.END)

        total_wt = 0
        total_tat = 0
        for r in result:
            output_text.insert(tk.END, f"{r['pid']} -> CT: {r['completion']} | TAT: {r['turnaround']} | WT: {r['waiting']} | Priority: {r['priority']}\n")
            total_wt += r['waiting']
            total_tat += r['turnaround']

        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        output_text.insert(tk.END, f"\nAverage Waiting Time: {avg_wt:.2f}")
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}")

        if is_animated.get():
            draw_animated_gantt_chart(timeline)
        else:
            draw_gantt_chart(timeline)

    elif algorithm == "SJF (Preemptive)":
        result, timeline = preemptive_sjf(process_list)
        output_text.delete('1.0', tk.END)

        total_wt = 0
        total_tat = 0
        for r in result:
            output_text.insert(tk.END, f"{r['pid']} -> CT: {r['completion']} | TAT: {r['turnaround']} | WT: {r['waiting']}\n")
            total_wt += r['waiting']
            total_tat += r['turnaround']

        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        output_text.insert(tk.END, f"\nAverage Waiting Time: {avg_wt:.2f}")
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}")
        # print("Timeline Data:", timeline) #debugging line
        
        if is_animated.get():
            draw_animated_gantt_chart(timeline)
        else:
            draw_gantt_chart(timeline)

    elif algorithm == "Priority Scheduling (Preemptive)":
        result, timeline = priority_preemptive(process_list)
        output_text.delete('1.0', tk.END)

        total_wt = 0
        total_tat = 0
        for r in result:
            output_text.insert(tk.END, f"{r['pid']} -> CT: {r['completion']} | TAT: {r['turnaround']} | WT: {r['waiting']} | Priority: {r['priority']}\n")
            total_wt += r['waiting']
            total_tat += r['turnaround']

        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        output_text.insert(tk.END, f"\nAverage Waiting Time: {avg_wt:.2f}")
        output_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_tat:.2f}")

        if is_animated.get():
            draw_animated_gantt_chart(timeline)
        else:
            draw_gantt_chart(timeline)

    else:
        messagebox.showinfo("Coming Soon", f"{algorithm} not implemented yet.")


def draw_gantt_chart(schedule):
    fig, gnt = plt.subplots()
    gnt.set_title("Gantt Chart")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")

    gnt.set_yticks([10 * (i + 1) for i in range(len(schedule))])
    gnt.set_yticklabels([p['pid'] for p in schedule])
    gnt.set_ylim(0, 10 * (len(schedule) + 1))

    for i, p in enumerate(schedule):
        start = p['completion'] - p['burst']
        gnt.broken_barh([(start, p['burst'])], (10 * (i + 1) - 4, 8),
                        facecolors=('tab:blue'))

    plt.show()

def draw_gantt_chart(timeline):
    if not timeline:
        return

    fig, ax = plt.subplots(figsize=(10, 2))

    colors = {}
    y_pos = 10  # y-axis fixed position for the bar height
    height = 9
    used_colors = []

    for item in timeline:
        pid = item['pid']
        start = item['start']
        end = item['end']

        # Assign a unique color for each process
        if pid not in colors:
            while True:
                color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                if color not in used_colors:
                    break
            colors[pid] = color
            used_colors.append(color)

        ax.broken_barh([(int(start), int(end) - int(start))], (y_pos, height), facecolors=colors[pid])
        ax.text((int(start) + int(end)) / 2, y_pos + height / 2, f"P{pid}",
                ha='center', va='center', color='black', fontsize=8, weight='bold')

    ax.set_ylim(0, 30)
    ax.set_xlim(0, max(int(item['end']) for item in timeline) + 2)
    ax.set_xlabel("Time")
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_title("Gantt Chart")

    fig.tight_layout()
    plt.show()

def draw_animated_gantt_chart(timeline):
    if not timeline:
        return

    fig, ax = plt.subplots(figsize=(10, 2))
    y_pos = 10
    height = 9
    colors = {}
    used_colors = []

    # Assign colors beforehand
    for item in timeline:
        pid = item['pid']
        if pid not in colors:
            while True:
                color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                if color not in used_colors:
                    break
            colors[pid] = color
            used_colors.append(color)

    bars = []

    def init():
        ax.set_xlim(0, max(item['end'] for item in timeline) + 2)
        ax.set_ylim(0, 30)
        ax.set_yticks([])
        ax.set_xlabel("Time")
        ax.set_title("Live Gantt Chart Simulation")
        return bars

    def animate(i):
        if i >= len(timeline):
            return bars

        item = timeline[i]
        pid = item['pid']
        start = item['start']
        end = item['end']

        bar = ax.broken_barh([(start, end - start)], (y_pos, height), facecolors=colors[pid])
        text = ax.text((start + end) / 2, y_pos + height / 2, f"P{pid}",
                       ha='center', va='center', color='black', fontsize=8, weight='bold')

        bars.append(bar)
        bars.append(text)
        return bars

    ani = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=len(timeline), interval=800, blit=False, repeat=False)
    plt.show()


# --- Root window styling ---
root = ThemedTk(theme="arc")
root.title("CPU Scheduler Simulator")
root.configure(bg="#f5f7fa")  # Light background

default_font = ("Segoe UI", 10)
root.option_add("*Font", default_font)

# --- ttk Style Enhancements ---
style = ttk.Style()
style.theme_use('default')

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x", pady=5)

style.configure(".", background="#f5f7fa")
style.configure("TLabel", background="#f5f7fa")
style.configure("TCheckbutton", background="#f5f7fa")

# Base TButton style
style.configure("TButton",
    padding=8,
    relief="flat",
    background="#4a90e2",
    foreground="white",
    font=('Segoe UI', 10, 'bold'),
    borderwidth=0
)
style.map("TButton",
    background=[('active', '#357ab7'), ('pressed', '#2c5aa0')],
    foreground=[('active', 'white')]
)

# Other widgets
style.configure("TEntry",
    relief="flat",
    padding=6,
    font=('Segoe UI', 10)
)

style.configure("TCombobox",
    padding=6,
    font=('Segoe UI', 10)
)

# --- Styling for all labels ---
label_style = {"bg": "#f0f0f0", "fg": "#000000"}

algorithm_var = tk.StringVar(value="FCFS")

# --- Top Dropdown ---
frame_top = ttk.LabelFrame(root, text="Select Algorithm", padding=10)
frame_top.pack(pady=10, padx=10, fill="x")

tk.Label(frame_top, text="Select Scheduling Algorithm:", **label_style).pack(side=tk.LEFT)

algorithm_dropdown = ttk.Combobox(frame_top, textvariable=algorithm_var,
                                  values=["FCFS", "SJF", "SJF (Preemptive)", "Round Robin", 
                                          "Priority Scheduling", "Priority Scheduling (Preemptive)"],
                                  state="readonly")
algorithm_dropdown.pack(side=tk.LEFT, padx=10)
Tooltip(algorithm_dropdown, "Choose a scheduling algorithm")

# --- Input Fields Frame with border ---
frame_input = ttk.LabelFrame(root, text="Add New Process", padding=10)
frame_input.pack(pady=10, padx=10, fill="x")

tk.Label(frame_input, text="Process ID", **label_style).grid(row=0, column=0)
tk.Label(frame_input, text="Arrival Time", **label_style).grid(row=0, column=1)
tk.Label(frame_input, text="Burst Time", **label_style).grid(row=0, column=2)

entry_pid = ttk.Entry(frame_input, width=10)
entry_arrival = ttk.Entry(frame_input, width=10)
entry_burst = ttk.Entry(frame_input, width=10)

entry_pid.grid(row=1, column=0)
entry_arrival.grid(row=1, column=1)
entry_burst.grid(row=1, column=2)

Tooltip(entry_pid, "Enter the process ID (e.g., 1, A)")
Tooltip(entry_arrival, "Time when the process arrives")
Tooltip(entry_burst, "CPU burst time for the process")

# --- Priority Field ---
label_priority = tk.Label(frame_input, text="Priority", **label_style)
entry_priority = ttk.Entry(frame_input, width=10)
label_priority.grid(row=0, column=3)
entry_priority.grid(row=1, column=3)
label_priority.grid_remove()
entry_priority.grid_remove()
Tooltip(entry_priority, "Only used in Priority Scheduling")

# --- Time Quantum Field ---
frame_quantum = tk.Frame(root, bg="#f0f0f0")
label_quantum = tk.Label(frame_quantum, text="Time Quantum (for RR):", **label_style)
quantum_entry = ttk.Entry(frame_quantum)

label_quantum.pack(side=tk.LEFT)
quantum_entry.pack(side=tk.LEFT)
frame_quantum.pack()
frame_quantum.pack_forget()  # Initially hidden

Tooltip(quantum_entry, "Only used in Round Robin algorithm")

# --- Add Button ---
btn_add = ttk.Button(frame_input, text="Add Process", command=add_process)
btn_add.grid(row=1, column=4, padx=10)
add_hover_effect(btn_add)
Tooltip(btn_add, "Add the process to the list")

# --- Process List Display ---
process_list_frame = ttk.LabelFrame(root, text="Process List", padding=10)
process_list_frame.pack(pady=10, padx=10, fill="x")

process_text = tk.Text(process_list_frame, height=8, width=60)
process_text.pack(pady=5)

# --- Simulation Output Display ---
output_frame = ttk.LabelFrame(root, text="Simulation Output", padding=10)
output_frame.pack(pady=10, padx=10, fill="x")
output_text = tk.Text(output_frame, height=10, width=60)
output_text.pack(pady=5)

# --- Placeholder for the Gantt chart canvas ---
gantt_canvas = None

# --- Button Frame (Delete/Reset) ---
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=5)

btn_delete = ttk.Button(button_frame, text="Delete Process", command=delete_process)
btn_delete.grid(row=0, column=1, padx=5)
add_hover_effect(btn_delete)

btn_reset = ttk.Button(button_frame, text="Reset All", command=reset_all)
btn_reset.grid(row=0, column=2, padx=5)
add_hover_effect(btn_reset)

Tooltip(btn_delete, "Remove the selected process from the list")
Tooltip(btn_reset, "Clear all processes and outputs")

# --- Run + Animation Toggle Frame ---
run_frame = tk.Frame(root, bg="#f0f0f0")
run_frame.pack(pady=5)

btn_run = ttk.Button(run_frame, text="Run Simulation", command=run_simulation)
btn_run.pack(side="left", padx=(0, 10))
add_hover_effect(btn_run)
Tooltip(btn_run, "Run the CPU scheduling simulation")

is_animated = tk.BooleanVar()
animation_checkbox = tk.Checkbutton(run_frame, text="Animate Gantt Chart", variable=is_animated, bg="#f0f0f0")
animation_checkbox.pack(side="left")
Tooltip(animation_checkbox, "Toggle animated Gantt chart")


# --- Algorithm Change Callback ---
def on_algorithm_change(event=None):
    selected = algorithm_var.get()
    if selected == "Priority Scheduling" or selected == "Priority Scheduling (Preemptive)":
        label_priority.grid()
        entry_priority.grid()
        frame_quantum.pack_forget()
    elif selected == "Round Robin":
        frame_quantum.pack(pady=5)
        label_priority.grid_remove()
        entry_priority.grid_remove()
    else:
        label_priority.grid_remove()
        entry_priority.grid_remove()
        frame_quantum.pack_forget()

algorithm_dropdown.bind("<<ComboboxSelected>>", on_algorithm_change)
on_algorithm_change()  # Call initially to set correct visibility

root.mainloop()
