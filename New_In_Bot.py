#!/usr/bin/env python
# coding: utf-8

# In[7]:

import Purelei_Shopify_Test
import pandas as pd
import pickle
import datetime
import shopify
from pathlib import Path
from datetime import datetime as dt



# In[63]:


class New_In_Bot:



    def get_all_products():

        page = shopify.Product.find(limit=250)
        all_products = []
        while page.has_next_page():
            all_products += page
            if page.has_next_page():
                page = page.next_page()
        all_products += page
        return all_products

    def kill_newin_of_specific_product(product_id):

        product = shopify.Product.find(product_id)
        productdf = pd.DataFrame.from_records([product.to_dict()])

        for row in productdf.iterrows():

            tags = row[1]['tags'].split(', ')
            if 'newin' in tags:
                tags.remove('newin')
            if 'neu' in tags:
                tags.remove('neu')
            tags = ', '.join(tags)

        product.tags = tags

        product.save()

        return "Tags newin and neu were deleted."


    def kill_newin_of_old_products():

        product_pickle = New_In_Bot.get_all_products()
        df = pd.DataFrame.from_records([s.to_dict() for s in product_pickle])

        #change type object to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])

        #kill timezone
        df['created_at']=df['created_at'].dt.tz_convert(None)

        # creating timedelta column showing the time a product is online
        now = datetime.datetime.today()

        one_month_ago = now - datetime.timedelta(days=30)

        df2 = df[(df['tags'].str.contains("newin|neu", na=False)) & (df['created_at'] < one_month_ago)]

        print(df2[['title','tags','created_at']])

        for row in df2.iterrows():

            id = row[1]['id']

            tags = row[1]['tags'].split(', ')
            if 'newin' in tags or 'neu' in tags:
                print(id)
                #New_In_Bot.kill_newin_of_specific_product(id)

        return "Done"

if __name__ == "__main__":
    Purelei_Shopify_Test.PureleiFunctions.change_store('test_purelei')
    print(New_In_Bot.kill_newin_of_old_products())





# In[10]:






# In[ ]:








# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




