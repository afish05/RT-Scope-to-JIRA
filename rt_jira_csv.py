# rt_jira_csv.py
# Author: afisher
# This script will output the .csv for creating JIRA sub-tasks using the RM scope .csv as input 

import sys
import os
import csv

cwd = os.getcwd() #Get the current directory, script will run on input from the same.
verify = 'N'

print('Welcome to the JIRA RT .csv script! \n\nPlease ensure your input file is located in the same directory as this script\n')

def main():
    
    hub = input('Enter DC4 hub company name: ')
    doc = input('Enter the EDI doc type: ')
    rt_task = input('Enter the master RT ticket number: ')
    sch_dt = input('Enter the scheduled install date (MM/DD/YYYY): ')
    owner = input('Enter your email address: ')
    filename = input('Enter the file name (with file extension) to run: ')

    #Exit script function
    def die():
        os.system("pause")
        sys.exit()
	
    #Restart script function
    def restart():
        print('\nRestarting Script\n')
        time.sleep(1)
        print('.')
        time.sleep(1)
        print('.')
        time.sleep(1)
        print('.\n')
        main()

    #Restart script for null inputs
    if hub == '' or doc == '' or rt_task == '' or sch_dt == '' or owner == '' or filename == '':
        print('\nInput Parameter missing.\n')
        restart()

	#User verify correct inputs
    verify = input('\nIs the above information correct? (Y/N): ')
    if verify == 'Y' or verify == 'y':
		
		#Format the input file name
        file = (cwd)+'\\'+(filename)
        
        #Open and read the input file
        try:
            with open((file), 'r') as chkfile:
                chkfile.read()

        #Fail for no file found
        except FileNotFoundError:
            print('\nERROR - Input file '+(filename)+' not found in '+(cwd)+'\n')
            die()

        #Fail non-text binary files
        except UnicodeDecodeError:
            print('\nERROR - Invalid input file. Please ensure that the file is saved in .csv format\n')
            die()

        #Fail other stuff
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
            print('\nFAIL - An Error Occured :(\n')
            die()

    else:
        restart()

if __name__ == "__main__":
    main()

