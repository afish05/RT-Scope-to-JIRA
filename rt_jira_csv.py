# rt_jira_csv.py
# Author: afisher
# This script will output the .csv for creating JIRA sub-tasks using the RM scope .csv as input 

import csv

print('Welcome to the JIRA RT .csv script! \n\nPlease ensure your input is named "scope.csv" and the file is located in the same directory as this script\n')

hub = input('Enter DC4 hub company name: ')
doc = input('Enter the EDI doc type: ')
rt_task = input('Eneter the master RT ticket number: ')
sch_dt = input('Enter the scheduled install date (MM/DD/YYYY): ')
owner = input('Enter your email address: ')

infile = open('scope.csv', 'r') #Name your file 'scope.csv'
csv_reader = csv.DictReader(infile, dialect='excel')

outfile = open('JIRA_Import.csv', 'w', newline='')
out_clmns = ['Type','Issue ID','Parent ID','Summary','Description','Scheduled','Account Name','RM Coordinator','Project Owner','Summary of Changes','TPID']
csv_writer = csv.DictWriter(outfile, fieldnames=out_clmns, dialect='excel')
csv_writer.writeheader()

for row in csv_reader:
    co_name = (row['COMPANY_NAME'])
    tpid = (row['MAX(SP.TPID)'])
    csv_writer.writerow({'Type':'Sub-task',
                         'Parent ID':(rt_task),
                         'Summary':(co_name)+' / '+(hub)+' / '+(doc),
                         'Description':'See Summary of Changes',
                         'Scheduled':(sch_dt),
                         'Account Name':(co_name),
                         'RM Coordinator':(owner),
                         'Project Owner':(owner),
                         'TPID':(tpid) or 'SALESFORCE'})      

infile.close()
outfile.close()

print('\nDONE - Script created JIRA_Import.csv. Please check the accuracy of its contents before uploading to JIRA')
