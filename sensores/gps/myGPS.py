import time

#reading values from sensor
class MyGPS(object):
    HEMISPHERES = ('N', 'S', 'E', 'W')

    def __init__(self, local_offset=0):
        # Object status
        self.fix_time = 0

        # Time
        self.timestamp = (0, 0, 0)
        self.date = (0, 0, 0)
        self.local_offset = local_offset

        # Position/Motion
        self.latitude = (0, 0.0, 'N')
        self.longitude = (0, 0.0, 'W')
        self.speed = (0.0, 0.0, 0.0)
        self.course = 0.0

        # GPS Info
        self.valid = False

    def upload(self, data):

        # Timestamp
        try:
            utc = data[1]
            if utc:
                hours = int(utc[0:2]) + self.local_offset
                minutes = int(utc[2:4])
                seconds = float(utc[4:])
                self.timestamp = (hours, minutes, seconds)
            else:
                self.timestamp = (0, 0, 0)
        # Bad Timestamp value present
        except ValueError:
            return False

        #Date
        try:
            date = data[9]
            if date:
                day = int(date[0:2])
                month = int(date[2:4])
                year = int(date[4:6])
                self.date = (day, month, year)
            else:
                self.date = (0, 0, 0)
        # Bad Date value present
        except ValueError:
            return False

        # Check Receiver Data Valid Flag
        if data[2] == 'A':
            # Longitude/Latitude
            try:
                # Latitude
                l_string = data[3]
                lat_degs = int(l_string[0:2])
                lat_mins = float(l_string[2:])
                lat_hemi = data[4]

                # Longitude
                l_string = data[5]
                lon_degs = int(l_string[0:3])
                lon_mins = float(l_string[3:])
                lon_hemi = data[6]
            except ValueError:
                return False

            if lat_hemi not in self.HEMISPHERES:
                return False

            if lon_hemi not in self.HEMISPHERES:
                return False

            # Speed
            try:
                spd_knt = float(data[7])
            except ValueError:
                return False

            # Course
            '''
            try:
                print('course')
                course = float(data[8])
            except ValueError:
                return False
            '''

            # Update Object Data
            self.latitude = (lat_degs, lat_mins, lat_hemi)
            self.longitude = (lon_degs, lon_mins, lon_hemi)
            # Include mph and hm/h
            self.speed = (spd_knt, spd_knt * 1.151, spd_knt * 1.852)
            #self.course = course
            self.valid = True

            # Update Last Fix Time
            try:
                self.fix_time = pyb.millis()
            except NameError:
                self.fix_time = time.time()

            #self.new_fix_time()
