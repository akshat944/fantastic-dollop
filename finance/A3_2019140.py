from flask import Flask, render_template, request, redirect,url_for
import os
from datetime import datetime,timedelta,date,time
import numpy as np
from bokeh.models import Markup, ColumnarDataSource
from bokeh.plotting import figure, output_file, show
import time
from turbo_flask import Turbo
import pandas as pd
import random
from flask_sock import Sock
import sys
import threading
import csv



app = Flask(__name__)
sock = Sock(app)
turbo = Turbo(app)

picfolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picfolder 


llis = list()
hlis = list()
ulis = list()
rlis = list()
nlis = list()
plis = list()
vlis = list()
dlis = list()
username = 'Guest'

@app.route('/')
def home():

    del llis[:]
    del hlis[:]
    del ulis[:]
    del rlis[:]
    del nlis[:]
    del plis[:]
    del vlis[:]
    
    dlis = ['NTPC',
              'HDFCBANK',
              'INFY',
              'SHREECEM',
              'UPL',
              'TATASTEEL',
              'SUNPHARMA',
              'HDFC',
              'NESTLEIND',
              'HEROMOTOCO',
              'HINDUNILVR',
              'ICICIBANK',
              'TCS',
              'LT',
              'DRREDDY',
              'IOC',
              'BAJAJFINSV',
              'ADANIPORTS',
              'ITC',
              'BAJAJ-AUTO',
              'TATAMOTORS',
              'MARUTI',
              'ULTRACEMCO',
              'CIPLA',
              'RELIANCE',
              'BHARTIARTL',
              'EICHERMOT',
              'JSWSTEEL',
              'TITAN',
              'GAIL',
              'POWERGRID',
              'GRASIM',
              'BAJFINANCE',
              'HINDALCO',
              'WIPRO',
              'TECHM',
              'BPCL',
              'COALINDIA',
              'ZEEL',
              'VEDL',
              'MM',
              'SBIN',
              'BRITANNIA',
              'AXISBANK',
              'HCLTECH',
              'KOTAKBANK',
              'ASIANPAINT',
              'ONGC',
              'INDUSINDBK']

    logo = os.path.join(app.config['UPLOAD_FOLDER'],'IIITD_fin.png')
    mag = os.path.join(app.config['UPLOAD_FOLDER'],'mag.png')
    aaaa = os.path.join(app.config['UPLOAD_FOLDER'],'aaaa.png')

    cdate = date.today() - timedelta(weeks = 508)
    #pdate = date.today() - timedelta(weeks = 508,days=1)


    print(cdate)
    #print(pdate)

    ddp = 'archive\\'
    
    for i in range(6):
        rs = random.choice(dlis)
        rlis.append(rs)
    
    for i in range(25):
        rs = random.choice(dlis)
        nlis.append(rs)

    for x in dlis:
        df = pd.read_csv('archive\\' + str(x) + '.csv')
        for index, row in df.iterrows():
            if datetime.strptime(row["Date"], '%Y-%m-%d').date() == cdate:
                plis.append(row['Close'])
                vlis.append(row['Volume'])

    iter1={plis[i] : mnt for i,mnt in enumerate(dlis)} 
    iter2={vlis[i] : mnt for i,mnt in enumerate(dlis)} 

    low = {key: val for key, val in sorted(iter1.items(), key = lambda ele: ele[0])}
    high = {key: val for key, val in sorted(iter1.items(), key = lambda ele: ele[0], reverse = True)}
    low_v = {key: val for key, val in sorted(iter2.items(), key = lambda ele: ele[0])}
    high_v = {key: val for key, val in sorted(iter2.items(), key = lambda ele: ele[0], reverse = True)}

    k_l = list(low.keys())
    v_l = list(low.values())
    k_h = list(high.keys())
    v_h = list(high.values())

    k_ll = list(low_v.keys())
    v_ll = list(low_v.values())
    k_hh = list(high_v.keys())
    v_hh = list(high_v.values())

    for x in rlis:
        df = pd.read_csv('archive\\' + str(x) + '.csv')
        for index, row in df.iterrows():
            if datetime.strptime(row["Date"], '%Y-%m-%d').date() == cdate:
                hlis.append(row["High"])
                llis.append(row["Low"])
    
    return render_template("index.html", dlis = dlis,rlis= rlis, ln = int(len(rlis)),lnd = len(dlis), hlis = hlis, llis = llis , ulis=ulis,nlis=nlis,nlen = len(nlis),logo=logo,username=username,mag=mag,aaaa=aaaa,k_l=k_l,v_l=v_l,k_h=k_h,v_h=v_h,k_ll=k_ll,v_ll=v_ll,k_hh=k_hh,v_hh=v_hh)

@app.route('/dataset', methods=['POST', 'GET'])
def dataset():
    stock = request.form['stk']
    
    # assumes csv files of stocks are present in same folder as this file
    # templates folder must also be present in the same folder as this file
    file ='archive/'+ stock + '.csv'
    df = pd.read_csv(file)
    
    print(stock)

    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure, curdoc
    from bokeh.driving import count

    output_file("plot.html")
    # file to save the model
    # instantiating the figure object
    graph = figure(title="Bokeh Scatter Graph")

    # the points to be plotted
    x = df['Close']
    y = df['Open']
    size = 10
    
    # plotting the graph
    graph.scatter(x, y,size=size)
    script1, div1 = components(graph)
    cdn_js = CDN.js_files
    show(graph)
    
    return render_template("plot.html", script1=script1, div1=div1,cdn_js=cdn_js)

source = ColumnarDataSource({'x':[],'y':[]})
upda = 100
ro = 100

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'): 
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [round(random.uniform(hlis[_],llis[_]),2) for _ in range(6)]
        
    return {'load':load}

def update_load():
    with app.app_context():
        while True:
            time.sleep(30)
            turbo.push(turbo.replace(render_template('load0.html'), 'load'))
            turbo.push(turbo.replace(render_template('load1.html'), 'load1'))
            turbo.push(turbo.replace(render_template('load2.html'), 'load2'))
            turbo.push(turbo.replace(render_template('load3.html'), 'load3'))
            turbo.push(turbo.replace(render_template('load4.html'), 'load4'))
            turbo.push(turbo.replace(render_template('load5.html'), 'load5'))
            
    
if __name__ == '__main__':
    app.run(debug=True)