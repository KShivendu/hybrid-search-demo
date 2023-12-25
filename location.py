from PIL import Image
import exifread

def get_gps_coordinates(image_path):
    with open(image_path, 'rb') as image_file:
        exif_data = exifread.process_file(image_file)

        # Check if GPS tags are in the EXIF data
        if 'GPS GPSLatitude' in exif_data and 'GPS GPSLongitude' in exif_data:
            lat_ref = exif_data['GPS GPSLatitudeRef'].values
            lat = exif_data['GPS GPSLatitude'].values
            lon_ref = exif_data['GPS GPSLongitudeRef'].values
            lon = exif_data['GPS GPSLongitude'].values

            lat = convert_to_degrees(lat)
            lon = convert_to_degrees(lon)

            if lat is None or lon is None:
                return None, None

            if lat_ref != "N":
                lat = -lat
            if lon_ref != "E":
                lon = -lon

            return lat, lon
        else:
            return None, None

def convert_to_degrees(value):
    try:
        d, m, s = value
        return d.num / d.den + (m.num / m.den / 60) + (s.num / s.den / 3600)
    except ZeroDivisionError:
        return 0

if __name__ == '__main__':
    image_path = 'data/20231219_140217.jpg'
    print(get_gps_coordinates(image_path))
