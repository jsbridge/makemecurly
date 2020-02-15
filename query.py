import psycopg2
import pandas as pd
import numpy as np
import re
from glob import glob
import matplotlib.pyplot as plt
import collections
from collections import Counter

def query(predicted_class):

    db_name = 'curly_db'
    username = 'ubuntu'

    con = None
    con = psycopg2.connect(database = db_name, user = username, host='localhost')

    # Query the product database for products for the given class
    sql_query =""" 
    SELECT products_used FROM curly_hair_table WHERE class='%s'; 
    """   % predicted_class
    
    curly_sql = pd.read_sql_query(sql_query,con)
    
    products=[]
    for p in curly_sql['products_used']:
        temp = p.strip("[]")
        temp = temp.split("'")
        temp = temp[1::2]
        products.append(temp)
    
    full_list = []
    for p in products:
        full_list.extend(p)

    # Make the text looks nicer and do some cleanup of product names
    full_list = [f.replace('_', ' ') for f in full_list]
    full_list = [f.replace('  ', ' ') for f in full_list]
    full_list = [f.replace('-', ' ') for f in full_list]
    full_list = [f.replace('deva curl', 'devacurl') for f in full_list]
    full_list = [f.replace('sheamoisture', 'shea moisture') for f in full_list]

    full_list_tup = []
    for i in range(0,len(full_list),2):
        try:
            full_list_tup.append((full_list[i], full_list[i+1]))
        except IndexError:
            continue

    # Group products by type of product
    df = pd.DataFrame(full_list_tup, columns=['product', 'type'])
    df.groupby('type')['product'].apply(lambda x: x.mode().iat[0])

    types = ['shampoo', 'conditioner', 'leave in', 'gel', 'deep treatment',
             'protein', 'cream', 'serum', 'clarifying shampoo']
    prods=[]
    for t in types:
        prod = (df.groupby('type')['product'].apply(lambda x: x.mode().iat[0]))[t]
        prod = " ".join(p.capitalize() for p in prod.split(' '))
        if 'La' in prod:
           prod = prod.replace('La ', 'LA ')
        prods.append(prod)

    # Make amazon links to each product
    urls = []
    for p in prods:
        urls.append('https://www.amazon.com/s?k='+p.replace(' ', '+'))
                        
    return tuple(prods), tuple(urls)

