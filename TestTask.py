import datetime


def build_free_intervals(timetable,
                         day_start='09:00',
                         day_stop='21:00',
                         min_interval=30):
    """
    Little function to find free intervals in timetable

    :param timetable: list of dictionaries with intervals
    in format [{'start': 'HH:MM', 'stop': 'HH:MM'}, ]
    :param day_start: work start time, default = '09:00'
    :param day_stop: work stop time, default = '21:00'
    :param min_interval: default free interval in minutes, default = 30
    :return: list of free intervals, sorted by 'start', same as input format
    """
    template_interval = datetime.timedelta(minutes=min_interval)
    today = datetime.datetime.today()

    def get_datetime_from_time(time_):
        return datetime.datetime.combine(
            today, datetime.time.fromisoformat(time_)
        )

    def sort_timetable(timetable_):
        return sorted(timetable_, key=lambda x: x['start'])

    def is_long_enough(interval):
        start = get_datetime_from_time(interval['start'])
        finish = get_datetime_from_time(interval['stop'])
        return finish - start >= template_interval

    def build_fulltime_free_intervals(timetable_,
                                      day_start_='09:00',
                                      day_stop_='21:00'):
        intervals_ = []
        ival_start = day_start_

        for ival in sort_timetable(timetable_):
            if ival['start'] == day_start_:
                ival_start = ival['stop']
                continue
            if get_datetime_from_time(ival_start) >= get_datetime_from_time(day_stop_):
                break
            else:
                intervals_.append({
                    'start': ival_start,
                    'stop': ival['start']
                })
                ival_start = ival['stop']
        intervals_.append({
            'start': timetable_[-1]['stop'],
            'stop': day_stop_
        })
        return intervals_

    def cut_free_intervals(timetable_):

        def get_time_str(datetime_):
            return datetime_.isoformat(timespec='minutes')[-5:]

        intervals_ = []
        for ival in timetable_:
            interval = ival.copy()
            while is_long_enough(interval):
                finish = get_time_str(
                    datetime.datetime.combine(
                        today, datetime.time.fromisoformat(interval['start'])
                    ) + template_interval
                )
                intervals_.append({
                    'start': interval['start'],
                    'stop': finish
                })
                interval['start'] = finish
        return intervals_

    return cut_free_intervals(
        build_fulltime_free_intervals(
            sort_timetable(
                timetable
            ), day_start, day_stop)
    )


busy = [
    {'start': '10:30', 'stop': '10:50'},
    {'start': '18:40', 'stop': '18:50'},
    {'start': '14:40', 'stop': '15:50'},
    {'start': '16:40', 'stop': '17:20'},
    {'start': '20:05', 'stop': '20:20'}
]

print(build_free_intervals(busy, day_start='08:00', day_stop='21:20', min_interval=25))
