from datetime import datetime
from flask import request, make_response, redirect, url_for, render_template
from PRML import app
import pandas as pd
import random as rnd
import pickle
import gzip
import json

@app.route('/')
@app.route('/home')
def home():
    uid = request.cookies.get('uid')
    if(uid == None): newCust = True
    else: 
        uid = int(uid)
        newCust = False
        recom = recommend_from_cluster(uid,8)[['Product']].to_numpy()
        finalRecom = []
        for item in recom:
            finalRecom.append(item[0])
        udata = {
            'uid' : uid,
            'data' : get_history(uid),
            'Recommendations' : finalRecom
        }
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        newCust=newCust,
        udata = {} if newCust else udata
    )

@app.route('/profile')
def profile():
    uid = request.cookies.get('uid')
    if(uid == None):
        return render_template(
            'signin.html',
            title='SignIn Page',
            year=datetime.now().year
        )
    else:
        uid = int(uid)
        udata = {
            'uid' : uid,
            'data' : get_history(uid),
        }
        return render_template(
            'profile.html',
            title='Profile Page',
            year=datetime.now().year,
            udata = udata
        )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('uid')
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('uid',uid,60*60*24)
    return resp

@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('uid','',0)
    return resp

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


def get_color(data):
    if(data['Color'] == 'b'): return "Blue"
    elif(data['Color'] == 'r'): return "Red"
    elif(data['Color'] == 'g'): return "Green"
    elif(data['Color'] == 'y'): return "Yellow"
    elif(data['Color'] == 'w'): return "White"
    elif(data['Color'] == 'c'): return "Cyan"
    elif(data['Color'] == 'p'): return "Purple"
    
def get_size(data):
    if(data['Size'] == 'S'): return "Small"
    elif(data['Size'] == 'M'): return "Medium"
    elif(data['Size'] == 'L'): return "Large"
    elif(data['Size'] == 'XL'): return "XL"
    elif(data['Size'] == 'XXL'): return "XXL"
    
# with open('./PRML/static/Model/SVD_Model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)
#     print("Model loaded from file.")
    
purchase_df = pd.read_csv('./PRML/static/Model/purchase_df.csv', index_col=0)
feature_matrix = pd.read_csv('./PRML/static/Model/KMC.csv', index_col=0)

def recommend_from_cluster(customer_id, top_n=8):
    print(customer_id)
    if customer_id not in feature_matrix['CustomerID'].values:
        print("Customer ID not found in the dataset.")
        return None
    
    cluster_id = feature_matrix[feature_matrix['CustomerID'] == customer_id]['Cluster'].values[0]
    similar_customers = feature_matrix[feature_matrix['Cluster'] == cluster_id]['CustomerID']
    product_counts = purchase_df[purchase_df['CustomerID'].isin(similar_customers)].groupby('Product').size().reset_index(name='PurchaseCount')
    popular_products = product_counts.sort_values(by='PurchaseCount', ascending=False)
    already_purchased = purchase_df[purchase_df['CustomerID'] == customer_id]['Product'].tolist()
    recommendations = popular_products[~popular_products['Product'].isin(already_purchased)].head(top_n)

    return recommendations

def get_recommendations(customer_id, n_recommendations=8):
    print(customer_id)
    user_data = purchase_df[purchase_df['CustomerID'] == customer_id]
    if user_data.empty: 
        return get_recommendations(rnd.randint(1, 10000), 8)
    
    purchased_products = user_data['Product'].tolist()
    unique_products = purchase_df['Product'].unique()
    recommendations = []

    for product in unique_products:
        if product not in purchased_products:
            predicted_rating = model.predict(customer_id, product).est
            recommendations.append((product, predicted_rating))

    recommended_products = sorted(recommendations, key=lambda x: x[1], reverse=True)[:n_recommendations]

    recommended_attributes = []
    for product, rating in recommended_products:
        product_data = purchase_df[purchase_df['Product'] == product].iloc[0]
        recommended_attributes.append({
            'Product': product,
            'Recommended Price': product_data['Price'],
            'Predicted Rating': rating,
            'Recommended Color': get_color(product_data),
            'Recommended Size': get_size(product_data)
        })
    
    return recommended_attributes

def get_history(uid):
    with gzip.open(f'./PRML/static/CustomersDataset/c{uid}.json.gz', 'rt', encoding='utf-8') as file:
        dt = json.load(file)
        return dt
