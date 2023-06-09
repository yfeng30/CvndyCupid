import sqlite3

DB_FILE = "data.db"

db = None
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

db.executescript("""
CREATE TABLE if not exists profile(pfp text, user text, pw text, full_name text, dob text, contact text, college text, major text, bio text);
Insert into profile values(?,?,?,?,?,?,?,?,?), ('temp pfp text', 'admin', 'password', 'Frist Lsat', '1/2/2005', 'stuycs.org', 'Stuyvesant HS', 'SoftDev', "Hello World!");
CREATE TABLE if not exists matches(p0 text, p1 text, status text);
Insert into matches values(?,?,?), ('admin', '', '');
""")

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

# HELPER METHODS ---------------------------------------------------------------------------
def print_profile():
    print("\nprofile table")
    rows = c.execute("select * from profile")
    for row in rows:
        print(row)

def print_matches():
    print("\nmatches table")
    rows = c.execute("select * from matches")
    for row in rows:
        print(row)

# LOGIN METHODS ---------------------------------------------------------------------------

# Creates a new user
# Parameters: text pfp, user, pw, full_name, dob, contact, college, major, bio
# Returns nothing
def create_user(pfp, user, pw, full_name, dob, contact, college, major, bio):
    try:
        c=db_connect()
        
        # print("\ntables before creating user")
        # print_profile()
        # print_matches()

        # get list of all unique users in p0 in profile
        c.execute("select user from profile")
        existing_users = c.fetchall() # array of tuples, each tuple = (p0,)
        # print("\nexisting_users:")
        # print(existing_users)
        unique_users = []
        # print("starting to go through all the users")
        for i in range(len(existing_users)): # going through array
            person = existing_users[i][0] # gets string from tuple
            # print(person)
            if person != None and person not in unique_users:
                unique_users.append(person)
        #         print(person + " added to unique_users")
        # print("\nunique users:")
        # print(unique_users)
        
        # updating matches table
        for existing_user in unique_users:
            # create a row in matches where p0 = user inputted to create_user() and p1 = an existing user
            c.execute("Insert into matches values(?,?,?)", (user, existing_user, 'unswiped'))
            # create a row in matches where p0 = an existing user and and p1 = user inputted to create_user()
            c.execute("Insert into matches values(?,?,?)", (existing_user, user, 'unswiped'))

        # add inputted user to profile table
        c.execute("Insert into profile values(?,?,?,?,?,?,?,?,?)", (pfp, user, pw, full_name, dob, contact, college, major, bio))

        c.close()
        db.commit()
        db.close()
        print('\nUser ' + user + ' has been successfully created')
    except:
        print('\nUser ' + user + ' has not been created successfully')

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

# TESTING LOGIN METHODS ---------------------------------------------------------------------------

# print("create_user test")
# create_user('rory pfp', 'rory','gilmore', 'Rory Gilmore', '02/02/2002', '8675309', 'Yale', 'English', 'insert bio here')
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

# SWIPE HELPER METHODS ---------------------------------------------------------------------------

# takes (logged in) user, another user, and a status
# returns true if status is p0's relationship with p1
# returns false otherwise (not the right status, not right users, etc.)
def check_relationship(p0, p1, status):
    c=db_connect()
    c.execute('select * from matches where (p0 = ? AND p1 = ? AND status = ?)', (p0, p1, status))
    try:
        c.fetchone()[0]
        c.close()
        db.close()
        return True
    except:
        c.close()
        db.close()
        return False

# print_profile()
# print_matches()
# print("")
# print(check_relationship('admin', 'rory', 'unswiped'))
# print(check_relationship('admin', 'rory', 'match'))
# print(check_relationship('not', 'existing', 'user'))

def update_relationship(p0, p1, status):
    c=db_connect()
    c.execute ('delete from matches where (p0 = ? AND p1 = ?)', (p0, p1))
    c.execute("Insert into matches values(?,?,?)", (p0, p1, status))
    c.close()
    db.commit()
    db.close()
    print("\n" + p0 + " relationship towards " + p1 + " updated to " + status)

# SWIPE METHODS ---------------------------------------------------------------------------

# p0 = user of person logged in 
# p1 = user of person p0 is swiping on
# returns nothing
def swipe_right(p0, p1):

    # if p1 has already matched with p0
    # shldn't happen b/c can't swipe on someone you already matched with
    if check_relationship(p1, p0, 'match'):
        update_relationship(p0, p1, 'match')

    # if p1 has already not matched with p0
    # shldn't happen b/c can't swipe on someone who said no to you
    elif check_relationship(p1, p0, 'not match'):
        update_relationship(p0, p1, 'not match')

    # if p1 has already said yes to p0
    elif check_relationship(p1, p0, 'potential'):
        update_relationship(p0, p1, 'match')
        update_relationship(p1, p0, 'match')

    # if p1 hasn't swiped on p0
    elif check_relationship(p1, p0, 'unswiped'):
        update_relationship(p0, p1, 'potential')

    print("\n" + p0 + " swipe right on " + p1 + " complete")

# create_user('rory pfp', 'rory','gilmore', 'Rory Gilmore', '02/02/2002', '8675309', 'Yale', 'English', 'insert bio here')
# print_matches()
# swipe_right('rory', 'admin')
# print_matches()

# p0 = user of person logged in 
# p1 = user of person p0 is swiping on
# returns nothing
def swipe_left(p0, p1):

    # if p1 has already matched with p0
    # shldn't happen b/c can't swipe on someone you already matched with
    if check_relationship(p1, p0, 'match'):
        update_relationship(p0, p1, 'not match')
        update_relationship(p1, p0, 'not match')

    # if p1 has already not matched with p0
    # shldn't happen b/c can't swipe on someone who said no to you
    elif check_relationship(p1, p0, 'not match'):
        update_relationship(p0, p1, 'not match')

    # if p1 has already said yes to p0
    elif check_relationship(p1, p0, 'potential'):
        update_relationship(p0, p1, 'not match')
        update_relationship(p1, p0, 'not match')

    # if p1 hasn't swiped on p0
    elif check_relationship(p1, p0, 'unswiped'):
        update_relationship(p0, p1, 'not match')
        update_relationship(p1, p0, 'not match')

    print("\n" + p0 + " swipe left on " + p1 + " complete")

# create_user('rory pfp', 'rory','gilmore', 'Rory Gilmore', '02/02/2002', '8675309', 'Yale', 'English', 'insert bio here')
# print_matches()
# swipe_left('rory', 'admin')
# print_matches()


# CREATING EXTRA USERS ---------------------------------------------------------------------------

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
