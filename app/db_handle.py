import sqlite3

DB_FILE = "database.db"

db = None
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

db.executescript("""
CREATE TABLE if not exists profile(user text, pw text, full_name text, contact text, college text, major text, bio text);
Insert into profile values(?,?,?,?,?,?,?), ('admin', 'password', 'Frist Lsat', 'stuycs.org', 'Stuyvesant HS', 'SoftDev', "Hello World!");
""")
# CREATE TABLE if not exists playlist(username text, song text, artist text, lyrics text);
# """)

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

# LOGIN METHODS ---------------------------------------------------------------------------

# Creates a new user
# Parameters: text user, pw, full_name, contact, college, major, bio
# Returns nothing
def create_user(user, pw, full_name, contact, college, major, bio):
    try:
        c=db_connect()
        c.execute("Insert into profile values(?,?,?,?,?,?,?)", (user, pw, full_name, contact, college, major, bio))
        c.close()
        db.commit()
        db.close()
        print('User has been successfully created')
    except:
        print('User has not been created successfully')

# Checks if a username exists in the profile table
# Parameters: text user
# Returns True if user exists, False if user does not exist
def check_user(user):
    c=db_connect()
    c.execute("Select user from profile where user = ?", (user,))
    try:
        c.fetchone()[0]==user
        c.close()
        db.close()
        return True
    except: #If c.fetchone does not have an entry, then we want to catch the error and return an exception
        c.close()
        db.close()
        return False

# Checks if a password given matches the password of the username given 
# Parameters: text user, text pw
# Returns True is password works, False if password does not match
def check_pass(user, pw):
    c=db_connect()
    c.execute('select * from profile where (user = ? AND pw = ?)', (user, pw))
    try:
        c.fetchone()[0]
        c.close()
        db.close()
        return True
    except:
        c.close()
        db.close()
        return False

# print("create_user test")
# create_user('rory','gilmore', 'Rory Gilmore', '8675309', 'Yale', 'English', 'insert bio here')
# print("check_user test - should be True")
# print(check_user('admin'))
# print(check_user('rory'))
# print("check_user test - should be False")
# print(check_user('u'))
# print("check_pass test - should be True")
# print(check_pass('admin','password'))
# print(check_pass('rory','gilmore'))
# print("check_pass test - should be False")
# print(check_pass('admin','psword'))
# print(check_pass('u','p')) # false b/c not an account

# Copy and paste format (and uncomment) to create users for db
# These commands are executed when db_handle is imported to __init__.py ??
# user = ""
# pw = ""
# full_name = ""
# contact = ""
# college = ""
# major = ""
# bio = ""
# create_user(user, pw, full_name, contact, college, major, bio)

# print("\nmaking users for db")

# user = "ts1989"
# pw = "password"
# full_name = "Taylor Swift"
# contact = "@taylorswift"
# college = "n/a"
# major = "n/a"
# bio = "speak now (taylor's version) july 7th "
# create_user(user, pw, full_name, contact, college, major, bio)

# print(check_user('ts1989')) # true
# print(check_pass('sldkjfsl', 'slkdfj')) # false (wrong user and pw)
# print(check_pass('ts1989', 'sasdf')) # false (wrong pw)
# print(check_pass('ts1989', 'password')) # true