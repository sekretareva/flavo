from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import os

def buildPlot(ax1, ax2, ax3, method, file):
    ax = fig.add_subplot(ax1, ax2, ax3)
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.set_title(method , fontsize = 20)
    
    for strain, x, y in zip(strains, components['Component 1'], components['Component 2']):
        niche = niches.loc[niches['Strain']==strain]['Niche'].values[0]
        if niche == 'water':
            color = 'blue'
            sc1 = ax.scatter(x, y, c = color, label = color, alpha=0.5, s = 100)
        else:
            color = 'brown'
            sc2 = ax.scatter(x, y, c = color, label = color, alpha=0.5, s = 100)
        ax.annotate(strain, [x, y], fontsize=10)
    ax.legend([sc1, sc2],['Aquatic clade', 'Terrestial clade'])

folder = 'counted'        
files = os.listdir(folder+'/')
n = len(files)
fig = plt.figure(figsize=(12, 10))

for i, file in enumerate(files):
    genes_count = pd.read_csv(folder+'/'+file)
    
    genes_count = genes_count.loc[:, (genes_count != 0).any(axis=0)]
    niches = pd.read_csv('niches.csv')
    
    strains = genes_count[genes_count.columns[0]]
    features = genes_count.columns[1:]
    
    if len(features)>1:
    
        x = genes_count.loc[:, features].values
        x = StandardScaler().fit_transform(x)
    
        pca = PCA(n_components=2, random_state=0)
        components = pd.DataFrame(data = pca.fit_transform(x), columns = ['Component 1', 'Component 2'])
        buildPlot(2, 3, (i+1)*3-2, 'PCA', file)
        
        mds = MDS(random_state=0)
        components = pd.DataFrame(data = mds.fit_transform(x), columns = ['Component 1', 'Component 2'])
        buildPlot(2, 3, (i+1)*3-1, 'MDS', file)
        
        tsne = TSNE(random_state=0, perplexity=8)
        components = pd.DataFrame(data = tsne.fit_transform(x), columns = ['Component 1', 'Component 2'])
        buildPlot(2, 3, (i+1)*3, 'TSNE', file)