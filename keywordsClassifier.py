import pandas as pd
import os
import re

foldername = 'rastDownloads'
filenames = os.listdir(foldername+'/')
file_contents = []
rastClf = pd.read_csv('rastClassification.csv')
flavo = None

def addRank(column, t_to, t_from, raw_to, raw_from):
    if  'none' in t_to.iloc[raw_to][column]:
        t_to.loc[(raw_to,column)] = t_from.iloc[raw_from][column]
    else:
        t_to.loc[(raw_to,column)] = t_to.iloc[raw_to][column] + '; ' + t_from.iloc[raw_from][column]
 
try:
    kwClf = pd.read_csv('kwClassification.csv')
except IOError:
    kwClf = pd.DataFrame([], columns=['Category','System', 'Subsystem', 'Function'])
    

for filename in filenames:
    print(filename)
    flavo = pd.read_csv(foldername+'/'+filename, sep='\t')
    flavo.loc[:, "System"] = 'none'
    flavo.loc[:, "Category"] = 'none'
    
    temp = flavo.loc[flavo['Category'] == 'none']
    print('Unique functions: ' + str(len(temp['Function'].unique())))
    
    #сопоставление категории и системы подсистеме
    for fl_i, fl_s in enumerate(flavo['Subsystem']):
        if fl_s != '- none -':
            for ctg_i, ctg_s in enumerate(rastClf['Subsystem']):
                if ctg_s != 'none':
                    if ctg_s.rstrip().lower() in fl_s.lower() :
                        addRank('System', flavo, rastClf, fl_i, ctg_i)
                        addRank('Category', flavo, rastClf, fl_i, ctg_i)
    
    flavo = flavo.loc[flavo['Function'] != 'hypothetical protein']
    flavo = flavo.loc[flavo['Function'] != 'repeat region']
    
    temp = flavo.loc[flavo['Category'] == 'none']
    print('Rest unique functions: '+ str(len(temp['Function'].unique())))
    
    count = 0
    for i, fl_s in enumerate(temp.sort_values('Function', ascending=True)['Function'].unique()):
        if fl_s not in kwClf['Function'].unique():
            
            if 'antibiotic' in fl_s.lower() and 'biosynthesis' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Secondary Metabolism', 
                                  'System':'Bacterial cytostatics, differentiation factors and antibiotics', 
                                  'Subsystem':'Antibiotics biosynthesis', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'dna polymerase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA replication', 
                                  'Subsystem':'DNA polymerase', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'methylase' in fl_s.lower() and 'rna' not in fl_s.lower() and ('dna' in fl_s.lower() or 'modification' in fl_s.lower()):
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA Metabolism - no subcategory', 
                                  'Subsystem':'DNA methylation', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if re.match(r'^T[1-6]SS', fl_s):
                romanNumbers = ['I', 'II', 'III', 'IV', 'V', 'VI']
                type = re.search(r'[1-6]', fl_s).group(0)
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Protein secretion system, Type ' + romanNumbers[int(type)-1], 
                                  'Subsystem':'T' + type + ' SS component', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
                
            
            if 'integrase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Phages, Prophages, Transposable elements, Plasmids', 
                                  'System':'Transposable elements', 
                                  'Subsystem':'Integrase', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            
            if 'transposon' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Phages, Prophages, Transposable elements, Plasmids', 
                                  'System':'Transposable elements', 
                                  'Subsystem':'Transposon', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'transposase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Phages, Prophages, Transposable elements, Plasmids', 
                                  'System':'Transposable elements', 
                                  'Subsystem':'Transposase', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'response regulator' in fl_s.lower() or 'histidine kinase' in fl_s.lower() or ('two-component' in fl_s.lower() and ('response' in fl_s.lower() or 'sensor' in fl_s.lower())):
                kwClf = kwClf.append({'Category':'Regulation and Cell signaling', 
                                  'System':'Regulation and Cell signaling - no subcategory', 
                                  'Subsystem':'Two-component regulatory system', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                if 'dna' in fl_s.lower() and ' binding' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'Transcription', 
                                  'Subsystem':'Two-component regulatory system', 
                                  'Function':fl_s}, ignore_index=True)
            
            if 'nuclease' in fl_s.lower():                
                if 'dna' in fl_s.lower() or 'deoxyribo' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                            'System':'DNA Metabolism - no subcategory', 
                                            'Subsystem':'Nuclease', 
                                            'Function':fl_s}, ignore_index=True)
                    count+=1
                if  ('rna' in fl_s.lower() or 'ribo' in fl_s.lower()) and 'deoxyribo' not in fl_s.lower():
                    kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                            'System':'RNA processing and modification', 
                                            'Subsystem':'Nuclease', 
                                            'Function':fl_s}, ignore_index=True)
                    count+=1
                if 'dna' not in fl_s.lower() and 'rna' not in fl_s.lower() and  'ribo' not in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                            'System':'DNA Metabolism - no subcategory', 
                                            'Subsystem':'Nuclease', 
                                            'Function':fl_s}, ignore_index=True)
                    kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                            'System':'RNA processing and modification', 
                                            'Subsystem':'Nuclease', 
                                            'Function':fl_s}, ignore_index=True)
                    count+=1
                
            if 'siderophore' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Membrane Transport - no subcategory', 
                                  'Subsystem':'Siderophore', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'rod shape' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Cell Wall and Capsule', 
                                  'System':'Cell Wall and Capsule - no subcategory', 
                                  'Subsystem':'Cell shape', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'protein translocase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Protein transport', 
                                  'Subsystem':'Protein transport', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'dipeptidase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Protein Metabolism', 
                                  'System':'Protein degradation', 
                                  'Subsystem':'Dipeptidases', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if ('protease' in fl_s.lower() or 'peptidase' in fl_s.lower()) and 'aminopeptidase' not in fl_s.lower() and 'dipeptidase' not in fl_s.lower() and 'synthase' not in fl_s.lower():
                kwClf = kwClf.append({'Category':'Protein Metabolism', 
                                  'System':'Protein degradation', 
                                  'Subsystem':'Protein degradation', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'sigma factor' in fl_s.lower():
                kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'Transcription', 
                                  'Subsystem':'Transcription initiation, bacterial sigma factors', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'rna' in fl_s.lower() and ('methyltransferase' in fl_s.lower() or 'mnm' in fl_s.lower() or 'methylase' in fl_s.lower()):
                kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'RNA methylation', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'rna' in fl_s.lower() and 'methylthiotransferase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'tRNA methylthiolation', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if ('polyribonucleotide' in fl_s.lower() or 'rna' in fl_s.lower()) and 'nucleotidyltransferase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'RNA processing and degradation, bacterial', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'rna' in fl_s.lower() and 'pseudouridine' in fl_s.lower():
                  kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                          'System':'RNA processing and modification', 
                                          'Subsystem':'Pseudouridinylation', 
                                          'Function':fl_s}, ignore_index=True)
                  count+=1
            
            if 'aminopeptidase' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Protein Metabolism', 
                                  'System':'Protein degradation', 
                                  'Subsystem':'Aminopeptidases', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'helicase' in fl_s.lower():
                if 'dna' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA Metabolism - no subcategory', 
                                  'Subsystem':'DNA helicase', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                if 'rna' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'RNA Metabolism - no subcategory', 
                                  'Subsystem':'RNA helicase', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'aerotolerance' in fl_s.lower() or 'BatA' in fl_s or 'BatB' in fl_s or 'BatC' in fl_s or 'BatD' in fl_s or 'BatE' in fl_s:
                kwClf = kwClf.append({'Category':'Stress Response', 
                                  'System':'Oxidative stress', 
                                  'Subsystem':'Aerotolerance', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'vgrg' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Protein secretion system, Type VI', 
                                  'Subsystem':'Actin cross-linking toxin', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'cell division' in fl_s.lower() and ('protein' in fl_s.lower() or 'trigger' in fl_s.lower()):
                kwClf = kwClf.append({'Category':'Cell Division and Cell Cycle', 
                                  'System':'Cell Division and Cell Cycle - no subcategory', 
                                  'Subsystem':'Cell division protein', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'restriction' in fl_s.lower() and ('modification' in fl_s.lower() or 'methylase' in fl_s.lower()):
                if 'type i ' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                      'System':'DNA Metabolism - no subcategory', 
                                      'Subsystem':'Type I Restriction-Modification', 
                                      'Function':fl_s}, ignore_index=True)
                    count+=1
                if 'type ii ' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                      'System':'DNA Metabolism - no subcategory', 
                                      'Subsystem':'Type II Restriction-Modification', 
                                      'Function':fl_s}, ignore_index=True)
                    count+=1
                if 'type iii ' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                      'System':'DNA Metabolism - no subcategory', 
                                      'Subsystem':'Type III Restriction-Modification', 
                                      'Function':fl_s}, ignore_index=True)
                    count+=1
                if 'type iv ' in fl_s.lower():
                    kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                      'System':'DNA Metabolism - no subcategory', 
                                      'Subsystem':'Type IV Restriction-Modification', 
                                      'Function':fl_s}, ignore_index=True)
                    count+=1
                    
            if 'restriction enzyme' in fl_s.lower() or 'restriction endonuclease' in fl_s.lower():
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA Metabolism - no subcategory', 
                                  'Subsystem':'Restriction Enzyme', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
                
            if 'cluster' in fl_s.lower() and 'iron' in fl_s.lower() and 'sulfur' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Miscellaneous', 
                                  'System':'Plant-Prokaryote DOE project', 
                                  'Subsystem':'Iron-sulfur cluster assembly', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'lipoprotein' in fl_s.lower() and 'releas' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'ABC transporters', 
                                  'Subsystem':'Lipoprotein-releasing system', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'lipopolysaccharide' in fl_s.lower() and 'synthesis' in fl_s.lower() and 'export' not in fl_s.lower() and 'capsular' not in fl_s.lower():
                kwClf = kwClf.append({'Category':'Cell Wall and Capsule', 
                                  'System':'Gram-Negative cell wall components', 
                                  'Subsystem':'Lipopolysaccharides', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'polysaccharide' in fl_s.lower() and 'synthesis' in fl_s.lower() and 'export' not in fl_s.lower() and 'capsular' not in fl_s.lower():
                kwClf = kwClf.append({'Category':'Carbohydrates', 
                                  'System':'Polysaccharides', 
                                  'Subsystem':'Polysaccharide biosynthesis', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'lpt' in fl_s.lower() and 'protein' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Cell Wall and Capsule', 
                                  'System':'Gram-Negative cell wall components', 
                                  'Subsystem':'Lipoprotein sorting system', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'capsular' in fl_s.lower() and 'polysaccharide' in fl_s.lower() and 'synthesis' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Cell Wall and Capsule', 
                                  'System':'Capsular and extracellular polysacchrides', 
                                  'Subsystem':'Capsular Polysaccharides Biosynthesis and Assembly', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'crisp' in fl_s.lower() and 'repeat' in fl_s.lower():
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'CRISPs', 
                                  'Subsystem':'CRISPRs', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'crisp' in fl_s.lower() and 'spacer' in fl_s.lower():
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'CRISPs', 
                                  'Subsystem':'Spacers', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'crisp' in fl_s.lower() and ('ramp' in fl_s.lower() or 'cas' in fl_s.lower()):
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'CRISPs', 
                                  'Subsystem':'CRISPR-associated proteins', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
            
            if 'transport' in fl_s.lower() and 'ABC' not in fl_s and ('antiport' not in fl_s.lower() or 'symport' not in fl_s.lower() or 'uniport' not in fl_s.lower()):
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Membrane Transport - no subcategory', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'ABC' not in fl_s and 'antiport' in fl_s.lower() or 'symport' in fl_s.lower() or 'uniport' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Uni- Sym- and Antiporters', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
                
            if 'resist' in fl_s.lower() and 'phage' not in fl_s.lower():
                kwClf = kwClf.append({'Category':'Virulence, Disease and Defense', 
                                  'System':'Resistance to antibiotics and toxic compounds', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
    
            if 'resist' in fl_s.lower() and 'phage' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Virulence, Disease and Defense', 
                                  'System':'Virulence, Disease and Defense - no subcategory', 
                                  'Subsystem':'Phage defence', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'cytochrome' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Respiration', 
                                  'System':'Respiration - no subcategory', 
                                  'Subsystem':'Cytochrome', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'heat' in fl_s.lower() and 'shock' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Stress Response', 
                                  'System':'Heat shock', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'cold' in fl_s.lower() and 'shock' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Stress Response', 
                                  'System':'Cold shock', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'cold' in fl_s.lower() and 'shock' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Stress Response', 
                                  'System':'Stress Response - no subcategory', 
                                  'Subsystem':'Phage shock', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'ABC' in fl_s and 'transport' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'ABC-transporters', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'tonB' in fl_s or 'TonB' in fl_s:
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Membrane Transport - no subcategory', 
                                  'Subsystem':'Ton and Tol transopt system', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'ribosomal protein' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Protein Metabolism', 
                                  'System':'Protein biosynthesis', 
                                  'Subsystem':'Ribosome LSU/SSU bacterial', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'dna' in fl_s.lower() and 'repair' in fl_s.lower():
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA repair', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'tRNA-' in fl_s and len(fl_s)<16:
                kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'transcription' in fl_s.lower() and 'regulator' in fl_s.lower():
                kwClf = kwClf.append({'Category':'RNA Metabolism', 
                                  'System':'RNA processing and modification', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'type' in fl_s.lower() and 'secretion' in fl_s.lower():
                kwClf = kwClf.append({'Category':'Membrane Transport', 
                                  'System':'Protein secretion system', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
        
            if 'topoisomerase' in fl_s.lower():
                  kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA replication', 
                                  'Subsystem':'DNA topoisomerases', 
                                  'Function':fl_s}, ignore_index=True)
                  count+=1
        
            if 'replication' in fl_s.lower():
                kwClf = kwClf.append({'Category':'DNA Metabolism', 
                                  'System':'DNA replication', 
                                  'Subsystem':'none', 
                                  'Function':fl_s}, ignore_index=True)
                count+=1
    print('Classified by keywords: ' + str(count) + '\n')
    
kwClf.to_csv('kwClassification.csv', index=False)
