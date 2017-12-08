#This program takes the list of classifications crowdsourced in Zooniverse and updates the same in MongoDB corresponding to the subjects.

#Importing required packages
from panoptes_client import SubjectSet, Subject, Project, Panoptes
from pymongo import MongoClient
import argparse
import datetime
import itertools
import csv
import json
import io
import csh_db_config
import zooniverse_config

# connect to zooniverse
Panoptes.connect(username=zooniverse_config.Zooniverse_USERNAME, password=zooniverse_config.Zooniverse_PASS)
project = Project.find(zooniverse_config.Project_ID)

# connection to mongodb
mongoConn = MongoClient(csh_db_config.DB_HOST + ":" + str(csh_db_config.DB_PORT))
cshTransDB = mongoConn[csh_db_config.TRANSCRIPTION_DB_NAME]
cshTransDB.authenticate(csh_db_config.TRANSCRIPTION_DB_USER,
                            csh_db_config.TRANSCRIPTION_DB_PASS)
cshCollection = cshTransDB[csh_db_config.TRANS_DB_MeetingMinColl]
cshSubjectSets = cshTransDB[csh_db_config.TRANS_DB_SubjectSets]

classification_export = Project(zooniverse_config.Project_ID).get_export('classifications')
classification = classification_export.content.decode('utf-8')


#Traverses through each row of classifications in the JSON file created by zooniverse and assigns them to appropriate headers
for row in csv.DictReader(io.StringIO(classification)):

        annotations = json.loads(row['annotations'])
        subject_data = json.loads(row['subject_data'])
        transcription_question_1 = ''
        transcription_text_1 = ''
        transcription_question_2 = ''
        transcription_text_2 = ''
        transcription_filename = ''

        subject_id = row['subject_ids']
        subject_id = str(subject_id)
        
        #This part of code takes care of the subjects with the old version of workflow that do not have the updated file name
        if subject_id in ['1287013','1287029','1287027','1287024','1287018','1287030','1287023','1287019','1287032','1287031','1287020','1287014','1287018','1287015','1287015','1287018']:
           transcription_filename = str(subject_data[subject_id]['image'])
           transcription_filename = transcription_filename.rstrip('.jpg')
            
        else:
          transcription_filename = str(subject_data[subject_id]['Filename'])
          transcription_filename = transcription_filename.rstrip('.jpg')
            
        
        #Parsing the file/Flattening the JSON output from zooniverse into individual fields
        for task in annotations:
                    try:
                        if 'Is there a word in this image?' in task['task_label']:
                            if task['value'] is not None:
                                transcription_question_1 = str(task['task_label'])
                                transcription_text_1 = str(task['value'])
                    except KeyError:
                        continue
                    try:
                        if 'Please type the word(s) that appears in this image' in task['task_label']:
                            if task['value'] is not None:
                                transcription_question_2 = str(task['task_label'])
                                transcription_text_2 = str(task['value'])
                    except KeyError:
                        continue
                        
              # Retrieve and update the record from MongoDB  
                    updateQuery = {
                       
                       '$set':{
                    
                           'responses': [{
                                   'labellerId': row['user_id'],
                                   'type'      : transcription_text_1,
                                   'label'     : transcription_text_2
                                   }],
                                
                            'transcription': {
                                    
                                    'status'   : 'done'
                                    }
                            
                            } 
                        }
                    record = cshCollection.find_one_and_update({'_id': transcription_filename}, updateQuery)
