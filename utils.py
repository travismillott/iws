
import psycopg2
import settings
import cgi
import re


INSERT_COLUMNS = ['title', 'description', 'client', 'priority', 'target_date', 'ticket_url', 'product_area']
REQUIRED_COLUMNS = ['title', 'description', 'client', 'priority', 'target_date', 'product_area']
DISPLAYED_COLUMNS = INSERT_COLUMNS + ['created']
DB_CONNECTION_STRING = "dbname='iws' user='{user}' password='{password}'".format(password=settings.DB_PASSWORD, user=settings.DB_USER)

allArgsValid = lambda a_dict : all([a_dict[i] for i in a_dict])


def validateRequiredColumns(request_args):
  validatedArgs = {col:True for col in REQUIRED_COLUMNS}
  for col in REQUIRED_COLUMNS:
    if request_args.get(col)[0] == '':
      validatedArgs[col] = False
  if not re.search('\d{4}-\d{2}-\d{2}', request_args.get('target_date')[0]):
    validatedArgs['target_date'] = False
  return validatedArgs


def getDataRowsHTML(data):
  htmlData = ''
  for row in data:
    htmlData += '<tr>\n'
    for index, col in enumerate(DISPLAYED_COLUMNS):
      if not row[index] :
        htmlData += '<td></td>'
        continue
      if index==7:
        htmlData += '<td class="turnEpochIntoDate">{val}</td>'.format(val=cgi.escape(str(row[index])))
        continue
      htmlData += '<td>{val}</td>'.format(val=cgi.escape(str(row[index])))
    htmlData += '</tr>\n'
  return htmlData


def createFeatureRequestTable():
  data = fetchAllFeatureRequests()
  return '''

<div class="ui-bar ui-title ui-bar-a"> <h1>Feature Request</h1> </div> <div class="ui-body ui-body-a">
    <div style="width:30%"><a href="new_feature" data-ajax="false" data-role="button">New Feature Request</a></div>
    <table id="datatable" class="display" cellspacing="0" width="100%">
        <thead>
            <tr><th>{colNames}</th>
            </tr>
        </thead>
        <tfoot>
            <tr><th>{colNames}</th>
            </tr>
        </tfoot>
        <tbody>
          {data}
        </tbody>
    </table>
</div>
'''.format(colNames = "</th><th>".join([col.capitalize().replace('_',' ') for col in DISPLAYED_COLUMNS]),
           data=getDataRowsHTML(data))


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
  return fetchResults("""SELECT {cols}, extract(epoch from created) as created FROM feature_requests ORDER BY priority ASC, created DESC""".format(cols=','.join(DISPLAYED_COLUMNS[:-1])),())

def insertFeatureRequest(request_args):
  arg = lambda x : request_args.get(x)[0]
  runQuery("""INSERT INTO feature_requests ({target_columns}) 
                     VALUES ({vals});""".format(target_columns=','.join(INSERT_COLUMNS),
                                                vals          =','.join('%s' for i in range(len(INSERT_COLUMNS)))),
                       tuple(arg(col) for col in INSERT_COLUMNS)
          )


