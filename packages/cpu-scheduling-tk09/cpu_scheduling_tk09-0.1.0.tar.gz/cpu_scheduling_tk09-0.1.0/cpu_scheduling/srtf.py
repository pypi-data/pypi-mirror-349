def srtf(arrival_times, burst_times):
    n = len(arrival_times)
    remaining_time = burst_times[:]
    complete = 0
    time = 0
    min_index = -1
    waiting_time = [0] * n
    turnaround_time = [0] * n
    finish_time = [0] * n
    is_done = [False] * n

    while complete != n:
        min_time = float('inf')
        for i in range(n):
            if arrival_times[i] <= time and remaining_time[i] > 0 and remaining_time[i] < min_time:
                min_time = remaining_time[i]
                min_index = i

        if min_index == -1:
            time += 1
            continue

        remaining_time[min_index] -= 1
        if remaining_time[min_index] == 0:
            complete += 1
            finish_time[min_index] = time + 1
            turnaround_time[min_index] = finish_time[min_index] - arrival_times[min_index]
            waiting_time[min_index] = turnaround_time[min_index] - burst_times[min_index]

        time += 1

    return waiting_time, turnaround_time
