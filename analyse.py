import mysql.connector
import matplotlib.pyplot as plt
from numpy import corrcoef

cnx = mysql.connector.connect(user='root', password='travisDB45',
                              host='localhost',
                              database= 'travisDB')
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

def getFrequencyOfTeamSizes(cnx):
    query = """
        SELECT
            gh_team_size,
            COUNT(gh_team_size)
        FROM travistorrent_27_10_2016
        WHERE gh_team_size != 0
        GROUP BY gh_team_size
        """
    data = runQuery(cnx, query)

    totalNumberOfTeams = 0
    for entry in data:
        size, number = entry
        totalNumberOfTeams += (number * size)

    teamSizeToFrequency = {}

    for entry in data:
        size, number = entry
        teamSizeToFrequency.update({ size: (float(number)*float(size))/float(totalNumberOfTeams) })

    return teamSizeToFrequency


def compareFields(cnx, firstField, secondField):
    query = "SELECT " + firstField + ", " + secondField + " " + \
            "FROM travistorrent_27_10_2016 " + \
            "GROUP BY " + firstField

    data = runQuery(cnx, query)
    xs, rawY = extractVars(data)
    ys = map(float, rawY)

    print firstField, "vs", secondField

    corr(xs, ys)
    plot(xs, ys)

def team_avg_builds(cnx):
    # correlate team size with average number of builds
    builds_query = '''SELECT DISTINCT gh_project_name AS name, fail, total
                    FROM travistorrent_27_10_2016 
                    WHERE fail = (SELECT COUNT(*) 
                                FROM travistorrent_27_10_2016
                                WHERE gh_project_name = name AND tr_status = 'failed') 
                                AND
                        total = total = (SELECT COUNT(*)
                                FROM travistorrent_27_10_2016
                                WHERE tr_status != 'errored')
                    GROUP BY gh_project_name'''
    query_second = """SELECT COUNT(*) as total
                    FROM travistorrent_27_10_2016
                    WHERE tr_status != 'errored'
                    AND
                    gh_project_name = 'weppos/whois'"""
                   
    data = runQuery(cnx, query_second)
    team_sizes = []
    no_builds = []
    for row in data:
        print(row)                               
    pass
    
def team_builds(cnx):
    # team size v proportion of build fails
    # total num of builds
    builds_query = "SELECT DISTINCT gh_team_size, COUNT(tr_status) " + \
            "FROM travistorrent_27_10_2016 " + \
            "WHERE tr_status != 'errored' AND gh_team_size > 0 " + \
            "GROUP BY gh_team_size " + \
            "HAVING COUNT(tr_status) > 0 " + \
            "ORDER BY gh_team_size ASC "
            
    data = runQuery(cnx, builds_query)
    team_sizes_with_builds, total_builds = extractVars(data)
    total_builds = total_builds
    # total num of build fails, exclude those with no fails
    fail_query = "SELECT DISTINCT gh_team_size, COUNT(tr_status) " + \
            "FROM travistorrent_27_10_2016 " + \
            "WHERE tr_status = 'failed' and gh_team_size > 0 " + \
            "GROUP BY gh_team_size " + \
            "HAVING COUNT(tr_status) > 0 " + \
            "ORDER BY gh_team_size ASC "
    
    data = runQuery(cnx, fail_query)
    team_sizes_with_fails, build_fails = extractVars(data)
    proportions_of_fails = []
    no_sizes = len(team_sizes_with_fails)
    for k in range(0, no_sizes):
        size = team_sizes_with_fails[k]
        index = team_sizes_with_builds.index(size)
        num_fails = float(build_fails[k])
        num_builds = float(total_builds[index])
        proportions_of_fails.append(num_fails / num_builds)

    corr(team_sizes_with_fails, proportions_of_fails)
    # plot correlation graph
    plot(team_sizes_with_fails, proportions_of_fails) 
    pass
    
team_avg_builds(cnx)