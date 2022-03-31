from bs4 import BeautifulSoup
import re
import pandas as pd
import os

foldername = 'rastHtml'

filenames = os.listdir(foldername+'/')

name_pattern = r'([\w, ' ', \(, \)]+)\s\(\d+\)$'
 
try:
    classification = pd.read_csv('rastClassification.csv')
except IOError:
    classification = pd.DataFrame([], columns=['Category','System', 'Subsystem', 'Function'])


for filename in filenames:
    with open(foldername+'/'+filename, "r") as f:
        
        contents = f.read()
     
        html = BeautifulSoup(contents, 'lxml')
     
        count = 0
        for div_content in html.find_all("div", attrs={"name":re.compile(r'^tree_level_0')}): 
            ctg_hierarchy = div_content.get_text().split('\n')
            category_name = re.search(name_pattern, ctg_hierarchy[0]).groups()[0]
            for i in range(1, len(ctg_hierarchy)):
                stm_hierarchy = re.split('\s\(\d+\)',ctg_hierarchy[i])
                stm_hierarchy = [element.replace(u'\xa0', u'') for element in stm_hierarchy if element]
                system_name = stm_hierarchy[0]
                for subsystem in range(1, len(stm_hierarchy)):
                    if stm_hierarchy[subsystem].strip() not in classification['Subsystem'].unique():
                        classification = classification.append({'Category':category_name.strip(), 
                              'System':system_name.strip(), 
                              'Subsystem':stm_hierarchy[subsystem].strip(), 
                              'Function':''}, ignore_index=True)
                        count+=1
                    
                if (len(stm_hierarchy)==1):
                    if stm_hierarchy[0].strip() not in classification['System'].unique():
                        classification = classification.append({'Category':category_name.strip(), 
                              'System':stm_hierarchy[0].strip(), 
                              'Subsystem':'none', 
                              'Function':''}, ignore_index=True)
                        count+=1
                        
                            
        print(str(count) + ' new subsystems from file ' + filename)
     
not_none = classification.loc[classification['Subsystem'] != 'none']
indexes = []
    
for i, system, category in zip(classification.loc[classification['Subsystem'] == 'none'].index.values, 
                                classification.loc[classification['Subsystem'] == 'none']['System'], 
                                classification.loc[classification['Subsystem'] == 'none']['Category']):
    if system in not_none['System'].values:
        indexes.append(i)

classification = classification.drop(index = indexes)
                            
classification.to_csv('rastClassification.csv', index=False)
