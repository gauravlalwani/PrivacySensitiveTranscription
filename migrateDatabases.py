# !/usr/bin/python
# This program aims to migrate records to a new database using an updated schema

from pymogno import MongoClient

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
for resultItem in calciCollection.find():
    cshCollection.insert_one({
        '_id': resultItem['_id'],
        'file': {
            'anonName': resultItem['anonymizedImageFile'],
            'height'  : resultItem['height'],
            'name'    : resultItem['locationBasedImageFile'],
            'path'    : zooniverse_config.Image_Folder,
            'size'    : resultItem['size'],
            'width'   : resultItem['width'],
        },
        'page': {
            'lineNum'      : resultItem['numLine'],
            'registerNum'  : resultItem['register'],
            'wordNum'      : resultItem['numWord'],
            'pageNum'      : resultItem['numPage'],
            'pixelLocation': {
                'x': resultItem['locationX'],
                'y': resultItem['locationY']
            }
        }
    })
