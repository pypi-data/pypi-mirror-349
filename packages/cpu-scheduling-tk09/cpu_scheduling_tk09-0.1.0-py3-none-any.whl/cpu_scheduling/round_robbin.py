def round_robin(arrival_times, burst_times, quantum):
    n = len(arrival_times)
    rem_bt = burst_times[:]
    time = 0
    waiting_time = [0] * n
    turnaround_time = [0] * n
    queue = []
    visited = [False] * n
    completed = 0

    i = 0
    while i < n and arrival_times[i] <= time:
        queue.append(i)
        visited[i] = True
        i += 1

    while queue:
        idx = queue.pop(0)

        if rem_bt[idx] > quantum:
            time += quantum
            rem_bt[idx] -= quantum
        else:
            time += rem_bt[idx]
            rem_bt[idx] = 0
            turnaround_time[idx] = time - arrival_times[idx]
            waiting_time[idx] = turnaround_time[idx] - burst_times[idx]
            completed += 1

        for j in range(n):
            if arrival_times[j] <= time and not visited[j]:
                queue.append(j)
                visited[j] = True

        if rem_bt[idx] > 0:
            queue.append(idx)

        if not queue and completed < n:
            while i < n and arrival_times[i] > time:
                time += 1
            if i < n:
                queue.append(i)
                visited[i] = True
                i += 1

    return waiting_time, turnaround_time
