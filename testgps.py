import gps

# Connect to gpsd
session = gps.gps(host="localhost", port="2947", mode=gps.WATCH_ENABLE)

while True:
    # Get a GPS report
    report = session.next()
    if report['class'] == 'TPV':  # Only print valid position reports
        print(f"Latitude: {report.lat}, Longitude: {report.lon}, Altitude: {report.alt}")
