def priority_scheduling(arrival_times, burst_times, priorities, preemptive=False):
    n = len(arrival_times)
    waiting_time = [0] * n
    turnaround_time = [0] * n

    if not preemptive:
        completed = 0
        time = 0
        is_done = [False] * n

        while completed < n:
            idx = -1
            highest_priority = float('inf')
            for i in range(n):
                if arrival_times[i] <= time and not is_done[i]:
                    if priorities[i] < highest_priority:
                        highest_priority = priorities[i]
                        idx = i

            if idx == -1:
                time += 1
                continue

            waiting_time[idx] = time - arrival_times[idx]
            time += burst_times[idx]
            turnaround_time[idx] = waiting_time[idx] + burst_times[idx]
            is_done[idx] = True
            completed += 1

    else:
        remaining_time = burst_times[:]
        complete = 0
        time = 0
        finish_time = [0] * n
        is_done = [False] * n

        while complete != n:
            idx = -1
            highest_priority = float('inf')
            for i in range(n):
                if arrival_times[i] <= time and remaining_time[i] > 0:
                    if priorities[i] < highest_priority:
                        highest_priority = priorities[i]
                        idx = i

            if idx == -1:
                time += 1
                continue

            remaining_time[idx] -= 1
            if remaining_time[idx] == 0:
                complete += 1
                finish_time[idx] = time + 1
                turnaround_time[idx] = finish_time[idx] - arrival_times[idx]
                waiting_time[idx] = turnaround_time[idx] - burst_times[idx]

            time += 1

    return waiting_time, turnaround_time
