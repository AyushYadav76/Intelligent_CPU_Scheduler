class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival)  # Sort by arrival time
    current_time = 0
    
    for process in processes:
        if current_time < process.arrival:
            current_time = process.arrival  # Handle CPU idle time
        process.start_time = current_time
        process.completion_time = current_time + process.burst
        process.turnaround_time = process.completion_time - process.arrival
        process.waiting_time = process.turnaround_time - process.burst
        current_time = process.completion_time  # Move time forward
    
    return processes  # Return list with updated times

def sjf_scheduling(processes, preemptive=False):
    processes.sort(key=lambda x: (x.arrival, x.burst))
    completed = []
    ready_queue = []
    current_time = 0
    while processes or ready_queue:
        while processes and processes[0].arrival <= current_time:
            ready_queue.append(processes.pop(0))
        if not ready_queue:
            current_time = processes[0].arrival
            continue
        if preemptive:
            ready_queue.sort(key=lambda x: x.burst)
        process = ready_queue.pop(0)
        process.start_time = current_time
        process.completion_time = current_time + process.burst
        process.turnaround_time = process.completion_time - process.arrival
        process.waiting_time = process.turnaround_time - process.burst
        current_time = process.completion_time
        completed.append(process)
    return completed

def priority_scheduling(processes, preemptive=False):
    processes.sort(key=lambda x: (x.arrival, x.priority))
    completed = []
    ready_queue = []
    current_time = 0
    while processes or ready_queue:
        while processes and processes[0].arrival <= current_time:
            ready_queue.append(processes.pop(0))
        if not ready_queue:
            current_time = processes[0].arrival
            continue
        if preemptive:
            ready_queue.sort(key=lambda x: x.priority)
        process = ready_queue.pop(0)
        process.start_time = current_time
        process.completion_time = current_time + process.burst
        process.turnaround_time = process.completion_time - process.arrival
        process.waiting_time = process.turnaround_time - process.burst
        current_time = process.completion_time
        completed.append(process)
    return completed

def round_robin(processes, quantum):
    queue = []
    current_time = 0
    completed = []
    remaining_burst = {p.pid: p.burst for p in processes}
    while processes or queue:
        while processes and processes[0].arrival <= current_time:
            queue.append(processes.pop(0))
        if not queue:
            current_time = processes[0].arrival
            continue
        process = queue.pop(0)
        if process.start_time is None:
            process.start_time = current_time
        if remaining_burst[process.pid] > quantum:
            remaining_burst[process.pid] -= quantum
            current_time += quantum
            queue.append(process)
        else:
            current_time += remaining_burst[process.pid]
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival
            process.waiting_time = process.turnaround_time - process.burst
            completed.append(process)
    return completed
