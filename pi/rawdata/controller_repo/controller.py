#!/usr/bin/env python
# This file aim at the purpose of reading from the TODO file, read from the rfid status, read from the feeder status,PIN status, then determine what to do.
# It's action will be described as below:

# Read lines from feeder status file, schedule TODO file, rfid status file and store them into caches (lists)
feederStatusFileName = "/home/pi/shared_data/feeder.status"
scheduleTODOFileName = "/home/pi/shared_data/schedule.todo"
rfidStatusFileName = "/home/pi/rawdata/rfidstatus.txt"
pinTODOFolderName = "/home/pi/rawdata/tasks_running"

# Go through the feeder status cache. For each line:
# If the line indicate the task is COMPLETED, reset the status to WAITING, store the task ID in completed tasks
# If the line inicate the task is BUZY, go to the corresponding file for the pin, 
     # If the task is not there: reset the status to WAITING, store the task ID in completed tasks
     # If the task is still there: do nothing.
# If the line indicate the pin in WAITING, do nothing.

# Go through each line of the schedule TODO cache,
# 1. If a task have pasts its EXPIRE_TIME, then delete the task from file
# 2. If a task have an ID that was indicated completed, reduce one count from its REPEAT_X_TIMES
# 3. If a task have a REPEAT_X_TIMES smaller than 1, then delete the task from file cache
# Then:
# 1. If a task did not met its activation requirement, skip the task
# 2. If a task met its activation requirement, execute the task.

# If reached the end of file, write the modified file cache to disk, terminate the controller and wait for next activation

# Activation requirement include: 
# 1. It have passed EXECUTE_AFTER_UNIX_TIME
# 2. Feeder TARGET_FEEDER_NUMBER at TARGET_SITE_CODE is WAITING
# 3. IF_RECIEVE_FROM_ANTENNA_NUMBER and IF_RECIEVE_FROM_TAG_NUMBER had been satisfied

# Execution procedure:
# 1. Write into feeder status file cache that the target feeder is BUZY
# 2. Write task to feeder PIN TODO file (not cached)
# 3. Add INTERVAL_TIME to the task EXECUTE_AFTER_UNIX_TIME

# Files caches will be write in the following order:
# 1. Feeder status file,updating them to the new status
# 2. Schedule TODO file updating the status of tasks

# ----------------------------------------------------------------
# code:
import time

# Read lines from feeder status file, schedule TODO file, rfid status file and store them into caches (lists)
feederStatus = []
with open(feederStatusFileName) as f:
    for line in f:
        if not line.startswith('#'):
            feederStatus.append(line.strip())

scheduleTODO = []
with open(scheduleTODOFileName) as f:
    for line in f:
        if not line.startswith('#'):
            scheduleTODO.append(line.strip())

rfidStatus = []
with open(rfidStatusFileName) as f:
    for line in f:
        if not line.startswith('#'):
            ln = line.strip().split(",")
            if len(ln) == 4 and ln[0].isdigit():
                if int(time.time()) > int(ln[0]):
                    tag = (ln[1],ln[2],ln[3])
                    if tag not in rfidStatus:
                        rfidStatus.append(tag)
    

# Go through the feeder status cache. For each line:
# If the line indicate the task is COMPLETED, reset the status to WAITING, store the task ID in completed tasks
# If the line inicate the task is BUZY, go to the corresponding file for the pin, 
     # If the task is not there: reset the status to WAITING, store the task ID in completed tasks
     # If the task is still there: do nothing.
# If the line indicate the pin in WAITING, do nothing.

feeders = []
freeFeeders = []
newFeederStatus = []
completedTasks = []
try:
    for fs in feederStatus:
        fStatList = fs.split(",")
        # only accept the first line
        if (fStatList[0],fStatList[1]) not in feeders:
            if fStatList[3] == 'COMPLETE':
                completedTasks.append(fStatList[4])
                newFeederStatus.append([fStatList[0],fStatList[1],fStatList[2],'WAITING'])
                freeFeeders.append((fStatList[0],fStatList[1]))
            elif fStatList[3] == 'BUZY':
                with open(pinTODOFolderName + '/PIN' + fStatList[2] + ".todo") as f:
                    for line in f:
                        if not line.startswith('#'):
                            pinStatus = line.strip().split(",")
                            break
                # if there is a potentially legal line,
                if len(pinStatus) == 5:
                    # verify it is for this pin
                    if pinStatus[0] == fStatList[0] and pinStatus[1] == fStatList[1] and pinStatus[2] == fStatList[2]:
                        if not pinStatus[3] == fStatList[4]:
                            # The task is lost and there is a illegal task for a PIN now
                            # Clear both task and file.
                            completedTasks.append(fStatList[4])
                            completedTasks.append(pinStatus[3])
                            newFeederStatus.append([fStatList[0],fStatList[1],fStatList[2],'WAITING'])
                            freeFeeders.append((fStatList[0],fStatList[1]))
                            print("Illegal task "+pinStatus[3]+" found at PIN file, clearing...")
                            # clears pinfile
                            open(pinTODOFolderName + '/PIN' + fStatList[2] + ".todo", "w").close()
                            # do not modify the PIN as there is a legal task.
                        # if the uuid is the same, meaning pin is still doing its job, write it back
                        newFeederStatus.append(fStatList)
                    else:
                        # file is corrupt, clean it and then reset the status
                        print("Error! "+pinTODOFolderName + '/PIN' + fStatList[2] + ".todo contains feeder "+pinStatus[1]+" at "+pinStatus[0]+" to PIN #"+pinStatus[2])
                        print("Which it should contain feeder "+fStatList[1]+" at "+fStatList[0]+" to PIN #"+fStatList[2]+" !")
                        print("Reseting.....")
                        
                        newFeederStatus.append([fStatList[0],fStatList[1],fStatList[2],'WAITING'])
                        freeFeeders.append((fStatList[0],fStatList[1]))
                        # clears pinfile
                        open(pinTODOFolderName + '/PIN' + fStatList[2] + ".todo", "w").close()
                else:
                    # file is corrupt, clean it and then reset the status
                    print("Error! "+pinTODOFolderName + '/PIN' + fStatList[2] + ".todo is corrupt, clearing....")
                    newFeederStatus.append([fStatList[0],fStatList[1],fStatList[2],'WAITING'])
                    freeFeeders.append((fStatList[0],fStatList[1]))
                    # clears pinfile
                    open(pinTODOFolderName + '/PIN' + fStatList[2] + ".todo", "w").close()
            else:
                # This means it is probably waiting (by default)
                newFeederStatus.append([fStatList[0],fStatList[1],fStatList[2],'WAITING'])
                freeFeeders.append((fStatList[0],fStatList[1]))
            feeders.append((fStatList[0],fStatList[1]))
except:
    print("Error interacting with feeder status file @ "+ feederStatusFileName + "!")
    print("Exiting abnormally!")
    exit()
            
newScheduleTODO = []
# Go through each line of the schedule TODO cache,
# 1. If a task have pasts its EXPIRE_TIME, then delete the task from file
# 2. If a task have an ID that was indicated completed, reduce one count from its REPEAT_X_TIMES
# 3. If a task have a REPEAT_X_TIMES smaller than 1, then delete the task from file cache
# Then:
# 1. If a task did not met its activation requirement, skip the task
# 2. If a task met its activation requirement, execute the task.


# Activation requirements: 
def needToActivate(todoList):
    # 1. It have not passed EXECUTE_AFTER_UNIX_TIME yet, do not activate
    if todoList[1] > int(time.time()):
        return False
    # 2. Feeder TARGET_FEEDER_NUMBER at TARGET_SITE_CODE is not WAITING (buzy), do not activate
    if (todoList[2],todoList[3]) not in freeFeeders and not todoList[3] == 'F0':
        return False
        
    # 3. IF_RECIEVE_FROM_ANTENNA_NUMBER and IF_RECIEVE_FROM_TAG_NUMBER had been satisfied
    # if not caring for antenna status
    if todoList[5] == 'A0' and todoList[6] == '0_0':
        return True
        
    for tag in rfidStatus:
        if todoList[5] == 'A0' or tag[1] == todoList[5]:
            if todoList[6] == '0_0' or tag[2] == todoList[6]:
                return True
    return False


try:
    for td in scheduleTODO :
        todoList = td.split(",")
        # if data is too short, skip this line and report it
        if len(todoList) < 4:
            print("Unexpected line in schedule.todo of: \""+td+"\", deleting and continuing...")
            continue
        # if time stamp is wrong, skip this line
        if not todoList[1].isdigit():
            print("Unexpected EXECUTE_AFTER_UNIX_TIME in schedule.todo from line \""+td+"\", deleting and continuing...")
            continue
        if len(todoList) < 5:
            todoList.append('1')
        if len(todoList) < 6:
            todoList.append('A0')
        if len(todoList) < 7:
            todoList.append('0_0')
        if len(todoList) < 8:
            todoList.append('3600')
        if len(todoList) < 9:
            todoList.append(str(int(todoList[1]) + 43200))
        if len(todoList) < 10:
            todoList.append('1')
        # if amount is wrong, skip this line
        if not todoList[4].isdigit():
            print("Unexpected amount in schedule.todo from line \""+td+"\", deleting and continuing...")
            continue
        # if INTERVAL_TIME is wrong, skip this line
        if not todoList[7].isdigit():
            print("Unexpected INTERVAL_TIME in schedule.todo from line \""+td+"\", deleting and continuing...")
            continue
        # if expire time is wrong, skip this line
        if not todoList[8].isdigit():
            print("Unexpected expire time in schedule.todo from line \""+td+"\", with a value of \""+todoList[8]+"\", deleting and continuing...")
            continue
        # if repeat x times is wrong, skip this line
        if not todoList[9].isdigit():
            print("Unexpected REPEAT_X_TIMES in schedule.todo from line \""+td+"\", deleting and continuing...")
            continue
        
        # Hopefully now we have a legal line (P.S. This is the second time I am writing this line as thonny crashed on me sigh)
        # digitize all the needed integer fields
        todoList[1] = int(todoList[1])
        todoList[4] = int(todoList[4])
        todoList[7] = int(todoList[7])
        todoList[8] = int(todoList[8])
        todoList[9] = int(todoList[9])
        
        # 1. If a task have pasts its EXPIRE_TIME, then delete the task from file
        if int(time.time()) > todoList[8]:
            #skipping this line
            continue
        
        # 2. If a task have an ID that was indicated completed, reduce one count from its REPEAT_X_TIMES
        if todoList[0] in completedTasks:
            todoList[9] = todoList[9] -1
        # 3. If a task have a REPEAT_X_TIMES smaller than 1, then delete the task from file cache
        if todoList[9] < 1:
            #skipping this line
            continue
        
        # Then:
        # 1. If a task did not met its activation requirement, skip the task
        # 2. If a task met its activation requirement, execute the task.
        
        if needToActivate(todoList):
            # Execution procedure:
            # 1. Write into feeder status file cache that the target feeder is BUZY
            # update feeders to be not free too.
            # 2. Write task to feeder PIN TODO file (not cached)
            # 3. Add INTERVAL_TIME to the task EXECUTE_AFTER_UNIX_TIME
            # deal with F0 first
            if todoList[3] == 'F0':
                # trigger all connected feeders
                freeFeeders.clear()
                for i in range(len(newFeederStatus)):
                    if newFeederStatus[i][3] == 'WAITING':
                        # update feeder status
                        newFeederStatus[i][3] = 'BUZY'
                        newFeederStatus[i].append(todoList[0])
                        # update pin todo file
                        with open(pinTODOFolderName + '/PIN' + newFeederStatus[i][2] + ".todo",'w') as f:
                            f.write(','.join([newFeederStatus[i][0],newFeederStatus[i][1],newFeederStatus[i][2],todoList[0],str(todoList[4])]))
                        # update interval time
                        todoList[1] = todoList[1] + todoList[7]
            else:
                # trigger only the specific feeder
                freeFeeders.remove((todoList[2],todoList[3]))
                for i in range(len(newFeederStatus)):
                    if newFeederStatus[i][3] == 'WAITING' and newFeederStatus[i][0] == todoList[2] and newFeederStatus[i][1] == todoList[3]:
                        # update feeder status
                        newFeederStatus[i][3] = 'BUZY'
                        newFeederStatus[i].append(todoList[0])
                        # update pin todo file
                        with open(pinTODOFolderName + '/PIN' + newFeederStatus[i][2] + ".todo",'w') as f:
                            f.write(','.join([newFeederStatus[i][0],newFeederStatus[i][1],newFeederStatus[i][2],todoList[0],str(todoList[4])]))
                        # update interval time
                        todoList[1] = todoList[1] + todoList[7]
                       
            
            
        # if a program reached this point in the loop means it either had been executed or skipped, thus,
        # write it to the new schedule todo file.
        # convert it back to string states
        todoList[1] = str(todoList[1])
        todoList[4] = str(todoList[4])
        todoList[7] = str(todoList[7])
        todoList[8] = str(todoList[8])
        todoList[9] = str(todoList[9])
        newScheduleTODO.append(todoList)
        
        
except:
    print("Error interacting with schedule todo file @ "+ scheduleTODOFileName + "!")
    print("Exiting abnormally!")
    exit()



# Files caches will be write in the following order:
# 1. Feeder status file,updating them to the new status
with open(feederStatusFileName,'w') as f:
    for fs in newFeederStatus:
        f.write(','.join(fs)+"\n")
    
# 2. Schedule TODO file updating the status of tasks
with open(scheduleTODOFileName,'w') as f:
    for fs in newScheduleTODO:
        f.write(','.join(fs)+"\n")


# If reached the end of file, write the modified file cache to disk, terminate the controller and wait for next activation

