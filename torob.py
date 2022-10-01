import json
import random
import pandas as pd
import requests
import os
import streamlit as st
import sqlite3

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


import streamlit.components.v1 as components  # Import Streamlit
pp = 'hello'
# # Render the h1 block, contained in a frame of size 200x200.
components.html(f"<html><body><h1 class='h21ty'>{pp}</h1></body></html>", width=200, height=200)



# with open("hello.html") as html:
#     components.html(f'{html.read()}', width=200, height=200)


con = sqlite3.connect("prod.sqlite")
cur = con.cursor()

st.image('download.png')

inp = st.text_input('دنبال چه محصولی هستید ؟',
                    placeholder='نام محصول یا دسته بندی را وارد کنید و سپس Enter را فشار دهید',
                    help='نام محصول را وارد کنید و اینتر را بفشارید')
# myl = dict()
if inp != '':
    for i in range(1,10):
        requests.get(f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page={i}&size=100')


    # mypages = [f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=1&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=2&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=3&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=4&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=5&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=6&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=7&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=8&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=9&size=100',
    #            f'https://api.torob.com/v4/base-product/search/?category=&sort=popularity&q={inp}&page=10&size=100',
    #            ]
    for mp in mypages:
        url = requests.get(mp)
        x = url.json()
        for k in x['results']:
            nm = k['name1']
            pr = k['price_text']
            img = k['image_url']
            shp = k['shop_text']
            endz = 0
            cur.execute("insert into sqlite_master values(?,?,?,?,?)", (nm, pr, shp))
            con.commit()

df = pd.read_sql('SELECT * FROM Products ', con)

if df.empty:
    st.write('ابتدا یک محصول را جستجو کنید و منتظر بمانید')
else:
    st.dataframe(df)
    h = df.to_csv(sep=',')
    c = st.download_button(
        label="دانلود csv محصولات",
        data=h,
        file_name='tarfandoon.csv',
        mime='text/csv',
        key='dl'
    )

    if c:
        cur.execute("DELETE from Products ")
        con.commit()
        st.write('تمام دیتاها حذف شد ، برای دانلود مجددا یک محصول را جستجو کنید')
    st.error('Developed By Ali Jahani - Tafrandoon ')





