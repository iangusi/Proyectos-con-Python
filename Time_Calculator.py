def add_time(start, duration,day='False'):

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    time = start.split(' ')
    time_start = time[0].split(':')
    time_duration = duration.split(':')

    hour_start = int(time_start[0])
    minute_start = int(time_start[1])

    hour_duration = int(time_duration[0])
    minute_duration = int(time_duration[1])
  
    hour_result = hour_start+hour_duration
    minute_result = minute_start+minute_duration

    if minute_result > 60:
        hour_result += 1
        hour_duration += 1
        minute_result -= 60

    count_days = 0

    if time[1] == 'AM':
        if hour_result >= 24:
            hour_duration -= 24-hour_start
            count_days += 1 + hour_duration//24
        else:
            hour_duration += hour_start
    elif time[1] == 'PM':
        if hour_result >= 12:
            hour_duration -= 12-hour_start
            count_days += 1 + hour_duration//24
        else:
            hour_duration += hour_start

    hour_start = 0
    hora_24 = hour_duration%24

    time[1] = 'AM'
    if hora_24 == 0:
        hora_24 = 12
    elif hora_24 > 11:
        time[1] = 'PM'
        if hora_24 > 12:
            hora_24 -= 12

    new_time = ''
    
    new_time += str(hora_24)+':'
    if minute_result < 10:
        new_time += '0'
    new_time += str(minute_result)+' '+time[1]

    if day != 'False':
        day_num = days.index(day.title()) + count_days
        day_num %= 7
        new_time += ', '+days[day_num]

    if count_days == 1:
        new_time += ' (next day)'
    elif count_days > 1:
        new_time += f' ({count_days} days later)'
    return new_time

print(add_time("3:30 PM", "2:12"))


