# !/usr/bin/python
# This program takes a list of images as inputs (i.e., a file), adds them to subject sets of size n, and sends the subject sets to Zooniverse
# Code adapted from Mona Mishra

from panoptes_client import SubjectSet, Subject, Project, Panoptes
from pymongo import MongoClient

import argparse
import datetime
import itertools

import csh_db_config
import zooniverse_config

def main():
    ap = argparse.ArgumentParser(description='Given a list of images, bins them into subject sets of size n')

    # require file path to read in images
    ap.add_argument('-f', '--filename', required=True, dest='filename', type=str,
                    help='The name of the file from which to read the images')

    # optionally require subject set size; defaults to 1000
    ap.add_argument('-n', '--size', required=False, dest='n', type=int, default=1000,
                    help='The maximum number of images a subject set should contain. \
                          The value should be between 1 and 10000, inclusive')

    # parse args into variables and check values
    args = vars(ap.parse_args())

    filename = args['filename'][0] if args['filename'] else None
    n        = args['n'] if args['n'] else None

    if not (n >= 1 and n <= 10000):
        raise ValueError('n must be between 1 and 10000, inclusive')

    # connect to zooniverse
    Panoptes.connect(username=zooniverse_config.Zooniverse_USERNAME,
                     password=zooniverse_config.Zooniverse_PASS)
    project = Project.find(zooniverse_config.Project_ID)

    # connection to mongodb
    mongoConn = MongoClient(csh_db_config.DB_HOST + ":" + str(csh_db_config.DB_PORT))
    cshTransDB = mongoConn[csh_db_config.TRANSCRIPTION_DB_NAME]
    cshTransDB.authenticate(csh_db_config.TRANSCRIPTION_DB_USER,
                            csh_db_config.TRANSCRIPTION_DB_PASS)
    cshCollection = cshTransDB[csh_db_config.TRANS_DB_MeetingMinColl]
    cshSubjectSets = cshTransDB[csh_db_config.TRANS_DB_SubjectSets]

    # track subject sets being created
    subjectSets = []

    # get the image filenames in a Python list
    with open(filename) as handle:
        filenames = handle.readlines()

    # divide files into groups of n
    filegroups = list([e for e in t if e != None] for t in itertools.zip_longest(*([iter(filenames)] * n)))

    for group in filegroups:
        displayName = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())

        # create a new subject set
        subjectSet = SubjectSet()
        subjectSet.links.project = project
        subjectSet.display_name = displayName
        subjectSet.save()

        subjectSetId = subjectSet.id
        subjectSets.append(subjectSetId)

        # create a new subject for each file and add to the subject set
        for filename in group:
            # create a new subject
            subject = Subject()
            subject.links.project = project
            subject.add_location(cshCollection.find_one({'_id': filename})['file']['anonPath'])
            subject.save()

            # add to subject set
            subjectSet.add(subject)

            # retrieve and update the record from mongodb
            updateQuery = {
               '$set': {
                    'canCrowdsource': True
                },
               '$set': {
                   'transcription': {
                       'numClassifications': 5,
                       'subjectSetId'      : subjectSetId,
                       'status'            : 'sent'
                   }
               }
            }
            record = cshCollection.find_one_and_update({'_id': filename}, updateQuery)

        # create subject set record
        cshSubjectSets.insert_one({
            '_id'        : subjectSetId,
            'status'     : 'sent',
            'displayName': dsplayName
        })
        subjectSet.save()

    # add subject sets to the workflow
    workflow = project.links.workflows[0]
    workflow.add_subject_sets(subjectSets)
    workflow.save()

    # print helpful information to the console
    print('{} subject sets created with the following IDs: {}'.format(len(subjectSets), subjectSets))
            
if __name__ == '__main__':
    main()

