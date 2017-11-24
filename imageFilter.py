# !/usr/bin/python
# This program aims to filter out images which are not suitable to be sent to Zooniverse

from pymongo import MongoClient

import argparse
import os

import csh_db_config

def main():
    parser = argparse.ArgumentParser(description='Filter out images which are not suitable to be crowdsourced.')

    # require file path for images
    parser.add_argument('--path', required=True,
                        nargs=1, action='store', type=str, dest='path',
                        help='The file path at which the images are stored')

    # optionally require file size, width, and height lower and upper bound limits
    parser.add_argument('--size_min', required=False,
                        nargs=1, action='store', type=int, dest='size_min',
                        help='The minimum allowable image size in bytes, inclusive')
    parser.add_argument('--size_max', required=False,
                        nargs=1, action='store', type=int, dest='size_max',
                        help='The maximum allowable image size in bytes, inclusive')
    parser.add_argument('--height_min', required=False,
                        nargs=1, action='store', type=int, dest='height_min',
                        help='The minimum allowable image height in pixels, inclusive')
    parser.add_argument('--height_max', required=False,
                        nargs=1, action='store', type=int, dest='height_max',
                        help='The maximum allowable image height in pixels, inclusive')
    parser.add_argument('--width_min', required=False,
                        nargs=1, action='store', type=int, dest='width_min',
                        help='The minimum allowable image width in pixels, inclusive')
    parser.add_argument('--width_max', required=False,
                        nargs=1, action='store', type=int, dest='width_max',
                        help='The maximum allowable image width in pixels, inclusive')

    # parse args into variables
    args = vars(parser.parse_args())

    path       = args['path'][0] if args['path'] else None
    size_min   = args['size_min'][0] if args['size_min'] else None
    size_max   = args['size_max'][0] if args['size_max'] else None
    height_min = args['height_min'][0] if args['height_min'] else None
    height_max = args['height_max'][0] if args['height_min'] else None
    width_min  = args['width_min'][0] if args['width_min'] else None
    width_max  = args['width_max'][0] if args['width_max'] else None

    # list of images that are acceptable to be crowdsourced
    acceptable = []

    # mongodb client and connection to db
    mongoConn = MongoClient(csh_db_config.DB_HOST + ':' + str(csh_db_config.DB_PORT))
    cshTransDB = mongoConn[csh_db_config.TRANSCRIPTION_DB_NAME]
    cshTransDB.authenticate(csh_db_config.TRANSCRIPTION_DB_USER,
                        csh_db_config.TRANSCRIPTION_DB_PASS)
    cshCollection = cshTransDB[csh_db_config.TRANS_DB_MeetingMinColl]

    # evaluate image fles
    for filename in os.listdir(path):
        # retrieve file properties from database
        filename = os.path.splitext(filename)[0]
        record = cshCollection.find_one({'_id': filename})
        properties = record['file']

        # check size threshold
        size = properties['size']
        if size_min and size < size_min:
           continue
        if size_max and size > size_max:
           continue

        # check height threshold
        height = properties['height']
        if height_min and height < height_min:
           continue
        if height_max and height > size_max:
           continue

        # check width threshold
        width = properties['width']
        if width_min and width < width_min:
           continue
        if width_max and width > width_max:
           continue

        acceptable.append(filename)

    # save data
    with open('acceptable_images.txt', 'w') as handle:
        for f in acceptable:
            handle.write('{}\n'.format(f))

if __name__ == '__main__':
    main()

