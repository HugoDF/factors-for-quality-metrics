import mysql.connector
import matplotlib.pyplot as plt
from numpy import corrcoef

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database= 'travistorrent')
 
def plot(xs, ys):
    plt.plot(xs,ys)
    plt.show()
    
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
        GROUP BY gh_team_size
        """
    data = runQuery(cnx, query)
    
    totalNumberOfTeams = 0
    for entry in data:
        size, number = entry
        totalNumberOfTeams += number
        
    teamSizeToFrequency = {}
    
    for entry in data:
        size, number = entry
        teamSizeToFrequency.update({ size: float(number)/float(totalNumberOfTeams) })
    
    return teamSizeToFrequency

def getTeamSizeVsAvgTestsFail(cnx):
    query = """
        SELECT 
            gh_team_size,
            AVG(tr_tests_failed)
        FROM travistorrent_27_10_2016
        GROUP BY gh_team_size
        """
    data = runQuery(cnx, query)
    xs, ys = extractVars(data)
    print corrcoef(xs, ys)
    plot(xs, ys)
    # there is a strong correlation between team size and the proportion of test fails


def getTeamSizeVsAvgTests(cnx, weightedByTeamSizeFrequency = True):
    teamSizeToFrequency = getFrequencyOfTeamSizes(cnx)
    
    query = """
        SELECT 
            gh_team_size,
            AVG(gh_test_lines_per_kloc)
        FROM travistorrent_27_10_2016
        GROUP BY gh_team_size
        """

    data = runQuery(cnx, query)
    
    xs = []
    ys = []

    for entry in data:
        teamSize, testLines = entry
        weightedTestLines = testLines * teamSizeToFrequency.get(teamSize)
        xs.append(teamSize)
        if(weightedByTeamSizeFrequency):
            ys.append(weightedTestLines)
        else:
            ys.append(testLines)
    

    print corrcoef(xs, ys)
    plot(xs, ys)
    


# getColumns(cnx)
getTeamSizeVsAvgTestsFail(cnx)
# getTeamSizeVsAvgTests(cnx, True)