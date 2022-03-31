import pandas as pd
import os
import re

ranks = ['Category', 'System', 'Systems in Category']

folderFrom = 'classified'
folderTo = 'counted'
filenames = [filename.split('.')[0] for filename in os.listdir(folderFrom+'/')]

#загрузка и соединение категорезированных функций
ctg1 = pd.read_csv('rastClassification.csv')
ctg2 = pd.read_csv('kwClassification.csv')
ctg = pd.concat([ctg1,ctg2], ignore_index=True)

categories = []
systems = []

classification = {}
    
print("Выберите ранг:")
for rankN, rank in enumerate(ranks):
    print(rankN, rank)
    
rank = int(input())

print("Выберите параметры для анализа:")
if rank != 2:    
    rank = ranks[rank]
    for rankN, rankName in enumerate(ctg1.sort_values(rank, ascending=True)[rank].unique()):
        print(rankN, rankName)
        classification[str(rankN)] = rankName
    
    parameters = input().split(',')
    for parameter in parameters:
        if rank == ranks[0]:
            categories.append(classification[parameter.strip()])
        if rank == ranks[1]:
            systems.append(classification[parameter.strip()])
else:
    for categoryN, categoryName in enumerate(ctg1.sort_values(ranks[0])[ranks[0]].unique()):
        print('\n' + str(categoryN), categoryName)
        classification[str(categoryN)] = categoryName
        for systemN, systemName in enumerate(ctg1.loc[ctg[ranks[0]]==categoryName].sort_values(ranks[1])[ranks[1]].unique()):
            systemN = str(categoryN) + '.' + str(systemN)
            print(systemN, systemName)
            classification[systemN] = systemName
    
    parameters = input().split(',')
    for parameter in parameters:
        if '.' in parameter:
            systems.append(classification[parameter.strip()])
        else:
            if '+' in parameter:
                categoryNum = parameter.split('+')[0].strip()
                keys = [key for key in classification.keys() if re.match(r'^'+categoryNum+'[.]', key)]
                for key in keys:
                    systems.append(classification[key])
            else:
                categories.append(classification[parameter.strip()])
    
print('Анализируемые категории:')
print(categories)
print('Анализируемые системы:')
print(systems)

count = pd.DataFrame([], columns=categories+systems)
count.insert(0, 'Strain', filenames)
count.loc[:, 1:] = 0

for filename in filenames:
    #загрузка функций бактерии
    fl = pd.read_csv(folderFrom+'/'+filename + '.csv', sep=',')
          
    #подсчет количества строк по параметру
    for count_s in count.columns:
        if count_s in categories:
            param = ranks[0]
        else:
            param = ranks[1]
        for fl_i, fl_s in enumerate(fl[param]):
            if count_s.strip() in fl_s:
                index = count.loc[count['Strain']==filename].index
                count.loc[(index, count_s)] = count.iloc[index][count_s] + 1
                                     
# сохранение подсчетов
count.sort_values('Strain', ascending=True).to_csv(folderTo + '/current.csv', index=False)
