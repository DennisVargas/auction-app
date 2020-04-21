import web

db = web.database(dbn='sqlite', db='ebay_data.db')

######################BEGIN HELPER METHODS######################


# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey(): db.query('PRAGMA foreign_keys = ON')


# initiates a transaction on the database
def transaction(): return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#   sqlitedb.query('[FIRST QUERY STATEMENT]')
#   sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#   t.rollback()
#   print str(e)
# else:
#   t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples


# returns the current time from your database
def getTime():
    query_string = 'select Sys_Time from Time'
    results = query(query_string)
    return results[0].Sys_Time  # alternatively: return results[0]['time']

def getEndTime(itemID):
    query_string = 'select End_Time from Items where Item_ID = ' + itemID
    results = query(query_string)
    return results[0].End_Time


def setTime(new_time):
    t = db.transaction()
    try:
     db.update('Time', where="Sys_Time", Sys_Time = new_time)
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t.commit()


# returns a single item specified by the Item's Category in the database
def getItemByCategory(category):
    q = 'select * from Categories where Category = $Category'
    result = query(q, { 'Category': category })

    try:
        return result[0]
    except IndexError:
        return None


# returns a single item specif
# ied by the Item's ID in the database
def getItemById(itemID):
    q = 'select * from Items where Item_ID = $Item_ID'
    result = query(q, { 'Item_ID': itemID })

    try:
        return result[0]
    except IndexError:
        return None


# returns a single item specified by the Item's Description in the database
def getItemByDescription(itemDescription):
    q = 'select * from Items where Item_Description = $Item_Description'
    result = query(q, { 'Item_Description': itemDescription }) # TODO: needs to accept partial strings

    try:
        return result[0]
    except IndexError:
        return None


# returns a single item specified by the Item's Price in the database
def getItemByPrice(price):
    q = 'select * from Items where Buy_Price = $Buy_Price'
    result = query(q, { 'Buy_Price': price })

    try:
        return result[0]
    except IndexError:
        return None


# returns a single item specified by the Item's open/closed status in the database
def getItemByStatus(status, time):
    if status == open:
        q = 'select * from Items where (End_Time > $Time)'
        result = query(q, { 'Time': time })
    else:
        q = 'select * from Items where (End_Time < $Time)'
        result = query(q, { 'Time': time })

    try:
        return result[0]
    except IndexError:
        return None


def getBidsByItemId(itemID):
    q = 'select * from Bids where Item_ID = ' + itemID
    return query(q, {'Item_ID': itemID})


# returns a single item specified by the Item's ID in the database
def getUserById(user_id):
    q = 'select * from Users where User_ID = $User_ID'
    result = query(q, { 'User_ID': user_id })
    try:
        return result[0]
    except IndexError:
        return None


# def getItems(vars = {}, itemDescription = '', minPrice = '', maxPrice = '', status = 'all'):
def getItems(itemID = '', itemDescription='', category='', minPrice='', maxPrice='', status='all'):
    currTime = getTime()
    andFlag = 0
    # Create basic query that selects all items
    q = 'SELECT * FROM '
    ############# 'where ends > (select time from currenttime)'

    if (category == ''):
        q += 'Items'
    else:
        q += 'Items NATURAL JOIN Categories'

  # if (vars != {}) or (minPrice != '') or (maxPrice != '') or (status != 'all'):
    if (itemID != '') or (itemDescription != '') or (category != '') or (minPrice != '') or (maxPrice != '') or (status != 'all'):
        q += ' WHERE '

  # broke vars into individual checks
  # if vars != {}:
  #   q += web.db.sqlwhere(vars, grouping=' AND ')

    if itemID != '':
        q += 'Item_ID = '
        q += itemID
        andFlag = 1

    if itemDescription != '':
        if andFlag == 1:
            q += ' AND '
        q += 'Item_Description LIKE \'%'
        q += itemDescription
        q += '%\''
        andFlag = 1

    if category != '':
        if andFlag == 1:
            q += ' AND '
        q += 'Category LIKE \'%'
        q += category
        q += '%\''
        andFlag = 1

  # If min- and/or maxPrice are defined, append those restrictions to query
    if (minPrice != '') or (maxPrice != ''):
        # if vars != {}:                          q += ' AND '
        if andFlag == 1: q += ' AND '
        if minPrice != '':                    q += ' High_Bid >= ' + minPrice
        if minPrice != '' and maxPrice != '': q += ' AND '
        if maxPrice != '':                    q += ' High_Bid <= ' + maxPrice
        andFlag = 1

    if (status != 'all'):
        if andFlag == 1:
            q += ' AND '
        if status == 'open':
            # q += 'End_Time >= (select Sys_Time from Time) AND Start_Time <= (select Sys_Time from Time)'
            q += 'End_Time >= \'' + currTime + '\' AND Start_Time <= \'' + currTime + '\''
        if status == 'close':
            q += 'End_Time < \'' + currTime + '\''
        if status == 'notStarted':
            q += 'Start_Time > \'' + currTime + '\''

    # Return result of the query
    result = query(q)
    try:
        #return result[0]
        return result
    except IndexError:
        return None


def updateItemEndTime(itemID, new_end_time):
    db.update('Items',  where='Item_ID = ' + itemID,  End_Time=new_end_time)


def addBid(itemID, price, userID, current_time):
    t = db.transaction()
    try:
        db.insert('Bids', Item_ID=itemID, Amount=price, Bidder_ID=userID, Time=current_time)
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t.commit()

def addUser(country, location, userID):
    t = db.transaction()
    try:
        db.insert('Users', Country=country, Location=location, User_ID=userID, Rating=0)
    except Exception as e:
        t.rollback()
        print (str(e))
    else:
        t.commit()


def getWinnerId(itemID):
    q  = 'select Bidder_ID from Bids '
    q += 'where Item_ID = ' + itemID
    q += ' and amount = ('
    q += 'select max(Amount) from Bids '
    q += 'where Item_ID = ' + itemID
    q += ')'

    result = query(q)

    try:
        return result[0].Bidder_ID
    except IndexError:
        return None


# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################
