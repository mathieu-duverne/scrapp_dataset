# Scrapp dataset on kaggle
I created this script to be able to retrieve the names and links of featured datasets on kaggle on my phone without having to go to kaggle only if necessary.
url : https://www.kaggle.com/datasets?topic=trendingDataset

## Informations send on notify server 
I notify the number of new datasets that have been added to the csv file plus the Link, Usuability columns. 

### Information keep on the csv file 
Title, About, Usuability, Link

### Librairie | dependencies
run `pip install -r requirements.txt`

### When u have all the dependencies
run `python get_kaggle_dataset.py`