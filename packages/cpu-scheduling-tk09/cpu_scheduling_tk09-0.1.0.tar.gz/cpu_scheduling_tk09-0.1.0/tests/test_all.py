from cpu_scheduling import fcfs,sjf,srtf,round_robin,priority_scheduling

def test_fcfs():
    wt, tat = fcfs([0, 2, 4], [5, 3, 1])
    print("FCFS\nWaiting:", wt, "\nTurnaround:", tat)

def test_sjf():
    wt, tat = sjf([0, 1, 2, 3], [4,3,1,2])
    print("SJF\nWaiting:", wt, "\nTurnaround:", tat)

def test_srtf():
    wt, tat = srtf([0, 1, 2,3], [8, 4, 2,1])
    print("SRTF\nWaiting:", wt, "\nTurnaround:", tat)

def test_rr():
    wt, tat = round_robin([0, 1, 2,3], [4, 3, 2,1], quantum=2)
    print("Round Robin\nWaiting:", wt, "\nTurnaround:", tat)

def test_priority():
    wt, tat = priority_scheduling([0, 1, 2,3], [8, 4, 9,5], [2, 1, 3,2])
    print("Priority\nWaiting:", wt, "\nTurnaround:", tat)

if __name__ == "__main__":
    test_fcfs()
    test_sjf()
    test_srtf()
    test_rr()
    test_priority()
