# Some code taken and modified from https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import sys
import os

def get_geotags(file_path):

    image = Image.open(file_path)
    image.verify()
    exif = image._getexif()

    if not exif:
        print()
        raise Exception(f"No EXIF metadata found for file {file_path}")

    geotags = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                print()
                raise Exception(f"No EXIF geotags found for file {file_path}")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotags[val] = exif[idx][key]

    return geotags


def decimal_to_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    coord = round(degrees + minutes + seconds, 5)

    if ref in ['S', 'W']:
        coord = -coord

    return coord


def get_coordinates(geotags):
    lat = decimal_to_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = decimal_to_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)


if __name__ == '__main__':

    if len(sys.argv) < 2:
      print(f"\nERROR: Not enough arguments given.\nUsage: {sys.argv[0]} relative_image_file_path\nExiting.\n")
      sys.exit(1)

    image_path = os.path.dirname(os.path.realpath(__file__)) + '/' + sys.argv[1]
    if not os.path.exists(image_path):
        print(f"\nERROR: File '{image_path}' could not be found.\nExiting.\n")
        sys.exit(1)

    geotags = get_geotags(image_path)
    (lat, lon) = get_coordinates(geotags)
    print(lat, lon)

    print()