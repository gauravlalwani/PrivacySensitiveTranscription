# !/usr/bin/python
# This program aims at sending subject sets to Zooniverse
# Originally authored by Mona Mishra

from panoptes_client import SubjectSet, Subject, Project, Panoptes
from pymongo import MongoClient

import db_config
import zooniverse_config

# connection to zooniverse
Panoptes.connect(username=zooniverse_config.Zooniverse_USERNAME,
                 password=zooniverse_config.Zooniverse_PASS)

# find the project using project id and subject set id
project = Project.find(zooniverse_config.Project_ID);
subject_set=SubjectSet.find(zooniverse_config.Subject_Set_ID);

# connection to mongodb
mongoConn = MongoClient(db_config.DB_HOST + ":" + str(db_config.DB_PORT))
claciTransDB = mongoConn[db_config.TRANSCRIPTION_DB_NAME]
claciTransDB.authenticate(db_config.TRANSCRIPTION_DB_USER,      #DB authentication
                          db_config.TRANSCRIPTION_DB_PASS)
transWordColl = claciTransDB[db_config.TRANS_DB_MeetingMinColl] #transWordColl collection in claciTransDB that holds all the records

# fetch the image filenames in a python list
for resultItem in transWordColl.find():
	subject = Subject()
	subject.links.project = project
	fileLocation = zooniverse_config.Image_Folder + resultItem["anonymizedImageFile"]
	subject.add_location(fileLocation)

	# saves locationBasedImageFile and ID as the metadata
	subject.metadata['locationBasedImageFile'] = resultItem["locationBasedImageFile"];
	subject.metadata['ID'] = resultItem["_id"];
	subject.save()

	# saving the subject in subject set
	subject_set.add(subject)

# add subject set to 1st workflow in project
workflow = project.links.workflows[0]
workflow.add_subject_sets([subject_set])
