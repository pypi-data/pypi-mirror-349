def fcfs(arrival_times, burst_times):
    n = len(arrival_times)
    start_time = 0
    waiting_time = [0] * n
    turnaround_time = [0] * n

    process = sorted(zip(arrival_times, burst_times, range(n)))

    for arrival, burst, idx in process:
        if start_time < arrival:
            start_time = arrival
        waiting_time[idx] = start_time - arrival
        turnaround_time[idx] = waiting_time[idx] + burst
        start_time += burst

    return waiting_time, turnaround_time
