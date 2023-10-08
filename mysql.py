# from flaskext.mysql import MySQL
# import mysql_configuration

# _MYSQL = MySQL()

# def init_mysql(app):
#     app.config['MYSQL_DATABASE_USER'] = mysql_configuration.MYSQL_DATABASE_USER
#     app.config['MYSQL_DATABASE_PASSWORD'] = mysql_configuration.MYSQL_DATABASE_PASSWORD
#     app.config['MYSQL_DATABASE_DB'] = mysql_configuration.MYSQL_DATABASE_DB
#     app.config['MYSQL_DATABASE_HOST'] = mysql_configuration.MYSQL_DATABASE_HOST
#     _MYSQL.init_app(app)

# def get_cursor():
#     return _MYSQL.get_db().cursor()

# def get_test_sql_data():
#     cursor = _MYSQL.get_db().cursor()
#     cursor.execute("SELECT AppName, AppID FROM TestTable")
#     result = cursor.fetchone()
#     return {
#         'AppName': result[0],
#         'AppID': result[1]
#     }