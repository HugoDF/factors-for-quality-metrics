import mysql.connector
import matplotlib.pyplot as plt
from numpy import corrcoef

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


# getColumns(cnx)
compareFields(cnx, "gh_team_size", "AVG(tr_tests_failed)")
compareFields(cnx, "gh_team_size", "AVG(tr_tests_failed) / COUNT(row)")
compareFields(cnx, "gh_team_size", "AVG(gh_test_churn)")
compareFields(cnx, "gh_num_pr_comments", "AVG(tr_tests_failed)")
compareFields(cnx, "gh_num_pr_comments", "AVG(gh_test_churn)")
compareFields(cnx, "gh_test_churn", "AVG(tr_tests_failed)")

compareFields(cnx, "gh_num_issue_comments", "AVG(gh_num_pr_comments)")
compareFields(cnx, "gh_num_pr_comments", "AVG(gh_num_issue_comments)")
compareFields(cnx, "gh_num_issue_comments", "AVG(gh_num_commit_comments)")
compareFields(cnx, "gh_num_commit_comments", "AVG(gh_num_pr_comments)")
