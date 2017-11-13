# !/usr/bin/python
# This program takes a list of images as inputs (i.e., a file) and bins them into subject sets of size n
# Code adapted from Mona Mishra

import argparse

from panoptes_client import SubjectSet, Subject, Project, Panoptes
from pymongo import MongoClient

import db_config
import zooniverse_config

# get filename and subject set size as input from the command line
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--filename', required=True, dest='filename',
                help='The name of the file from which to read the images')
ap.add_argument('-n', '--size', required=False, dest='n',
                help='The maximum number of images a subject set should contain. \
                      The value should be between 1 and 10000, inclusive')
args = vars(ap.parse_args())

filename = args['filename']
try:
    n = args['n']
    assert(n > 1 and n < 10001)
except:
    n = 1000

# connect to zooniverse
Panoptes.connect(username=zooniverse_config.Zooniverse_USERNAME,
                 password=zooniverse_config.Zooniverse_PASS)

# find the project using project id and subject set id
project = Project.find(zooniverse_config.Project_ID);

# connection to mongodb
mongoConn = MongoClient(db_config.DB_HOST + ":" + str(db_config.DB_PORT))
claciTransDB = mongoConn[db_config.TRANSCRIPTION_DB_NAME]
claciTransDB.authenticate(db_config.TRANSCRIPTION_DB_USER,      #DB authentication
                          db_config.TRANSCRIPTION_DB_PASS)

# get the image filenames in a Python list
with open(filename) as handle:
    filenames = handle.readlines()

# divide files into groups of n
filegroups = list([e for e in t if e != None] for t in itertools.zip_longest(*([iter(filenames)] * n)))

for group in filegroups:
    # create a new subject set for each file group
    subjectSet = SubjectSet()

    # create a new subject for each file and add to the subject set
    for filename in group:
        subject = Subject()
        subject.links.project = project
        fileLocation = zooniverse_config.Image_Folder + filename
        subject.add_location(fileLocation)

        # saves locationBasedImageFile and ID as the metadata
        subject.metadata['ID'] = resultItem["_id"];
        subject.save()

        # saving the subject in subject set
        subjectSet.add(subject)

        # update file subject set metadata attribute
