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
    parser.add_argument('--size_l', required=False,
                        nargs=1, action='store', type=int, dest='size_l',
                        help='The file size lower bound in bytes, inclusive')
    parser.add_argument('--size_u', required=False,
                        nargs=1, action='store', type=int, dest='size_u',
                        help='The file size upper bound in bytes, inclusive')
    parser.add_argument('--height_l', required=False,
                        nargs=1, action='store', type=int, dest='height_l',
                        help='The file height lower bound in pixels, inclusive')
    parser.add_argument('--height_u', required=False,
                        nargs=1, action='store', type=int, dest='height_u',
                        help='The file height upper bound in pixels, inclusive')
    parser.add_argument('--width_l', required=False,
                        nargs=1, action='store', type=int, dest='width_l',
                        help='The file width lower bound in pixels, inclusive')
    parser.add_argument('--width_u', required=False,
                        nargs=1, action='store', type=int, dest='width_u',
                        help='The file width upper bound in pixels, inclusive')

    # parse args into variables
    args = vars(parser.parse_args())

    path     = args['path'][0]
    size_l   = args['size_l']
    size_u   = args['size_u']
    height_l = args['height_l']
    height_u = args['height_u']
    width_l  = args['width_l']
    width_u  = args['width_u']

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
        if size_l and size < size_l:
           continue
        if size_u and size > size_u:
           continue

        # check height threshold
        height = properties['height']
        if height_l and height < height_l:
           continue
        if height_u and height > size_u:
           continue

        # check width threshold
        width = properties['width']
        if width_l and width < width_l:
           continue
        if width_u and width > width_u:
           continue

        acceptable.append(filename)

    # save data
    with open('acceptable_images.txt', 'w') as handle:
        for f in acceptable:
            handle.write('{}\n'.format(f))

if __name__ == '__main__':
    main()

