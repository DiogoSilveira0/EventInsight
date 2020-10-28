# to show that method convert is ok

def convert (d, m, hem):
    aux = str(m).split('.')
    m = int(aux[0])
    s = float(aux[1][0:2]+'.'+aux[1][2:])
    degrees = d + (m/60) + (s/3600)
    if hem == 'S' or hem == 'W':
        degrees = -degrees
    precision = 4
    return "{:.{}f}".format( degrees, precision )

#41.1496° N 8.611° W
#41°8'58.6'' N 8°36.659' W
lat = convert(41, 8.586, 'N')
lon = convert(8, 36.659, 'W')
print('Latitude:' + lat + '\nLongitude:' + lon)
