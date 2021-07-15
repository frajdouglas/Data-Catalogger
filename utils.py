# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:20:22 2021

@author: FraserDouglas
"""

import subprocess
import os
import datetime
import pickle
import pandas as pd

# Map the specified azure file storage to a free drive, save which drive has been used
def map_drive(conn_string):
    """Maps a free network drive letter to the defined Azure file share
   
    Parameters
    ----------
    conn_string : str
        Connection string with credentials to Azure file share

    Returns
    -------
    drive_letter : str
        Drive letter of the drive connected to the file share
    drive_connection : str
        Full path to the Azure file store connected to the drive
    """            
    # raw string should be passed to subprocess.run function
    # backslashes in Python need to be escaped, ie, to run this '\\servername\path\resource.txt' you must do either '\\\\servername\\path\\resource.txt' or r'\\servername\path\resource.txt'
    drive_connect = subprocess.run('net use * ' + conn_string, shell=True, capture_output = True,check = True)
    
    # Save prompt response as a string
    print(drive_connect.stdout.decode())
    output_text = drive_connect.stdout.decode()

    # Save the drive letter as a variable ready for disconnecting from network drive
    # Split string by space delimiter
    split_string = output_text.split()
    # Find the drive letter which should be the second item
    drive_letter = split_string[1]
    drive_letter = drive_letter + '\\'
    drive_connection = drive_letter + conn_string
    print(drive_letter)
    print(drive_connection)
    
    sub_string = drive_connection.split(".net\\",1)[1]
    datastore_name = sub_string.split(" /u",1)[0]
    
    return(drive_letter, drive_connection,datastore_name)

# Disconnect from drive
def unmap_drive(drive_letter):
    """Disconnects a specified network drive
   
    Parameters
    ----------
    drive_letter : str
        Drive letter of the drive connected to the file share

    """
    # Create prompt command statement to unmap drive_letter, use the drive_letter to unmap from this network drive
    delete_command = 'net use ' + drive_letter[0:2] + ' /del'   
    drive_disconnect = subprocess.run(delete_command, shell=True, capture_output = True,check = True)
    print(drive_disconnect.stdout.decode())
    return(drive_disconnect.stdout.decode())

# Gather metadata
def get_metadata(drive_letter ,save_path,datastore_name):
    # Create counters and empty dictionaries and define pickle save path
    sub_dict = {}
    error_dict = {}
    count = 0
    error_count = 0
    dict_dir = f'{save_path}{datastore_name}_new_metadata.pickle'
    old_dict_dir = f'{save_path}{datastore_name}_old_metadata.pickle'
    backup_dir = f'{save_path}{datastore_name}_backup_old_metadata.pickle'
    error_dir = f'{save_path}{datastore_name}_new_metadata_errors.pickle'
    old_error_dict_dir = f'{save_path}{datastore_name}_old_errors_metadata.pickle'
    backup_error_dir = f'{save_path}{datastore_name}_backup_old_errors_metadata.pickle'
    
    # Rename metadata pickle files 
    if os.path.exists(backup_dir):
        os.remove(backup_dir)
    else:
        pass

    if os.path.exists(old_dict_dir):
            os.rename(old_dict_dir, backup_dir)
    else:
        pass

    if os.path.exists(dict_dir):
        os.rename(dict_dir, old_dict_dir)
        
    else:
        pass
    
    # Rename error pickle files 
    if os.path.exists(backup_error_dir):
        os.remove(backup_error_dir)
    else:
        pass
    
    if os.path.exists(old_error_dict_dir):
            os.rename(old_error_dict_dir, backup_error_dir)
    else:
        pass

    if os.path.exists(error_dir):
        os.rename(error_dir, old_error_dict_dir)
    else:
        pass          
    
    # Walk through files and get statistics, add them to a dictionary  
    for(drive_letter,dirs,files) in os.walk(drive_letter):
        for x in files:
            try:
                count += 1
                sub_dict[count] = {}
                file_path = os.path.join(drive_letter,x)
                path = file_path[3:]
                #print(path)
                size = os.path.getsize(file_path)
                split_text = os.path.splitext(file_path)
                file_type = split_text[1]
                ctime = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                sub_dict[count]['file_path'] = path
                sub_dict[count]['mtime'] = mtime
                sub_dict[count]['ctime'] = ctime
                sub_dict[count]['file_type'] = file_type
                sub_dict[count]['size_mb'] = round(size/(1000000), 2)
            # Handle errors and log them in dictionary
            except Exception as error:
                    error_count += 1
                    error_dict[error_count] = {}
                    error_type = type(error).__name__
                    error_dict[error_count]['file path'] = path
                    error_dict[error_count]['error'] = error_type 
                    print(error_dict)
                    continue
    # Save new metadata dictionary as pickle file
    with open(dict_dir,"wb") as pickled_storage:
        pickle.dump(sub_dict,pickled_storage)

    # Save new error dictionary as pickle file
    with open (error_dir,"wb") as pickled_storage:
        pickle.dump(error_dict,pickled_storage)

# Classify metadata into newand deleted 
def get_sets(save_path,datastore_name):
    # Create empty sets
    old_set = set()
    new_set = set()

    # Create empty dictionary for reformatting of old dictionary
    old_metadata_location = f'{save_path}{datastore_name}_old_metadata.pickle'
    new_metadata_location = f'{save_path}{datastore_name}_new_metadata.pickle'
    deleted_files_set_save_location = f'{save_path}{datastore_name}_deleted_files_set.pickle'
    new_files_set_save_location = f'{save_path}{datastore_name}_new_files_set.pickle'

    # Convert old dictionary to set
    if os.path.exists(old_metadata_location):
        with open(old_metadata_location, 'rb') as opened_file:
            unpickled_file = pickle.load(opened_file)

        for x in unpickled_file: 
            file_path = unpickled_file.get(x).get('file_path')
            old_set.add(file_path)
    else:
        old_set = set()

    # Convert new dictionary to set
    with open(new_metadata_location, 'rb') as opened_file:
        unpickled_file = pickle.load(opened_file)

    for x in unpickled_file: 
        file_path = unpickled_file.get(x).get('file_path')
        new_set.add(file_path)
        
    # Find deleted files and save to pickle
    deleted_files = old_set.difference(new_set)
    with open(deleted_files_set_save_location ,"wb") as file:
        pickle.dump(deleted_files,file)
        opened_file.close()     
        print("Deleted files dumped " + str(datetime.datetime.now()))
    
    
    # Find new files and save to pickle
    new_files = new_set.difference(old_set)
    with open(new_files_set_save_location ,"wb") as file:
        pickle.dump(new_files,file)
        opened_file.close()     
        print("New files Dumped " + str(datetime.datetime.now()))

    # Delete variables for deleted files set and new files set
    del deleted_files
    del new_files
    
        # Delete unpickled_file variable
    del unpickled_file
# combine all results into master spreadsheet
def get_summary(save_path, drive_connection, drive_letter,datastore_name):
    # Combine file list, new files list and deleted files list and errors list into excel file and save into the drive. Also save the csvs for each file storage into ESRIVM2 ready to be combined.
    # Reconstruct the drive letter for specifying drive save path   
    dict_dir = f'{save_path}{datastore_name}_new_metadata.pickle'
    error_dir = f'{save_path}{datastore_name}_new_metadata_errors.pickle'
    deleted_files_set_save_location = f'{save_path}{datastore_name}_deleted_files_set.pickle'
    new_files_set_save_location = f'{save_path}{datastore_name}_new_files_set.pickle'
    
    current_files_save_location = f'{save_path}{datastore_name}_current_files.csv'
    new_files_save_location = f'{save_path}{datastore_name}_new_files.csv'
    deleted_files_save_location = f'{save_path}{datastore_name}_deleted_files.csv'
    error_list_save_location = f'{save_path}{datastore_name}_errors_list.csv'

    # Save a csv for each of the file lists into the save path folder.

    if os.path.exists(dict_dir):
        opened_file = open(dict_dir, 'rb')
        unpickled_file = pickle.load(opened_file)
        opened_file.close()
        df1 = pd.DataFrame.from_dict(unpickled_file, orient = 'index')
        df1.to_csv(current_files_save_location,index=True)
        

    if os.path.exists(new_files_set_save_location):
        with open(new_files_set_save_location, 'rb') as opened_file:
            unpickled_file = pickle.load(opened_file)
        data_list = list(unpickled_file)
        df2 = pd.DataFrame(data_list)
        df2.to_csv(new_files_save_location,index=True)

    if os.path.exists(deleted_files_set_save_location):
        with open(deleted_files_set_save_location, 'rb') as opened_file:
            unpickled_file = pickle.load(opened_file)
        data_list = list(unpickled_file)
        df3 = pd.DataFrame(data_list)
        df3.to_csv(deleted_files_save_location,index=True)


    if os.path.exists(error_dir):
        with open(error_dir, 'rb') as opened_file:
            unpickled_file = pickle.load(opened_file)
        df4 = pd.DataFrame.from_dict(unpickled_file, orient = 'index')
        df4.to_csv(error_list_save_location,index=True)
        
    print('Metadata Summary CSVs saved in ' + save_path)

    # Save an excel file in the datastore location 

    writer = pd.ExcelWriter(drive_letter + datastore_name + '_files_summary.xlsx', engine='openpyxl')
    df1.to_excel(writer, sheet_name='Current_Files')
    df2.to_excel(writer, sheet_name='New_Files')
    df3.to_excel(writer, sheet_name='Deleted_Files')
    df4.to_excel(writer, sheet_name='Errors_List')
    writer.save()
    
    print('Metadata Summary Saved in ' + drive_letter + datastore_name)
    
