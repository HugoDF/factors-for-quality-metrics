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


# teamSizeToTeamsWithVolumeOfTest(cnx)

def getPrCommentsForTeams(cnx, teamSizes):
    prCommentsForTeams = {}
    for size in teamSizes:
        print size
        query = """
            SELECT
                gh_project_name,
                AVG(gh_num_pr_comments)
            FROM travistorrent_27_10_2016
            WHERE gh_team_size = """ + str(size) + """
            GROUP BY gh_project_name
        """
        data = runQuery(cnx, query)
        prCommentsForTeams[size] = map(lambda x: (x[0], float(x[1])), data)

    return prCommentsForTeams

def teamSizeToTeamsWithPrComments(cnx):
    query = """ SELECT gh_team_size FROM travistorrent_27_10_2016 GROUP BY gh_team_size"""
    data = runQuery(cnx, query)

    teamSizes = map(lambda x: x[0], data)
    prCommentsForTeams = getPrCommentsForTeams(cnx, teamSizes)

    with open('./data/prCommentsForTeams.json', 'w') as outfile:
        json.dump(prCommentsForTeams, outfile)

    print json.dumps(prCommentsForTeams)


# teamSizeToTeamsWithPrComments(cnx)

def getBuildResultsForPrComments(cnx, numPrComments):
    buildResultsForPrComments = {}
    for number in numPrComments:
        print number
        query = """
            SELECT
                gh_num_pr_comments,
                COUNT(*) as total
            FROM travistorrent_27_10_2016
            WHERE gh_num_pr_comments = """ + str(number) + """
            GROUP BY gh_num_pr_comments
        """;

        data = runQuery(cnx, query)

        if(len(data) > 0):
            _, total = data[0]
        else:
            total = 0

        query = """
            SELECT
                gh_num_pr_comments,
                COUNT(*) as fail
            FROM travistorrent_27_10_2016
            WHERE gh_num_pr_comments = """ + str(number) + """
                AND tr_status = 'failed'
            GROUP BY gh_num_pr_comments
        """;

        data = runQuery(cnx, query)

        if(len(data) > 0):
            _, fail = data[0]
        else:
            fail = 0

        print number, total, fail
        buildResultsForPrComments[number] = (number, total, fail)

    return buildResultsForPrComments


def prCommentsToBuildFailures(cnx):
    query = """ SELECT gh_num_pr_comments FROM travistorrent_27_10_2016 GROUP BY gh_num_pr_comments"""
    data = runQuery(cnx, query)

    numPrComments = map(lambda x : x[0], data)
    buildResultsForPrComments = getBuildResultsForPrComments(cnx, numPrComments)

    with open('./data/buildsForPrComments.json', 'w') as outfile:
        json.dump(buildResultsForPrComments, outfile)

    print json.dumps(buildResultsForPrComments)

# prCommentsToBuildFailures(cnx)

def getVolumeOfTestForNumPrComments(cnx, numPrComment):
    volumeOfTestForNumPrComments = {}
    for number in numPrComment:
        print number
        query = """
            SELECT
                AVG(gh_test_cases_per_kloc)
            FROM travistorrent_27_10_2016
            WHERE gh_num_pr_comments = """ + str(number) + """
            GROUP BY gh_num_pr_comments
        """
        data = runQuery(cnx, query)
        if(len(data)>0):
            volumeOfTestForNumPrComments[number] = data[0][0]
        else:
            volumeOfTestForNumPrComments[number] = 0

    return volumeOfTestForNumPrComments

def prCommentsToVolumeOfTest(cnx):
    query = """ SELECT gh_num_pr_comments FROM travistorrent_27_10_2016 GROUP BY gh_num_pr_comments"""
    data = runQuery(cnx, query)

    numPrComments = map(lambda x: x[0], data)
    numPrCommentsToVolumeOfTest = getVolumeOfTestForNumPrComments(cnx, numPrComments)

    with open('./data/volumeOfTestForPrComments.json', 'w') as outfile:
        json.dump(numPrCommentsToVolumeOfTest, outfile)

    print json.dumps(numPrCommentsToVolumeOfTest)


prCommentsToVolumeOfTest(cnx)
