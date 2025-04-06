import streamlit as st
from scheduler import fcfs_scheduling, sjf_scheduling, priority_scheduling, round_robin
from visualize import draw_gantt_chart

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining_time = burst
        self.waiting_time = 0
        self.turnaround_time = 0


st.title("CPU Scheduler Simulator")

# Input Fields
processes = []
num_processes = st.number_input("Enter number of processes", min_value=1, step=1)

for i in range(num_processes):
    with st.expander(f"Process {i+1}"):
        pid = st.text_input(f"PID {i+1}", key=f"pid_{i}")
        arrival = st.number_input(f"Arrival Time {i+1}", min_value=0, step=1, key=f"arrival_{i}")
        burst = st.number_input(f"Burst Time {i+1}", min_value=1, step=1, key=f"burst_{i}")
        priority = st.number_input(f"Priority {i+1} (Optional)", min_value=0, step=1, key=f"priority_{i}")
        processes.append((pid, arrival, burst, priority))

# Scheduler Selection
algorithm = st.selectbox("Select Scheduling Algorithm", ["FCFS", "SJF", "Priority", "Round Robin"])

if algorithm == "Round Robin":
    quantum = st.number_input("Enter Quantum Time", min_value=1, step=1)

if st.button("Run Simulation"):
    processes_obj = [Process(*p) for p in processes]

    if algorithm == "FCFS":
        scheduled = fcfs_scheduling(processes_obj)
    elif algorithm == "SJF":
        scheduled = sjf_scheduling(processes_obj)
    elif algorithm == "Priority":
        scheduled = priority_scheduling(processes_obj)
    elif algorithm == "Round Robin":
        scheduled = round_robin(processes_obj, quantum)

    print("Scheduled Processes:", scheduled)

    if scheduled:
        draw_gantt_chart(scheduled)
    else:
        st.error("No processes were scheduled. Check your input data or scheduling function.")

