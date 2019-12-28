import datetime
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_table_experiments as dtable
import plotly
from random import random
from dash.dependencies import Input, Output
from requests.auth import HTTPBasicAuth
import json
import requests
import urllib3
import jenkins
import time
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def get_json_jenkins_data():
    jenkinsJson = None
    url = 'http://192.168.0.14:8080' + '/api/json?tree=views[name,jobs[name,lastCompletedBuild[result,duration,timestamp],lastBuild[result,timestamp],lastSuccessfulBuild[duration],healthReport[description,score],inQueue,buildable,color]]'
    #print(url)
    jobData =[]

    s = requests.get(url,auth=('admin', 'admin'))
    #print(s.status_code)
    #print(s.content)
    dt = json.loads(s.content)
    jobs = dt['views'][0]
    #print('No of jobs:',len(jobs))
    #print(jobs.get('jobs'))
    for job in jobs.get('jobs'):
        rowJ = {}
        name = job.get('name')
        rowJ['jobName'] = name
        status = job.get('lastBuild').get('result')
        rowJ['buildResult'] = status
        ti = job.get('lastBuild').get('timestamp')
        buildtime = datetime.fromtimestamp(ti/1000)
        rowJ['lastBuildTime'] = buildtime.ctime()
        #print( 'jobName:', name, 'buildResult:', status,'lastBuildTime:' ,buildtime)
        #print(rowJ)
        jobData.append(rowJ)
        rowJ = {}
    #print(jobData)
    #print(json.dumps(dt, indent = 4, sort_keys=True))
    
    return jobData

def get_job_data(res):
    if res:
        return res
    else:
        jobData = [
            {'jobName': 'Game of Thrones', 'buildResult': 'FAILED','lastBuildTime': 'Unknown'},
            {'jobName': 'Game of Thrones', 'buildResult': 'SUCCESS','lastBuildTime': 'Unknown'},
            {'jobName': 'Game of Thrones', 'buildResult': 'UNKNOWN','lastBuildTime': 'Unknown'}]
    return jobData
    
def get_job_table(res):
    if res:
        table = dt.DataTable(id='data-table', columns=[
        {'name': 'Job Name', 'id': 'jobName'},
        {'name': 'Last Build Result', 'id': 'buildResult'}, 
        {'name': 'Last Build Time', 'id': 'lastBuildTime'}], 
        data=get_job_data(res), editable=True,
        style_cell={'textAlign': 'center','min-width':'50px','backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_data_conditional=[
        {
            'if': {
                'column_id': 'buildResult',
                'filter_query': '{buildResult} eq "FAILURE"'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'buildResult',
                'filter_query': '{buildResult} eq "SUCCESS"'
            },
            'backgroundColor': 'green',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'buildResult',
                'filter_query': '{buildResult} eq "UNKNOWN"'
            },
            'backgroundColor': 'yellow',
            'color': 'black',
        }
        ]
        )
        return table
    else: return None
        
app.layout = html.Div([
    html.Div([
        html.H4('CI Dashboard Live updates'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
        ]),
    html.Div([
        html.Div(id='live-update-jobs'),
        dcc.Interval(
            id='interval-job-component',
            interval=3*1000, # in milliseconds
            n_intervals=0,
        )
    ]),
    html.Div([
        html.Div(id='live-update-more-jobs'),
        dt.DataTable(id='more-data-table', columns=[
        {'name': 'Job Name', 'id': 'jobName'},
        {'name': 'Last Build Result', 'id': 'buildResult'}, 
        {'name': 'Last Build Time', 'id': 'lastBuildTime'}],
        style_cell={'textAlign': 'center','min-width':'50px','leftMargin':'5px'})
    ]) 
    ])


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    #lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    tm = time.asctime( time.localtime(time.time()) )
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Local time in Chicago, Illinois::  ', style=style),
        html.Span(tm,style=style),
        
    ]
    
@app.callback(Output('live-update-jobs', 'children'),
              [Input('interval-job-component', 'n_intervals')])
def update_jobs(n):
    #lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    tm = time.asctime( time.localtime(time.time()) )
    #style = {'padding': '5px', 'fontSize': '16px'}
    jobData = [
            {'jobName': tm, 'buildResult': 'FAILED','lastBuildTime': 'Unknown'},
            {'jobName': tm, 'buildResult': 'SUCCESS','lastBuildTime': 'Unknown'},
            {'jobName': tm, 'buildResult': 'UNKNOWN','lastBuildTime': 'Unknown'}] 
        
    return get_job_table(get_json_jenkins_data())
   



 
if __name__ == '__main__':
    app.run_server(debug=True)