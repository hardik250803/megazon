import pandas as pd
import os
from sklearn.cluster import KMeans


data_directory = '../CustomersDataset/'

if os.path.exists('../Model/purchase_df.csv'):
    purchase_df = pd.read_csv('../Model/purchase_df.csv', index_col=0)
else:
    purchase_data = []
    for filename in os.listdir(data_directory):
        if filename.endswith('.gz'):
            file_path = os.path.join(data_directory, filename)
            
            customer_data = pd.read_json(file_path, compression='gzip', lines=True)
            for _, row in customer_data.iterrows():
                customer_id = row['i']
                for purchase in row['b']:
                    for product in purchase['Products']:
                        purchase_data.append({
                            'CustomerID': customer_id,
                            'Product': product['n'],
                            'Price': product['p'],
                            'Color': product['c'],
                            'Size': product['s'],
                        })
    purchase_df = pd.DataFrame(purchase_data)
    purchase_df.to_csv('../Model/purchase_df.csv', index=True)

print(purchase_df)
encoded_features = pd.get_dummies(purchase_df, columns=['Product','Color','Size'], drop_first=True)
feature_matrix = encoded_features.groupby(['CustomerID']).sum().reset_index()

kmeans = KMeans(n_clusters=5,random_state=0)
kmeans.fit(feature_matrix.drop(columns=['CustomerID']))
feature_matrix['Cluster'] = kmeans.labels_

feature_matrix.to_csv('../Model/KMC.csv',index = True)