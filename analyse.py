import mysql.connector
import matplotlib.pyplot as plt
from numpy import corrcoef

import json

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database= 'travistorrent')
plotEnabled = True
corrEnabled = True

def plot(xs, ys):
    if(plotEnabled):
        plt.plot(xs,ys)
        plt.show()

def corr(xs, ys):
    if(corrEnabled):
        print corrcoef(xs, ys)[0][1]

def extractVars(data):
    xs = []
    ys = []
    for entry in data:
        x, y = entry[:2]
        xs.append(x)
        ys.append(y)
    return xs, ys

def runQuery(cnx, query):
    cursor = cnx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def getColumns(cnx):
    query = "SHOW FIELDS FROM travistorrent_27_10_2016"
    data = runQuery(cnx, query)

    for entry in data:
        print entry[0]

def getProjectNameToTotalsMap(data):
    projectNameToTotalsMap = {}
    for (name, total) in data:
        projectNameToTotalsMap[name] = total

    return projectNameToTotalsMap

def getProjects(cnx, size):
    query = "SELECT gh_project_name, COUNT(*) as total  FROM travistorrent_27_10_2016 WHERE gh_team_size = " + str(size) + " GROUP BY gh_project_name"
    data = runQuery(cnx, query)
    projectNameToTotalsMap = getProjectNameToTotalsMap(data)

    query = "SELECT gh_project_name, COUNT(*) as fail FROM travistorrent_27_10_2016 WHERE gh_team_size = " + str(size) + " AND tr_status = 'failed' GROUP BY gh_project_name"
    data = runQuery(cnx, query)

    projects = []
    for (name, fails) in data:
        total = projectNameToTotalsMap.get(name)
        projects.append((name, total, fails))

    return projects

def getTeamSizeToTeamInfoMap(cnx, teamSizes):
    teamSizeToTeamInfo = {}
    for size in teamSizes:
        print size
        teamSizeToTeamInfo[size] = getProjects(cnx, size)
    return teamSizeToTeamInfo

def teamSizeToTeamsWithBuildInfo(cnx):
    query = """SELECT gh_team_size FROM travistorrent_27_10_2016 GROUP BY gh_team_size"""
    data = runQuery(cnx, query)

    teamSizes = map(lambda x : x[0], data)
    teamSizeToTeamInfo = getTeamSizeToTeamInfoMap(cnx, teamSizes)

    with open('./data/buildInfoForTeams.json', 'w') as outfile:
        json.dump(teamSizeToTeamInfo, outfile)

    print json.dumps(teamSizeToTeamInfo)

# teamSizeToTeamsWithBuildInfo(cnx)

def getVolumeOfTestForTeams(cnx, teamSizes):
    volumeOfTestForTeams = {}
    for size in teamSizes:
        print size
        query = """
            SELECT
                gh_project_name,
                AVG(gh_test_cases_per_kloc)
            FROM travistorrent_27_10_2016
            WHERE gh_team_size = """ + str(size) + """
            GROUP BY gh_project_name
        """
        data = runQuery(cnx, query)
        volumeOfTestForTeams[size] = data

    return volumeOfTestForTeams

def teamSizeToTeamsWithVolumeOfTest(cnx):
    query = """ SELECT gh_team_size FROM travistorrent_27_10_2016 GROUP BY gh_team_size"""
    data = runQuery(cnx, query)

    teamSizes = map(lambda x: x[0], data)
    teamSizeToTeamsWithVolumeOfTest = getVolumeOfTestForTeams(cnx, teamSizes)

    with open('./data/volumeOfTestForTeams.json', 'w') as outfile:
        json.dump(teamSizeToTeamsWithVolumeOfTest, outfile)

    print json.dumps(teamSizeToTeamsWithVolumeOfTest)


teamSizeToTeamsWithVolumeOfTest(cnx)
