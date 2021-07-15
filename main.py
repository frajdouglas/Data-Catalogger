# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:23:39 2021

@author: FraserDouglas
"""

import datetime
import os
import threading
import utils



# Obtain the latest metadata and store it in a dictionary save as pickle file. 
# Rename the previous "new_metadata" file as the "old_metadata" file ready for comparison
    
def catalogger(store_list,save_path,log_save_path,begin_time):
    """Maps a free network drive letter to the defined Azure file share,
       collects metadata for each file and identifies current,deleted and new
       files since last run. Once finished, unmaps network drive.
   
    Parameters
    ----------
    store_list : str
        List of Azure file stores to catalog
    save_path : str
        Location to save results
    log_save_path : str
        Location to save log of run
    begin_time : datetime
        Time of metadata collection start time

    """
    
    for file_storage in store_list:
        try:
            print("Starting " + file_storage + " Metadata Collection")
            drive_letter,drive_connection,datastore_name = utils.map_drive(file_storage)
            utils.get_metadata(drive_letter,save_path,datastore_name)
            utils.get_sets(save_path,datastore_name)
            # Log time for New, Deleted and Modified Files Identification completion
            with open(log_save_path,"a") as file:
                file.write("Metadata Updated, New and Deleted Files Identified: " + str(file_storage) + " " + str(datetime.datetime.now()-begin_time) + "\n")
            print("Metadata Updated, New and Deleted Files Identified: " + str(file_storage) + " " +str(datetime.datetime.now()-begin_time))
    
    
            # Combine file list, new files list and deleted files list and errors list into excel file and save into the drive. Also save the csvs for each file storage into ESRIVM2 ready to be combined.
            utils.get_summary(save_path, drive_connection, drive_letter,datastore_name)
    
            # Unmap drive and move onto next file storage
            utils.unmap_drive(drive_letter)
        except Exception as error:
            print(error)
            with open(log_save_path,"a") as file:
                file.write(str(error) + str(file_storage))
            utils.unmap_drive(drive_letter)
            continue

def main(save_path):
    """Creates Threads for each set of Azure file stores metadata collection
   
    Parameters
    ----------
    save_path : str
        Location to save results

    """
    # Azure File Store Locations. Each list details which file stores will be searched by each thread.
    # Each list should be roughly the same size of drive.
    store_list_1 = ['********']
    store_list_2 = ['********']
    store_list_3 = ['********']
    store_list_4 = ['********']
    store_list_5 = ['********']
    store_list_6 = ['********']
    store_list_7 = ['********']
    store_list_8 = ['********']
       
    # Log file save paths
    log_save_path = save_path + "run_log.txt"
    all_runs_path = save_path + "all_runs_log.txt"
    
    
    # Create a runs log file if it doesn't exist already and logs start time of run. This logs every run of the script.
    if os.path.exists(all_runs_path):
        with open(all_runs_path, "a") as file:
            file.write("Start Time: " + str(datetime.datetime.now()) + "\n")
            
    else:
        with open(all_runs_path, "w") as file:
            file.write("Start Time: " + str(datetime.datetime.now()) + "\n")
    
    # Start recording time of run and record in the log for this specific run
    begin_time = str(datetime.datetime.now())
    with open(log_save_path, "w+") as file:
        file.write("Start Time: " + str(datetime.datetime.now()) + "\n")
    
    print("Start Time: " + str(datetime.datetime.now()))
    
    # This can be looped
    
    t1 = threading.Thread(target=catalogger,args=[store_list_1,save_path,log_save_path,begin_time])
    t2 = threading.Thread(target=catalogger,args=[store_list_2,save_path,log_save_path,begin_time])
    t3 = threading.Thread(target=catalogger,args=[store_list_3,save_path,log_save_path,begin_time])
    t4 = threading.Thread(target=catalogger,args=[store_list_4,save_path,log_save_path,begin_time])
    t5 = threading.Thread(target=catalogger,args=[store_list_5,save_path,log_save_path,begin_time])
    t6 = threading.Thread(target=catalogger,args=[store_list_6,save_path,log_save_path,begin_time])
    t7 = threading.Thread(target=catalogger,args=[store_list_7,save_path,log_save_path,begin_time])
    t8 = threading.Thread(target=catalogger,args=[store_list_8,save_path,log_save_path,begin_time])
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    
    # Log end time for this specific run and log.
    with open(all_runs_path,"a") as file:    
        file.write("Finish Time: " + str(datetime.datetime.now()) + "\n")

    

if __name__ == '__main__':
    main()