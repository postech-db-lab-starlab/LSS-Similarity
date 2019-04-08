import psycopg2

user = 'kjhong'
password = 'kjhong'
host_product = 'localhost'
dbname = 'kjhong'
port='5432'
conn_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
            .format(dbname=dbname, user=user, host=host_product, password=password, port=port)
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

query = "select html from urls.urls_tb where id = 9577"
writeFile = open("9577.html", "w")
curs.execute(query)
result = curs.fetchall()[0][0]
print(type(result))
writeFile.write(result)


