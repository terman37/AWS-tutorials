# Imports
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# Create connection string
myuser = "admin"
mypwd = "123456789"
endpoint = "db.cvnmyj5p6kww.us-east-1.rds.amazonaws.com"
db_name = "MYDATABASE"
connection_string = "mysql+pymysql://" + myuser + ":" + mypwd + "@" + endpoint + ":3306/" + db_name

# Create an engine to <DB Name>
engine = create_engine(connection_string)

# Check if DB exists otherwise create it.
if not database_exists(engine.url):
    create_database(engine.url)
    print(db_name + " not existing, now created")
else:
    print(db_name + " connection OK")

# Get the table names
table_names = engine.table_names()
print("Existing table list:")
print(table_names)

connection = engine.connect()
while True:
    stmt = input("Enter your SELECT SQL query (q to quit): ")
    if stmt != "q":
        results = connection.execute(stmt).fetchall()
        print(results)
    else:
        break