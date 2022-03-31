import pandas as pd
import os

param = 'Category'

folderFrom = 'rastDownloads'
folderTo = 'classifiedRAST'
filenames = [filename.split('.')[0] for filename in os.listdir(folderFrom+'/')]

def addRank(column, t_to, t_from, raw_to, raw_from):
    if  'none' in t_to.iloc[raw_to][column]:
        t_to.loc[(raw_to,column)] = t_from.iloc[raw_from][column].strip()
    else:
        if t_to.iloc[raw_to][column]:
            column_array = t_to.iloc[raw_to][column].split(';')
            column_array = [j.strip() for j in column_array]
            if t_from.iloc[raw_from][column].strip() not in column_array:
                column_array.append(t_from.iloc[raw_from][column].strip())
                t_to.loc[(raw_to,column)] = '; '.join(sorted(column_array))

#загрузка и соединение категорезированных функций
rastClf = pd.read_csv('rastClassification.csv')
kwClf = pd.read_csv('kwClassification.csv')
ctg = pd.concat([rastClf,kwClf], ignore_index=True)


for filename in filenames:
    print(filename)
    #загрузка функций бактерии
    fl = pd.read_csv(folderFrom+'/'+filename + '.tsv', sep='\t')
    fl.loc[:, "System"] = 'none'
    fl.loc[:, "Category"] = 'none'
    
    temp = fl.loc[fl['Category'] == 'none']
    print('Unique functions: ' + str(len(temp['Function'].unique())))
    
    #сопоставление категории и системы подсистеме
    for n, subsystem in enumerate(fl['Subsystem']):
        if subsystem != '- none -':
            for rast_n, rastSubsystem in enumerate(rastClf['Subsystem']):
                if rastSubsystem != '- none -' and rastSubsystem != 'none':
                    if rastSubsystem.rstrip().lower() in subsystem.lower() :
                        addRank('System', fl, rastClf, n, rast_n)
                        addRank('Category', fl, rastClf, n, rast_n)
                        
    temp = fl.loc[fl['Category'] == 'none']
    print('Rest unique functions after rast classification: ' + str(len(temp['Function'].unique())))
    
    #сопоставление категории, системы, подсистемы функции
    for n, func in enumerate(fl['Function']):
        if func != '- none -':
            for kw_n, kwFunc in enumerate(kwClf['Function']):
                if kwFunc.rstrip().lower()  in func.lower() :
                    addRank('System', fl, kwClf, n, kw_n)
                    addRank('Category', fl, kwClf, n, kw_n)
                    addRank('Subsystem', fl, kwClf, n, kw_n)
                    
    temp = fl.loc[fl['Category'] == 'none']
    print('Rest unique functions after keywords classification: ' + str(len(temp['Function'].unique())) + '\n')
                    
    #избавление от лишних строк и колонок
    fl = fl.drop(['Feature ID', 'Type', 'Contig', 'Start', 'Stop', 'Frame', 'Strand', 'Length (bp)'], 1)
    fl = fl.loc[fl['Function'] != 'hypothetical protein']
    fl = fl.loc[fl['Function'] != 'repeat region']
    
    #сохранение категоризированных функций
    fl.to_csv(folderTo + '/' + filename + '.csv', index=False)
