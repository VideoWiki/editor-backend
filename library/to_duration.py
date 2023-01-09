from datetime import datetime, timedelta


def convert_to_duration(duration):
    if duration == None:
        return datetime.strptime(str(timedelta(seconds=0)), "%H:%M:%S").time()
    else:
        return datetime.strptime(str(timedelta(seconds=int(duration))), "%H:%M:%S").time()
