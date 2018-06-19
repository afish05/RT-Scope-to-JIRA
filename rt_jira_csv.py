# rt_jira_csv.py
# Author: afisher
# This script will output the .csv for creating JIRA sub-tasks using the RM scope .csv as input 

import sys
import time
import os
import re
import csv

print('Welcome to the JIRA RT .csv script! \n\nPlease ensure your input file is located in the same directory as this script\n')

def main():

    cwd = os.getcwd() #Get the current directory, script will run on input from the same.
    hub = ''
    doc = ''
    rt_task = ''
    sch_dt = ''
    owner = ''
    filename = ''

    #Exit script function
    def die():
        os.system('pause')
        sys.exit()
	
    #Restart script function
    def restart():
        print('\nRestarting Script\n')
        time.sleep(2)
        main()

    #Get the inputs, do not allow blank inputs
    while hub == '':
        hub = input('Enter DC4 hub company name: ')

    while doc == '':        
        doc = input('Enter the EDI doc type: ')

    while rt_task == '':        
        rt_task = input('Enter the master RT ticket number: ')

    while sch_dt == '':
        sch_dt = input('Enter the scheduled install date (MM/DD/YYYY): ')
        while not re.match('(0[1-9]|1[0-2])/(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(20[0-9][0-9])',(sch_dt)):
            print('\n'+(sch_dt)+' is not a valid date. Please enter a valid date in MM/DD/YYYY format\n')
            sch_dt = input('Enter the scheduled install date (MM/DD/YYYY): ')

    while owner == '':    
        owner = input('Enter your email address: ')

    while filename == '':
        filename = input('Enter the file name (with file extension) to run: ')

    #Review and verify inputs
    print('\n\n'+(hub)+' - DC4 Company Name')
    print((doc)+' - DocType')
    print((rt_task)+' - RT-Task')
    print((sch_dt)+' - Scheduled Date')
    print((owner)+' - Owner')
    print((filename)+' - Filename')

    verify = input('\nIs the above information correct? (y/n): ')
    if verify == 'Y' or verify == 'y':
		
	#Format the input file name
        file = (cwd)+'\\'+(filename)
        
        #Open and read the input file, fail for common exceptions
        try:
            with open((file), 'r') as chkfile:
                chkfile.read()
        except FileNotFoundError:
            print('\nERROR - Input file '+(filename)+' not found in '+(cwd)+'\n')
            die()
        except UnicodeDecodeError:
            print('\nERROR - Invalid input file. Please ensure that the file is saved in .csv format\n')
            die()
        except Exception:
            print('\nAn unexpected error occured\n')
            die()

        try:
            #Create the output file and assign column headers
            with open((cwd)+'\JIRA_Import_'+(rt_task)+'.csv', 'w', newline='') as outfile:
                out_clmns = ['Type','Issue ID','Parent ID','Summary','Description','Scheduled','Account Name','RM Coordinator','Project Owner','Summary of Changes','TPID']
                csv_writer = csv.DictWriter(outfile, fieldnames=out_clmns, dialect='excel')
                csv_writer.writeheader()

                #Read the input file. Skip blank rows
                with open((file), 'r') as infile:
                    csv_reader = csv.DictReader((line for line in infile if not line.startswith(',')), dialect='excel')

                    #Build the output csv
                    for row in csv_reader:
                        co_name = (row['COMPANY_NAME'])
                        pr = ''
                        if '(PR)' in co_name:
                            co_name = co_name.replace(' (PR)','',).replace('(PR)','')
                            pr = ' (PR)'
                        else:
                            pass
                
                        tpid = (row[str(csv_reader.fieldnames[1])]) #Second column for TPID. Header differs.
                        csv_writer.writerow({'Type':'Sub-task',
                                        'Parent ID':(rt_task),
                                        'Summary':(co_name)+' / '+(hub)+' / '+(doc)+(pr),
                                        'Description':'See Summary of Changes',
                                        'Scheduled':(sch_dt),
                                        'Account Name':(co_name),
                                        'RM Coordinator':(owner),
                                        'Project Owner':(owner),
                                        'TPID':(tpid) or 'SALESFORCE'})

                    print('\nSUCCESS - Script created '+(outfile.name)+'.\n\nPlease check the accuracy of its contents before uploading to JIRA\n\n')
            die()
		
	#Report failures and do not create an output
        except Exception:
            os.remove(outfile.name)
            print('\nFAIL - An Error Occured when reading/writing the CSV. Please try again.\n')
            die()

    else:
        restart()

main()

