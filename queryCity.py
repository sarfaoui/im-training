import os,sys
import MySQLdb
import getpass

if len(sys.argv) < 2:
    print "No city name provided, exiting..."
    exit(0)

city = sys.argv[1]

# mysql error 1045 workaround
p = getpass.getpass()

env = os.getenv('SERVER_SOFTWARE')
if (env and env.startswith('Google App Engine/')):
    # Connecting from App Engine
    db = MySQLdb.connect(
                         unix_socket='/cloudsql/rare-basis-686:samir',
                         user='root')
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(
                         host='173.194.254.191',
                         port=3306,
                         user='dbread',
                         passwd=p,
                         db='world')

cursor = db.cursor()
cursor.execute('SELECT * FROM Cities \
               LEFT JOIN Regions \
               ON Cities.region_id = Regions.id \
               INNER JOIN Countries \
               ON Cities.country_id = Countries.id \
               WHERE Cities.name = "%s"'
               % city)
results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+'

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)








