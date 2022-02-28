from bs4 import BeautifulSoup
import re
import pandas as pd
import os

foldername = 'html'

filenames = os.listdir(foldername+'/')
 
try:
    ctg = pd.read_csv('categories.csv')
except IOError:
    ctg = pd.DataFrame([], columns=['Category','System', 'Subsystem', 'Function'])


for filename in filenames:
    with open(foldername+'/'+filename, "r") as f:
        
        contents = f.read()
     
        soup = BeautifulSoup(contents, 'lxml')
     
        count = 0
        for string in soup.find_all("div", attrs={"name":re.compile(r'^tree_level_0')}): 
            a = string.get_text().split('\n')
            head = a[0][0:a[0].find('(')]
            for i in range(1, len(a)):
                subheads = re.split('\(\d+\)',a[i])
                subheads = [element for element in subheads if element]
                for subhead in range(1, len(subheads)):
                    if subheads[subhead].strip() not in ctg['Subsystem'].unique():
                        ctg = ctg.append({'Category':head.strip(), 
                              'System':subheads[0].strip(), 
                              'Subsystem':subheads[subhead].strip(), 
                              'Function':''}, ignore_index=True)
                        count+=1
                if (len(subheads)==1):
                    if subheads[0].strip() not in ctg['System'].unique():
                        ctg = ctg.append({'Category':head.strip(), 
                              'System':subheads[0].strip(), 
                              'Subsystem':'none', 
                              'Function':''}, ignore_index=True)
                        count+=1
                        
                            
        print(str(count) + ' new subsystems from file ' + filename)
                            
ctg.to_csv('categories.csv', index=False)
                    
            
        
