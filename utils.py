

import psycopg2
import settings
DB_CONNECTION_STRING = "dbname='iws' user='{user}' password='{password}'".format(password=settings.DB_PASSWORD, user=settings.DB_USER)


def runQuery(query, arg):
  dbConn = psycopg2.connect(DB_CONNECTION_STRING)
  dbCursor = dbConn.cursor()
  dbCursor.execute(query, arg)
  dbConn.commit()
  dbCursor.close()
  dbConn.close()


def fetchResults(query, arg):
  dbConn = psycopg2.connect(DB_CONNECTION_STRING)
  dbCursor = dbConn.cursor()
  dbCursor.execute(query, arg)
  result = dbCursor.fetchall()
  dbCursor.close()
  dbConn.close()
  return result


def fetchAllFeatureRequests():
  return fetchResults("""SELECT * FROM feature_requests""",())

def insertFeatureRequest(request_args):
  arg = lambda x : request_args.get(x)[0]
  columns = ['title', 'description', 'client', 'priority', 'target_date', 'ticket_url', 'product_area']
  runQuery("""INSERT INTO feature_requests ({target_columns}) 
                     VALUES ({vals});""".format(target_columns=','.join(columns),
                                                vals          =','.join('%s' for i in range(len(columns)))),
                       tuple(arg(col) for col in columns)
          )


