# !/usr/bin/python
# This program aims to migrate records to a new database using an updated schema

from pymongo import MongoClient

import os

import db_config
import old_db_config
import zooniverse_config

# mongodb client
mongoConn = MongoClient(old_db_config.DB_HOST + ':' + str(db_config.DB_PORT))

# connection to old db
claciTransDB = mongoConn[old_db_config.TRANSCRIPTION_DB_NAME]
claciTransDB.authenticate(old_db_config.TRANSCRIPTION_DB_USER,
                          old_db_config.TRANSCRIPTION_DB_PASS)
claciCollection = claciTransDB[db_config.TRANS_DB_MeetingMinColl]

# connection to new db
cshTransDB = mongoConn[db_config.TRANSCRIPTION_DB_NAME]
cshTransDB.authenticate(db_config.TRANSCRIPTION_DB_USER,
                        db_config.TRANSCRIPTION_DB_PASS)
cshCollection = cshTransDB[db_config.TRANS_DB_MeetingMinColl]

# fetch the image filenames in a python list
for record in claciCollection.find():
    cshCollection.insert_one({
        '_id' : record['_id'],
        'file': {
            'anonName': record['anonymizedImageFile'],
            'height'  : record['height'],
            'name'    : record['locationBasedImageFile'],
            'path'    : zooniverse_config.Image_Folder,
            'size'    : getFileSize(record),
            'width'   : record['width'],
        },
        'page': {
            'lineNum'      : record['numLine'],
            'registerNum'  : record['register'],
            'wordNum'      : record['numWord'],
            'pageNum'      : record['numPage'],
            'pixelLocation': {
                'x': record['locationX'],
                'y': record['locationY']
            }
        }
    })

# helper function to get file size
def getFileSize(record):
    if 'size' in record:
        return record['size']

    return os.path.getsize(zooniverse_config.Image_Folder + \
                           resultItem['anonymizedImageFile'])
