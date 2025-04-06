def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    result = []
    timeline = []

    for p in processes:
        start_time = max(current_time, p['arrival'])
        end_time = start_time + p['burst']
        completion = end_time
        turnaround = completion - p['arrival']
        waiting = turnaround - p['burst']

        result.append({
            'pid': p['pid'],
            'arrival': p['arrival'],
            'burst': p['burst'],
            'completion': completion,
            'turnaround': turnaround,
            'waiting': waiting
        })

        timeline.append({
            'pid': p['pid'],
            'start': start_time,
            'end': end_time
        })

        current_time = end_time

    return result, timeline

def round_robin(processes, time_quantum):
    processes = sorted(processes, key=lambda x: x['arrival'])
    queue = []
    time = 0
    timeline = []
    results = []
    remaining_burst = {p['pid']: p['burst'] for p in processes}
    process_map = {p['pid']: p for p in processes}
    arrived = []
    i = 0

    while i < len(processes) or queue:
        # Add newly arrived processes
        while i < len(processes) and processes[i]['arrival'] <= time:
            queue.append(processes[i]['pid'])
            arrived.append(processes[i]['pid'])
            i += 1

        if not queue:
            time += 1
            continue

        pid = queue.pop(0)
        burst_left = remaining_burst[pid]
        run_time = min(time_quantum, burst_left)
        start_time = time
        time += run_time
        end_time = time

        # Add to timeline
        timeline.append({
            'pid': pid,
            'start': start_time,
            'end': end_time
        })

        remaining_burst[pid] -= run_time

        # Add newly arrived processes during this run
        while i < len(processes) and processes[i]['arrival'] <= time:
            if processes[i]['pid'] not in arrived:
                queue.append(processes[i]['pid'])
                arrived.append(processes[i]['pid'])
            i += 1

        # Requeue if not finished
        if remaining_burst[pid] > 0:
            queue.append(pid)
        else:
            turnaround = end_time - process_map[pid]['arrival']
            waiting = turnaround - process_map[pid]['burst']
            results.append({
                'pid': pid,
                'arrival': process_map[pid]['arrival'],
                'burst': process_map[pid]['burst'],
                'completion': end_time,
                'waiting': waiting,
                'turnaround': turnaround
            })

    avg_waiting = sum(p['waiting'] for p in results) / len(results)
    avg_turnaround = sum(p['turnaround'] for p in results) / len(results)

    return {
        'processes': results,
        'avg_waiting': avg_waiting,
        'avg_turnaround': avg_turnaround
    }, timeline

def sjf(processes):
    processes = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    result = []
    timeline = []
    current_time = 0
    ready_queue = []
    completed = []

    while len(completed) < len(processes):
        for p in processes:
            if p not in completed and p['arrival'] <= current_time and p not in ready_queue:
                ready_queue.append(p)

        if ready_queue:
            ready_queue.sort(key=lambda x: x['burst'])
            current = ready_queue.pop(0)
            start_time = max(current_time, current['arrival'])
            end_time = start_time + current['burst']
            completion = end_time
            turnaround = completion - current['arrival']
            waiting = turnaround - current['burst']

            result.append({
                'pid': current['pid'],
                'arrival': current['arrival'],
                'burst': current['burst'],
                'completion': completion,
                'turnaround': turnaround,
                'waiting': waiting
            })

            timeline.append({
                'pid': current['pid'],
                'start': start_time,
                'end': end_time
            })

            current_time = end_time
            completed.append(current)
        else:
            current_time += 1

    return result, timeline

def priority_scheduling(processes):
    processes = sorted(processes, key=lambda x: (x['arrival'], x['priority']))
    result = []
    timeline = []
    current_time = 0
    ready_queue = []
    completed = []

    while len(completed) < len(processes):
        for p in processes:
            if p not in completed and p['arrival'] <= current_time and p not in ready_queue:
                ready_queue.append(p)

        if ready_queue:
            ready_queue.sort(key=lambda x: x['priority'])  # Lower value = higher priority
            current = ready_queue.pop(0)
            start_time = max(current_time, current['arrival'])
            end_time = start_time + current['burst']
            completion = end_time
            turnaround = completion - current['arrival']
            waiting = turnaround - current['burst']

            result.append({
                'pid': current['pid'],
                'arrival': current['arrival'],
                'burst': current['burst'],
                'priority': current['priority'],
                'completion': completion,
                'turnaround': turnaround,
                'waiting': waiting
            })

            timeline.append({
                'pid': current['pid'],
                'start': start_time,
                'end': end_time
            })

            current_time = end_time
            completed.append(current)
        else:
            current_time += 1

    return result, timeline


def preemptive_sjf(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    n = len(processes)
    time = 0
    completed = 0
    remaining_bt = {p['pid']: p['burst'] for p in processes}
    start_time = {}
    timeline = []
    ready_queue = []

    while completed < n:
        for p in processes:
            if p['arrival'] <= time and p['pid'] not in [x['pid'] for x in ready_queue if x['pid'] != 'idle'] and remaining_bt[p['pid']] > 0:
                ready_queue.append(p)

        if not ready_queue:
            timeline.append({'pid': 'idle', 'start': time, 'end': time + 1})
            time += 1
            continue

        current = min(ready_queue, key=lambda x: remaining_bt[x['pid']])
        if current['pid'] not in start_time:
            start_time[current['pid']] = time

        timeline.append({'pid': current['pid'], 'start': time, 'end': time + 1})
        remaining_bt[current['pid']] -= 1
        time += 1

        if remaining_bt[current['pid']] == 0:
            current['completion'] = time
            current['turnaround'] = current['completion'] - current['arrival']
            current['waiting'] = current['turnaround'] - current['burst']
            completed += 1
            ready_queue = [p for p in ready_queue if p['pid'] != current['pid']]

    return processes, timeline

def priority_preemptive(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    n = len(processes)
    time = 0
    completed = 0
    remaining_bt = {p['pid']: p['burst'] for p in processes}
    start_time = {}
    timeline = []
    ready_queue = []

    while completed < n:
        for p in processes:
            if p['arrival'] <= time and p['pid'] not in [x['pid'] for x in ready_queue if x['pid'] != 'idle'] and remaining_bt[p['pid']] > 0:
                ready_queue.append(p)

        if not ready_queue:
            timeline.append({'pid': 'idle', 'start': time, 'end': time + 1})
            time += 1
            continue

        current = min(ready_queue, key=lambda x: (x['priority'], x['arrival']))
        if current['pid'] not in start_time:
            start_time[current['pid']] = time

        timeline.append({'pid': current['pid'], 'start': time, 'end': time + 1})
        remaining_bt[current['pid']] -= 1
        time += 1

        if remaining_bt[current['pid']] == 0:
            current['completion'] = time
            current['turnaround'] = current['completion'] - current['arrival']
            current['waiting'] = current['turnaround'] - current['burst']
            completed += 1
            ready_queue = [p for p in ready_queue if p['pid'] != current['pid']]

    return processes, timeline
