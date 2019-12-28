from pymongo import MongoClient
from requests.auth import HTTPBasicAuth
import requests
from pprint import pprint
import json
import urllib3
import jenkins
import time
from datetime import datetime


server = None
dbSrv = None
jenkinJson = None

def connect_to_jenkins():
    server = jenkins.Jenkins('http://localhost:8080', username='admin', password='admin')
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))
    return server

def connect_to_db():
    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    client = MongoClient('mongodb://localhost:27071')
    db=client.admin
    # Issue the serverStatus command and print the results
    serverStatusResult=db.command("serverStatus")
    pprint(serverStatusResult)
    return client

def get_json_jenkins_data():
    jenkinsJson = None
    url = 'http://192.168.0.14:8080' + '/api/json?tree=views[name,jobs[name,lastCompletedBuild[result,duration,timestamp],lastBuild[result,timestamp],lastSuccessfulBuild[duration],healthReport[description,score],inQueue,buildable,color]]'
    print(url)
    jobData =[]
    '''
    http = urllib3.PoolManager()
    #r = http.request('GET','http://192.168.0.14:8080/',auth=HTTPBasicAuth('admin', 'admin'))
    #print(r.status)
    r = requests.get('http://192.168.0.14:8080/',auth=('admin', 'admin'))
    print(r.status_code)
    print(r.content)
    '''
    s = requests.get(url,auth=('admin', 'admin'))
    print(s.status_code)
    print(s.content)
    dt = json.loads(s.content)
    jobs = dt['views'][0]
    print('No of jobs:',len(jobs))
    print(jobs.get('jobs'))
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
    print(jobData)
    #print(json.dumps(dt, indent = 4, sort_keys=True))
    
    return jenkinsJson

get_json_jenkins_data()

'''
out = '{"_class":"hudsonou.model.Hudson","views":[{"_class":"hudson.model.AllView","jobs":[{"_class":"hudson.model.FreeStyleProject","name":"Test","buildable":true,"color":"blue","healthReport":[{"description":"Build stability: No recent builds failed.","score":100}],"inQueue":false,"lastBuild":{"_class":"hudson.model.FreeStyleBuild","result":"SUCCESS","timestamp":1576724317379},"lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","duration":220,"result":"SUCCESS","timestamp":1576724317379},"lastSuccessfulBuild":{"_class":"hudson.model.FreeStyleBuild","duration":220}}],"name":"all"}]}';
newOut = '{"_'class":"hudson.model.Hudson","views":[{"_class":"hudson.model.AllView","jobs":[{"_class":"hudson.model.FreeStyleProject","na{"_class":"hudson.model.Hudson","views":[{"_class":"hudson.model.AllView","jobs":[{"_class":"hudson.model.FreeStyleProject","name":"Test","buildable":true,"color":"blue","healthReport":[{"description":"Build stability: No recent builds failed.","score":100}],"inQueue":false,"lastBuild":{"_class":"hudson.model.FreeStyleBuild","result":"SUCCESS","timestamp":1576900943604},"lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","duration":424,"result":"SUCCESS","timestamp":1576900943604},"lastSuccessfulBuild":{"_class":"hudson.model.FreeStyleBuild","duration":424}},{"_class":"hudson.model.FreeStyleProject","name":"TestOne","buildable":true,"color":"blue","healthReport":[{"description":"Build stability: No recent builds failed.","score":100}],"inQueue":false,"lastBuild":{"_class":"hudson.model.FreeStyleBuild","result":"SUCCESS","timestamp":1576901697590},"lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","duration":241,"result":"SUCCESS","timestamp":1576901697590},"lastSuccessfulBuild":{"_class":"hudson.model.FreeStyleBuild","duration":241}}],"name":"all"}]}me":"Test","buildable":true,"color":"blue","healthReport":[{"description":"Build stability: No recent builds failed.","score":100}],"inQueue":false,"lastBuild":{"_class":"hudson.model.FreeStyleBuild","result":"SUCCESS","timestamp":1576900943604},"lastCompletedBuild":{"_class":"hudson.model.FreeStyleBuild","duration":424,"result":"SUCCESS","timestamp":1576900943604},"lastSuccessfulBuild":{"_class":"hudson.model.FreeStyleBuild","duration":424}}],"name":"all"}]}'
dt = json.loads(out)
dtNew = json.loads(newOut)
jobs = dt['views'][0]

#print(json.dumps(dt, indent = 4, sort_keys=True))

for job in jobs.get('jobs')
    print(jobs.get('jobs')[0].get('name'))

server = connect_to_jenkins()
print('No of Jobs are:',server.jobs_count())

info = server.get_job_info('Test')
lb = info.get('lastBuild')
print(lb)

#print(info)
for key, value in info.items(): 
    print (key, value) 

for (k,v) in info:
    print('Key:',k)
    print('Value:',v)
'''
