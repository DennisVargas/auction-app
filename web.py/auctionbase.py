#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import urlparse

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())


def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
                            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
                            extensions=extensions,)
    jinja_env.globals.update(globals)

    web.header('Content-Type', 'text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)


def clean_results(results):
    result_dict_list = list()
    for result in list(results):
        result_dict = {'Item_ID': result.Item_ID, 'Name': result.Name,
                       'Item_Description': result.Item_Description,
                       'High_Bid': result.High_Bid, 'Buy_Price': result.Buy_Price,
                       'Min_Bid': result.Min_Bid, 'Start_Time': result.Start_Time,
                       'End_Time': result.End_Time, 'Seller_ID': result.Seller_ID}
        result_dict_list.append(result_dict)
    return result_dict_list

def clean_bids(results):
    result_dict_list = list()
    for result in list(results):
        result_dict = {'Bidder_ID': result.Bidder_ID,
                       'Time': result.Time,
                       'Amount': result.Amount}
        result_dict_list.append(result_dict)
    return result_dict_list

#####################END HELPER METHODS#####################

# first parameter => URL, second parameter => class name
urls = (
  '/currtime', 'curr_time',
  '/selecttime', 'select_time',
  '/search', 'search',
  '/add_bid', 'add_bid',
  '/add_user', 'add_user',
  '/item_info', 'item_info',
)

class curr_time:
    # A simple GET request, to '/currtime'
    # Notice that we pass in `current_time' to our `render_template' call
    # in order to have its value displayed on the web page

    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time = current_time)


class select_time:
    # Another GET request, this time to the URL '/selecttime'
    def GET(self):
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests and GET requests

    def POST(self):
        post_params = web.input()

        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss']
        enter_name = post_params['entername']

        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)

        # save the selected time as the current time in the database
        sqlitedb.setTime(selected_time)

        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)


class search:
    # A GET request to the URL '/search'
    def GET(self):
        return render_template('search.html')

    # A POST request to the URL '/search'
    def POST(self):
        post_params = web.input()

        itemID = post_params['itemID']
        category = post_params['category']
        itemDescription = post_params['itemDescription']
        minPrice = post_params['minPrice']
        maxPrice = post_params['maxPrice']
        status = post_params['status']
        # currenttime = sqlitedb.getTime()
        if (itemID != '' or itemDescription != '' or category != '' or minPrice != '' or maxPrice != ''):
            results = sqlitedb.getItems(itemID, itemDescription, category, minPrice, maxPrice, status)

    # sqlitedb.getItems({'Item_ID' : itemID, 'Item_Description' : itemDescription }
    #                   minPrice = 'minPrice', maxPrice = 'maxPrice', status = 'status')


#     if (itemID != ''):
#       ID_result = sqlitedb.getItemById(itemID)
#       if ID_result == None:
#         return render_template('search.html',
#                                message='There are no items with that ID')
#
#     if (category != ''):
#       category_result = sqlitedb.getItemByCategory(category)
#       if category_result == None:
#         return render_template('search.html',
#                                message='There are no items with that category')
#
#     if (itemDescription != ''):
#       description_result = sqlitedb.getItemByDescription(itemDescription)
#       if description_result == None:
#         return render_template('search.html',
#                                message='There are no items with that description')
#
#     if (price != ''):
#       price_result = sqlitedb.getItemByPrice(price)
#       if price_result == None:
#         return render_template('search.html',
#                              message='There are no items with that price')
#
#     if (status != 'all'):
#       status_result = sqlitedb.getItemByStatus(status, current_time)
#       if status_result == None:
#         return render_template('search.html',
#                                message='There are no items with that status')

            if len(results) == 0:
                return render_template('search.html',
                                       add_result='There are no items that match that search')
            else:
                results_dict_list = clean_results(results)
               # return render_template('search.html',
               #                         add_result='Success! Your results are:\n' + str(results))
                return render_template('search.html', results=results_dict_list,
                                       add_result='Success! Your results are:\n' + str(results))
        else:
            return render_template('search.html')


class add_user:
    # A GET request to the URL '/add_user'
    def GET(self):
        return render_template('add_user.html')

    # A POST request to the URL '/add_user'
    def POST(self):
        post_params = web.input() #Control B here

        country = post_params['country']
        location = post_params['location']
        userID = post_params['userID']
        # current_time = sqlitedb.getTime()

        ### Many ways to fail... #######################################

        # (1) All fields must be filled
        if (country == '') or (location == '') or (userID == ''):
            return render_template('add_user.html',
                                   message='You must fill out every field')

        user_row = sqlitedb.getUserById(userID)

        # (4) UserID must correspond to an existing user in User table
        #item_row = sqlitedb.getItemById(userID);
        #if item_row == None:
        #  return render_template('add_user.html',
        #                         message='There are no items with that ID'
        #                         )


        ### ... but it's possible to succeed :P ########################

        # A bid at the buy_price closes the auction
    #    if (price >= item_row.buy_price):
          # Update ends to current_time
     #     sqlitedb.updateItemEndTime(itemID, current_time);
        if user_row is None:
            sqlitedb.addUser(country, location, userID)
            return render_template('add_user.html',
                                   message='Congratulations! You have joined!')

        # Should return error here!
        return render_template('add_user.html',
                               message='Error! You are already in the User list! ')


class add_bid:
    # A GET request to the URL '/add_bid'
    def GET(self):
        return render_template('add_bid.html')

    # A POST request to the URL '/add_bid'
    def POST(self):
        post_params = web.input()

        itemID = post_params['itemID']
        price = post_params['price']
        userID = post_params['userID']
        current_time = sqlitedb.getTime()

        ### Many ways to fail... #######################################

        # (1) All fields must be filled
        if (itemID == '') or (price == '') or (userID == ''):
            return render_template('add_bid.html',
                                   message='You must fill out every field')

        item_row = sqlitedb.getItemById(itemID)

        # (2) There must be an item with that ID
        if item_row == None:
            return render_template('add_bid.html',
                                   message='There are no items with that ID')

        # (3) Users can't bid on closed auction items
        if string_to_time(item_row.End_Time) <= string_to_time(current_time):
            return render_template('add_bid.html',
                                   message='That auction is already closed')

        # (4) UserID must correspond to an existing user in User table
        user_row = sqlitedb.getUserById(userID)
        if user_row is None:
            return render_template('add_bid.html',
                                   message='There are no users with that ID')

        # (5) Don't accept bids <= current highest bid
        if float(price) <= float(item_row.High_Bid):
            return render_template('add_bid.html',
                                   message='You must make a bid higher than the current price '
                                           '(currently $' + str(item_row.High_Bid) + ')')

        ### ... but it's possible to succeed :P ########################

        # A bid at the buy_price closes the auction
        if price >= item_row.Buy_Price and item_row.Buy_Price is not None:
            # Update ends to current_time
            sqlitedb.updateItemEndTime(itemID, current_time)
            return render_template('add_bid.html',
                                   message='Congratulations! You just closed that auction by '
                                           'making a bid at or above the buy price')

        # Add bid to Bid table in db
        sqlitedb.addBid(itemID, price, userID, current_time)

        return render_template('add_bid.html',
                               message='Success! You\'ve just placed a bid on '
                                       + item_row.Name + '(' + itemID + ')')


class item_info:
    # A GET request to the URL '/item_info'
    def GET(self):
        return render_template('item_info.html')

    # A POST request to the URL '/item_info'
    def POST(self):
        post_params = web.input()

        itemID = post_params['itemID']
        currenttime = sqlitedb.getTime()

        results = sqlitedb.getItems(itemID, '', '', '', '', 'all')
        bids = sqlitedb.getBidsByItemId(itemID)
        statusOC = ''
        end = sqlitedb.getEndTime(itemID)

        winnerID = sqlitedb.getWinnerId(itemID)

        if len(results) == 0:
            return render_template('item_info.html',
                                   add_result='There are no items that match that search')
        else:
            results_dict_list = clean_results(results)
            bids.reverse()
            bids_dict_list = clean_bids(bids)

            if currenttime >= end:
                statusOC = 'closed'
                return render_template('item_info.html', results=results_dict_list,
                                       bids=bids_dict_list, winner=winnerID, status=statusOC,
                                       add_result='Success! Your results are:\n' + str(bids_dict_list))
            else:
                statusOC = 'open'
                return render_template('item_info.html', results=results_dict_list,
                                   bids=bids_dict_list, status=statusOC,
                                   add_result='Success! Your results are:\n' + str(bids_dict_list))




###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()

