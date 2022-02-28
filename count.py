import pandas as pd

param = 'Category'
filename = '913281'
foldername = 'rastFunctions'

def add_ctg(column, t_to, t_from, raw_to, raw_from):
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
ctg1 = pd.read_csv('categories.csv')
ctg2 = pd.read_csv('categoriesByKeywords.csv')
ctg = pd.concat([ctg1,ctg2], ignore_index=True)
#создание датафрейма для подсчет строк, отнесенных к категории/системе/подсистеме
count = pd.DataFrame([], columns=[param,'count'])
count.loc[:, param] = ctg[param].unique()
count.loc[:, 'count'] = 0
#загрузка функций бактерии
fl = pd.read_csv(foldername+'/'+filename + '.tsv', sep='\t')
fl.loc[:, "System"] = 'none'
fl.loc[:, "Category"] = 'none'

#сопоставление категории и системы подсистеме
for fl_i, fl_s in enumerate(fl['Subsystem']):
    if fl_s != '- none -':
        for ctg_i, ctg_s in enumerate(ctg1['Subsystem']):
            if ctg_s != '- none -':
                if ctg_s.rstrip().lower() in fl_s.lower() :
                    add_ctg('System', fl, ctg1, fl_i, ctg_i)
                    add_ctg('Category', fl, ctg1, fl_i, ctg_i)

#сопоставление категории, системы, подсистемы функции
for fl_i, fl_s in enumerate(fl['Function']):
    if fl_s != '- none -':
        for ctg_i, ctg_s in enumerate(ctg2['Function']):
            if ctg_s.rstrip().lower()  in fl_s.lower() :
                add_ctg('System', fl, ctg2, fl_i, ctg_i)
                add_ctg('Category', fl, ctg2, fl_i, ctg_i)
                add_ctg('Subsystem', fl, ctg2, fl_i, ctg_i)
                
#избавление от лишних строк и колонок
fl = fl.drop(['Feature ID', 'Type', 'Contig', 'Start', 'Stop', 'Frame', 'Strand', 'Length (bp)', 'NCBI GI', 'locus'], 1)
fl = fl.loc[fl['Function'] != 'hypothetical protein']
fl = fl.loc[fl['Function'] != 'repeat region']

#сохранение категоризированных функций
fl.to_csv(filename + '-ctg.csv', index=False)

#подсчет количества строк по параметру
for count_i, count_s in enumerate(count[param]): 
    for fl_i, fl_s in enumerate(fl[param]):
        if count_s.strip() in fl_s:
             count.loc[(count_i, 'count')] = count.iloc[count_i]['count']  + 1
             
#сохранение подсчетов
count.sort_values(param, ascending=True).to_csv(filename + '-count.csv', index=False)
