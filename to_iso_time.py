import datetime
def to_iso_time(timestamp):
    iso_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            # add 4 hours to get UTC time
    iso_time = datetime.datetime.fromisoformat(iso_time) + datetime.timedelta(hours=5)
            # replace space with T and add Z to end
    iso_time = iso_time.isoformat().replace(' ', 'T') + 'Z'
    return iso_time