# !/usr/bin/python
# This program aims to migrate records to a new database using an updated schema

from pymongo import MongoClient

import os

import csh_db_config
import claci_db_config
import zooniverse_config

# mongodb client
mongoConn = MongoClient(csh_db_config.DB_HOST + ':' + str(csh_db_config.DB_PORT))

# connection to old db
claciTransDB = mongoConn[claci_db_config.TRANSCRIPTION_DB_NAME]
claciTransDB.authenticate(claci_db_config.TRANSCRIPTION_DB_USER,
                          claci_db_config.TRANSCRIPTION_DB_PASS)
claciCollection = claciTransDB[claci_db_config.TRANS_DB_MeetingMinColl]

# connection to new db
cshTransDB = mongoConn[csh_db_config.TRANSCRIPTION_DB_NAME]
cshTransDB.authenticate(csh_db_config.TRANSCRIPTION_DB_USER,
                        csh_db_config.TRANSCRIPTION_DB_PASS)
cshCollection = cshTransDB[csh_db_config.TRANS_DB_MeetingMinColl]

# fetch the image filenames in a python list
for record in claciCollection.find():
    cshCollection.insert_one({
        '_id' : record['_id'],
        'file': {
            'height'  : record['height'],
            'origPath': zooniverse_config.Orig_Image_Folder + \
                            '{0:04d}'.format(record['numPage']) + '/' + \
                            record['locationBasedImageFile'],
            'anonPath': zooniverse_config.Anon_Image_Folder + \
                            record['anonymizedImageFile'],
            'size'    : record['size'],
            'width'   : record['width'],
        },
        'scan': {
            'lineNum'      : record['numLine'],
            'itemGroupNum' : record['register'],
            'wordNum'      : record['numWord'],
            'scanNum'      : record['numPage'],
            'pixelLocation': {
                'x': record['locationX'],
                'y': record['locationY']
            }
        }
    })

