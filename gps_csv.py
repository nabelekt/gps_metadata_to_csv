# -----------------------------------------------------------------------------------------------------------

import gps_exif
import sys
import os
import csv

# -----------------------------------------------------------------------------------------------------------

# USER OPTIONS:

# Specify mode to handle the CSV files, see https://docs.python.org/3/library/functions.html#open
FILE_MODE = 'w'

#CSV Options, see https://docs.python.org/3.1/library/csv.html
CSV_QUOTE_OPTION = csv.QUOTE_NONE  # csv.QUOTE_ALL, csv.QUOTE_MINIMAL, csv.QUOTE_NONNUMERIC, or csv.QUOTE_NONE

# -----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    if len(sys.argv) < 3:
      print(f"\nERROR: Not enough arguments given.\nUsage: {sys.argv[0]} relative_image_directory output_csv_filename\nExiting.\n")
      sys.exit(1)

    image_dir = os.path.dirname(os.path.realpath(__file__)) + '/' + sys.argv[1]
    if not os.path.isdir(image_dir):
        print(f"\nERROR: Directory '{image_dir}' could not be found or is not a directory.\nExiting.\n")
        sys.exit(1)

    image_file_names = os.listdir(image_dir)

    coordinates = []

    for image_file_ind in range(len(image_file_names)):
        geotags = gps_exif.get_geotags(image_dir + '/' + image_file_names[image_file_ind])
        (lat, lon) = gps_exif.get_coordinates(geotags)
        coordinates.append((lat, lon))

    # Create CSV file
    output_file = open(sys.argv[2], FILE_MODE)
    output_file.write("lat,lon" + "\n")
    wr = csv.writer(output_file, quoting=CSV_QUOTE_OPTION)
    for row in coordinates:
        wr.writerow(row)
    output_file.close()