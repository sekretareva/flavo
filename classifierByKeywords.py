import pandas as pd
import os

foldername = 'rastFunctions'
filenames = os.listdir(foldername+'/')
file_contents = []
ctg = pd.read_csv('categories.csv')
flavo = None

def add_ctg(column, t_to, t_from, raw_to, raw_from):
    if  'none' in t_to.iloc[raw_to][column]:
        t_to.loc[(raw_to,column)] = t_from.iloc[raw_from][column]
    else:
        t_to.loc[(raw_to,column)] = t_to.iloc[raw_to][column] + '; ' + t_from.iloc[raw_from][column]

def defineEnzyme(table, enzyme_name, table_to):
    for fl_i, fl_s in enumerate(table.sort_values('Function', ascending=True)['Function'].unique()):
        if enzyme_name in fl_s.lower():
            if fl_s not in table_to['Function'].unique():
                    table_to = table_to.append({'Category':'Enzymes', 
                                  'System':'Enzymes', 
                                  'Subsystem':enzyme_name, 
                                  'Function':fl_s}, ignore_index=True)
            else:
                exists = False
                for name in table_to.loc[table_to['Function'] == fl_s].Subsystem.unique():
                    if name == enzyme_name:
                        exists = True
                if not exists:
                        table_to = table_to.append({'Category':'Enzymes', 
                            'System':'Enzymes', 
                            'Subsystem':enzyme_name, 
                            'Function':fl_s}, ignore_index=True)
    return table_to
 
try:
    ctg_kw = pd.read_csv('categoriesWithKeywords.csv')
except IOError:
    ctg_kw = pd.DataFrame([], columns=['Category','System', 'Subsystem', 'Function'])
    

for filename in filenames:
    print(filename)
    flavo = pd.read_csv(foldername+'/'+filename, sep='\t')
    flavo.insert(0, 'Job', filename)
    flavo.loc[:, "System"] = 'none'
    flavo.loc[:, "Category"] = 'none'
    
    temp = flavo.loc[flavo['Category'] == 'none']
    print('Unique functions: ' + str(len(temp['Function'].unique())))
    
    #сопоставление категории и системы подсистеме
    for fl_i, fl_s in enumerate(flavo['Subsystem']):
        if fl_s != '- none -':
            for ctg_i, ctg_s in enumerate(ctg['Subsystem']):
                if ctg_s != 'none':
                    if ctg_s.rstrip().lower() in fl_s.lower() :
                        add_ctg('System', flavo, ctg, fl_i, ctg_i)
                        add_ctg('Category', flavo, ctg, fl_i, ctg_i)
    
    flavo = flavo.drop(['Feature ID', 'Type', 'Contig', 'Start', 'Stop', 'Frame', 'Strand', 'Length (bp)', 'NCBI GI', 'locus'], 1)
    flavo = flavo.loc[flavo['Function'] != 'hypothetical protein']
    flavo = flavo.loc[flavo['Function'] != 'repeat region']
    
    temp = flavo.loc[flavo['Category'] == 'none']
    print('Rest unique functions: '+ str(len(temp['Function'].unique())))
    
    enzymes = ['reductase', 'transferase', 'phosphorylase', 'hydrolase', 'aminase', 'kinase', 'ligase',
                'hydrogenase', 'synthase', 'xylase', 'halogenase', 'isomerase', 'phosphatase', 'nuclease'
                'hydratase', 'thiolase', 'aldolase', 'oxidase', 'esterase', 'mutase', 'cyclase', 
                'nucleotidase', 'atpase', 'permease', 'helicase', 'synthetase', 'acetylase', 'deacetylase', 
                'desuccinylase', 'succinylase', 'chelatase', 'deiminase', 'epimerase', 'lyase', 'amidase',
                'oxygenase', 'amylase', 'glucosidase', 'xylosidase', 'peptidase', 'lactamase', 'methylase',
                'helicase']
    enzymes_count = (len(ctg_kw))
    for enzyme in enzymes:
        ctg_kw = defineEnzyme(temp, enzyme, ctg_kw)
    enzymes_count =len(ctg_kw) - enzymes_count
    print('Classified as enzyme: ' + str(enzymes_count))
    
    count = 0
    for i, fl_s in enumerate(temp.sort_values('Function', ascending=True)['Function'].unique()):
        if fl_s not in ctg_kw['Function'].unique():
            
            if 'transport' in fl_s.lower() and 'ABC' not in fl_s and ('antiport' not in fl_s.lower() or 'symport' not in fl_s.lower() or 'uniport' not in fl_s.lower()):
                ctg_kw = ctg_kw.append({'Category':'Membrane Transport', 
                                  'System':'Membrane Transport - no subcategory', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'ABC' not in fl_s and 'antiport' in fl_s.lower() or 'symport' in fl_s.lower() or 'uniport' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Membrane Transport', 
                                  'System':'Uni- Sym- and Antiporters', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'resist' in fl_s.lower() and 'phage' not in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Virulence, Disease and Defense', 
                                  'System':'Resistance to antibiotics and toxic compounds', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
    
            if 'resist' in fl_s.lower() and 'phage' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Virulence, Disease and Defense', 
                                  'System':'Virulence, Disease and Defense - no subcategory', 
                                  'Subsystem':'Phage defence', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'cytochrome' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Respiration', 
                                  'System':'Respiration - no subcategory', 
                                  'Subsystem':'Cytochrome', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'heat' in fl_s.lower() and 'shock' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Stress Response', 
                                  'System':'Heat shock', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'cold' in fl_s.lower() and 'shock' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Stress Response', 
                                  'System':'Cold shock', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'cold' in fl_s.lower() and 'shock' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Stress Response', 
                                  'System':'Stress Response - no subcategory', 
                                  'Subsystem':'Phage shock', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'ABC' in fl_s and 'transport' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Membrane Transport', 
                                  'System':'ABC-transporters', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'tonB' in fl_s or 'TonB' in fl_s:
                ctg_kw = ctg_kw.append({'Category':'Membrane Transport', 
                                  'System':'Membrane Transport - no subcategory', 
                                  'Subsystem':'Ton and Tol transopt system', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'ribosomal protein' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Protein Metabolism', 
                                  'System':'Protein biosynthesis', 
                                  'Subsystem':'Ribosome LSU/SSU bacterial', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'dna' in fl_s.lower() and 'repair' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'DNA Metabolism', 
                                  'System':'DNA repair', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'tRNA-' in fl_s and len(fl_s)<16:
                ctg_kw = ctg_kw.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'transcription' in fl_s.lower() and 'regulator' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'type' in fl_s.lower() and 'secretion' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'Membrane Transport', 
                                  'System':'Protein secretion system', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'topoisomerase' in fl_s.lower():
                  ctg_kw = ctg_kw.append({'Category':'DNA Metabolism', 
                                  'System':'DNA replication', 
                                  'Subsystem':'DNA topoisomerases', 
                                  'Function':fl_s}, ignore_index=True)
                  count+=1
        
            if 'replication' in fl_s.lower():
                ctg_kw = ctg_kw.append({'Category':'DNA Metabolism', 
                                  'System':'DNA replication', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
    print('Classified by keywords: ' + str(count) + '\n')
    
    ctg_kw.to_csv('categoriesByKeywords.csv', index=False)