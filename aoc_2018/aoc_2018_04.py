with open('data/aoc_2018/04.txt') as f:
    dat = sorted([x.strip() for x in f.readlines()])

def parse_data(output = True):
    duty_guard = 0
    guard_minutes = {}
    guard_periods = {}
    for d in dat:
        ts, act = d.split('] ')
        if act[0] == 'G':
            duty_guard = int(act.split('#')[1].split(' ')[0])
            if duty_guard not in guard_minutes:
                guard_minutes[duty_guard] = 0
            if duty_guard not in guard_periods:
                guard_periods[duty_guard] = {}
        if act[0] == 'f':
            asleep = int(ts.split(':')[1])
        if act[0] == 'w':
            awake = int(ts.split(':')[1])
            date = ts.split(' ')[0].strip('[')
            guard_minutes[duty_guard] += awake - asleep
            if date in guard_periods[duty_guard]:
                guard_periods[duty_guard][date] += [(asleep, awake)]
            else:
                guard_periods[duty_guard][date] = [(asleep, awake)]
            if output:
                print('Guard', duty_guard, 'asleep between', asleep, 'and', awake, 'on', date)
    return guard_minutes, guard_periods

def part1(output = True):
    guard_minutes, guard_periods = parse_data(output)

    most_asleep = max(guard_minutes.items(), key = lambda x: x[1])
    if output:
        print('Most asleep guard is', most_asleep[0], 'for', most_asleep[1], 'minutes')
    minutes = {m: 0 for m in range(60)}
    for date, spans in guard_periods[most_asleep[0]].items():
        for span in spans:
            for m in range(span[0], span[1]):
                minutes[m] += 1
    most_asleep_minute = max(minutes.items(), key = lambda x: x[1])
    if output:
        print('Most often asleep minute is', most_asleep_minute[0], 'with', most_asleep_minute[1], 'dates')
    return most_asleep[0] * most_asleep_minute[0]

def part2(output = True):
    guard_minutes, guard_periods = parse_data(False)

    guard_max_minutes = {}
    for guard in guard_periods.keys():
        minutes = {m: 0 for m in range(60)}
        for date, spans in guard_periods[guard].items():
            for span in spans:
                for m in range(span[0], span[1]):
                    minutes[m] += 1
        most_asleep_minute = max(minutes.items(), key = lambda x: x[1])
        if output:
            print('Guard', guard, 'most often asleep minute is', most_asleep_minute[0], 'with', most_asleep_minute[1], 'dates')
        guard_max_minutes[guard] = most_asleep_minute

    most_asleep = max(guard_max_minutes.items(), key = lambda x: x[1][1])

    return most_asleep[0] * most_asleep[1][0]
