def float_to_duration(seconds = 0):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    duration = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return duration
