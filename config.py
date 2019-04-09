_user = 'USER' # TODO: Fill in the user name
_password = 'PASSWORD' # TODO: Fill in the password
_dbname = 'DATABASE_NAME' # TODO: Fill in the database name
_host_product = 'localhost'
_port='5432'
conn_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
              .format(dbname=_dbname, user=_user, host=_host_product, password=_password, port=_port)