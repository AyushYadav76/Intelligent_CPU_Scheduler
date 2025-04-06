import matplotlib.pyplot as plt

def draw_gantt_chart(processes):
    fig, ax = plt.subplots()
    y_labels = []
    for process in processes:
        ax.barh(process.pid, process.completion_time - process.start_time, left=process.start_time)
        y_labels.append(process.pid)
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)
    plt.show()
