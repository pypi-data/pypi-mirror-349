def sjf(arrival_times, burst_times):
    n = len(arrival_times)
    completed = 0
    time = 0
    waiting_time = [0] * n
    turnaround_time = [0] * n
    is_done = [False] * n

    while completed < n:
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            if arrival_times[i] <= time and not is_done[i]:
                if burst_times[i] < min_bt:
                    min_bt = burst_times[i]
                    idx = i

        if idx == -1:
            time += 1
            continue

        waiting_time[idx] = time - arrival_times[idx]
        turnaround_time[idx] = waiting_time[idx] + burst_times[idx]
        time += burst_times[idx]
        is_done[idx] = True
        completed += 1

    return waiting_time, turnaround_time
