import pandas as pd
import numpy as np
import os
import Diffusion_Maps.Importer as DMI
#import Diffusion_Maps.Algorithm as DMA
import Diffusion_Maps.AlgorithmNeigh2 as DMA
import Neighbours as Nbours
#Import outlines for output areas
polygons=pd.read_pickle('Mapping_Data.pkl')
#polygons = polygons[polygons['lad11cd'] == 'E06000023']
##Import metadata of the columns in the dataset
KS=pd.read_csv('CensusData/KS', names=['Data_Code','Type', 'Unit', 'Description'])
QS=pd.read_csv('CensusData/QS', names=['Data_Code','Type', 'Unit', 'Description'])
WP=pd.read_csv('CensusData/WP', names=['Data_Code','Type', 'Unit', 'Description'])

#Import first data file
filename=os.listdir('CensusData/data/')[0]

censusData=DMI.Import("".join(list('CensusData/data/'+filename)),selectedOAs=polygons['oa11cd'].values)

for filename in os.listdir('CensusData/data/')[1:]:
	#Import each data file
	newData=DMI.Import("".join(list('CensusData/data/'+filename)),selectedOAs=polygons['oa11cd'].values)
	if len(newData)==len(censusData):
		
		censusData=censusData.merge(newData,on='GeographyCode')

#Keep only raw counts of data

for i,header in enumerate(KS['Data_Code'].values):
	if KS['Type'].values[i] != 'Count':
		if header in list(censusData):
			censusData=censusData.drop(header,axis=1)
	if 'all' in KS['Description'].values[i].lower():
		if header in list(censusData):
			censusData=censusData.drop(header,axis=1)

for i,header in enumerate(QS['Data_Code'].values):
	if QS['Type'].values[i] != 'Count':
		if header in list(censusData):
			censusData=censusData.drop(header,axis=1)
	if 'all' in QS['Description'].values[i].lower():
		if header in list(censusData):
			censusData=censusData.drop(header,axis=1)

for i,header in enumerate(WP['Data_Code'].values):
	if WP['Type'].values[i] != 'Count':
		if header in list(censusData):
			censusData=censusData.drop(header,axis=1)
	if 'all' in WP['Description'].values[i].lower():
		if header in list(censusData):
			censusData=censusData.drop(header,axis=1)

#Make matrix only conataining data values
dataMatrix=np.asarray(censusData.as_matrix()[:,1:]).astype(float)
Neighbours = Nbours.Neighbours(polygons)
diffusion_Map_JE=DMA.Diffusion_Map(dataMatrix,10,Neighbours)
#diffusion_Map_test=DMA.Diffusion_Map(dataMatrix,10)

