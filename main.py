import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import fcfs, round_robin, sjf, priority_scheduling, preemptive_sjf, priority_preemptive
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


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

# GUI setup
root = tk.Tk()
root.title("CPU Scheduler Simulator")

process_list = []
algorithm_var = tk.StringVar(value="FCFS")

# --- Top Dropdown ---
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Select Scheduling Algorithm:").pack(side=tk.LEFT)

algorithm_dropdown = ttk.Combobox(frame_top, textvariable=algorithm_var,
                                  values=["FCFS", "SJF", "SJF (Preemptive)", "Round Robin", 
                                          "Priority Scheduling", "Priority Scheduling (Preemptive)"],
                                  state="readonly")
algorithm_dropdown.pack(side=tk.LEFT, padx=10)

# --- Input Fields ---
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Process ID").grid(row=0, column=0)
tk.Label(frame_input, text="Arrival Time").grid(row=0, column=1)
tk.Label(frame_input, text="Burst Time").grid(row=0, column=2)

entry_pid = tk.Entry(frame_input, width=10)
entry_arrival = tk.Entry(frame_input, width=10)
entry_burst = tk.Entry(frame_input, width=10)

entry_pid.grid(row=1, column=0)
entry_arrival.grid(row=1, column=1)
entry_burst.grid(row=1, column=2)

# --- Priority Field ---
label_priority = tk.Label(frame_input, text="Priority")
entry_priority = tk.Entry(frame_input, width=10)
label_priority.grid(row=0, column=3)
entry_priority.grid(row=1, column=3)
label_priority.grid_remove()
entry_priority.grid_remove()

# --- Time Quantum Field ---
frame_quantum = tk.Frame(root)
label_quantum = tk.Label(frame_quantum, text="Time Quantum (for RR):")
quantum_entry = tk.Entry(frame_quantum)

label_quantum.pack(side=tk.LEFT)
quantum_entry.pack(side=tk.LEFT)
frame_quantum.pack()
frame_quantum.pack_forget()  # Initially hidden

# --- Add Button ---
btn_add = tk.Button(frame_input, text="Add Process", command=add_process)
btn_add.grid(row=1, column=4, padx=10)

# --- Process List Display ---
tk.Label(root, text="Process List:").pack()
process_text = tk.Text(root, height=8, width=60)
process_text.pack(pady=5)

# --- Simulation Output Display ---
tk.Label(root, text="Simulation Output:").pack()
output_text = tk.Text(root, height=10, width=60)
output_text.pack(pady=5)

# --- Placeholder for the Gantt chart canvas ---
gantt_canvas = None

button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="Delete Process", command=delete_process).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Reset All", command=reset_all).grid(row=0, column=2, padx=5)

# --- Frame to hold Run button and Checkbox side by side ---
run_frame = tk.Frame(root)
run_frame.pack(pady=5)

# --- Run Button ---
btn_run = tk.Button(run_frame, text="Run Simulation", command=run_simulation)
btn_run.pack(side="left", padx=(0, 10))  # Padding on right to separate from checkbox

# --- Animation Toggle Checkbox ---
is_animated = tk.BooleanVar()
animation_checkbox = tk.Checkbutton(run_frame, text="Animate Gantt Chart", variable=is_animated)
animation_checkbox.pack(side="left")

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
