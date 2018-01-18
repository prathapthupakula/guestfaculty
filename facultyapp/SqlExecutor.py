import urllib

import Logger
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy import text
import sys
import MbConfig
#import exceptions
from MySQLdb import connect

class SqlExecutor:

    def getConnectionString(self, driver, host, name, username, password):
        connection_string = None
        if driver.lower() == 'mysql':
            connection_string = driver + '+mysqlconnector://' + username + ':' + password + '@' + host + '/' + name
        if driver.lower() == 'mssql':
            connection_string = "DRIVER=" + driver + ";SERVER=" + host + ";DATABASE=" + name + ";UID=" + username + ";PWD=" + password
            connection_string = urllib.quote_plus(connection_string)
            connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
        if driver.lower()=='redshift':
            connection_string = driver + '+psycopg2://' + username + ':' + password + '@' + host + '/' + name
        return connection_string


    def execute(self, sql, data={}, commit=True):
        res = None
        if len(data) > 0:
            try:
                res = self.cnxn.execute(text(sql), data)
                if commit:
                    self.cnxn.execute('COMMIT')
            except (exc.DBAPIError, e):
                res = None
                self.Logger.error(e)
                if e.connection_invalidated:
                    res = None
        else:
            try:
                res = self.cnxn.execute(text(sql))
                if commit:
                    self.cnxn.execute('COMMIT')
            except (sqlalchemy.exc.OperationalError,e):
                self.Logger.error(e)
            except (sqlalchemy.exc.ProgrammingError,e):
                self.Logger.error(e)
            except (exc.DBAPIError, e):
                res = None
                self.Logger.error(sql)
                self.Logger.error(e)
                if e.connection_invalidated:
                    res = None
            except (exceptions.TypeError,e):
                self.Logger.error(e)
                self.cnxn = self.connectEngine()
                self.cnxn.autocommit = False
            except:
                self.Logger.error(sys.exc_info()[0])
                self.cnxn = self.connectEngine()
                self.cnxn.autocommit = False
                res = self.cnxn.execute(text(sql));
        return res


    def fetchRows(self, sql, data=[], fetchType='fetchone'):
        ret = None
        try:
            res = self.cnxn.execute(text(sql), data);
        except (sqlalchemy.exc.OperationalError, e):
            self.Logger.error(e)
            self.cnxn = self.connectEngine()
            self.cnxn.autocommit = False
            res = self.cnxn.execute(text(sql), data);
        except (sqlalchemy.exc.ProgrammingError, e):
            self.Logger.error(e)
        except (exc.DBAPIError, e):
            res = None
            self.Logger.error(sql)
            self.Logger.error(e)
            if e.connection_invalidated:
                res = None
        except:
            self.Logger.error(sys.exc_info()[0])
            self.cnxn = self.connectEngine()
            self.cnxn.autocommit = False
            res = self.cnxn.execute(text(sql), data);
        if res is not None:
            if (fetchType == 'fetchone'):
                ret = res.fetchone()
            if (fetchType == 'fetchall'):
                ret = res.fetchall()
        return ret

    def begin(self):
        try:
            self.cnxn.execute('SELECT 1')
        except (sqlalchemy.exc.OperationalError, e):
            self.Logger.error(e)
            self.cnxn = self.connectEngine()
            self.cnxn.autocommit = False

        trans = self.cnxn.begin()
        return trans;

    def fetchRowCount(self, sql, data=[], fetchType='fetchone'):
        ret = None
        try:
            res = self.cnxn.execute(text(sql), data);
        except (sqlalchemy.exc.OperationalError, e):
            self.Logger.error(e)
            self.cnxn = self.connectEngine()
            self.cnxn.autocommit = False
            res = self.cnxn.execute(text(sql), data);
        if res is not None:
            if (fetchType == 'fetchone'):
                ret = res.fetchone()
            if (fetchType == 'fetchall'):
                ret = res.fetchall
        if ret is not None:
            return len(ret)
        else:
            return ret
