
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        Users = [];
        Auctions = [];
        Bids_InAuction = [];
        Item_Category = [];
        
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            #Users relation data
            Seller = item['Seller'];
            Seller_UserID = Seller['UserID'];
            Seller_Rating = Seller['Rating'];
            Seller_Location = item['Location'];
            #Add " in Location
            if('"' in Seller_Location):
                Seller_Location = Seller_Location.split('"');
                Segement_Len = len(Seller_Location);
                Temp_Array = Seller_Location[0];
                for i in range(1,Segement_Len):
                    Temp_Array = Temp_Array+'""'+Seller_Location[i];
                Seller_Location = Temp_Array;
                        
            Seller_Country = item['Country'];
            Users.append((Seller_UserID,Seller_Rating,Seller_Location,Seller_Country));
            if(item['Number_of_Bids'] != '0'):
                #Bids relation data
                Bid_ItemID = item['ItemID'];
                
                Bids = item['Bids'];
                for Bid in Bids:
                    Bidder = Bid['Bid']['Bidder'];
                    Bidder_UserID = Bidder['UserID'];
                    Bidder_Rating = Bidder['Rating'];
                    if(Bidder.has_key('Location')):
                        Bidder_Location = Bidder['Location'];
                    else:
                        Bidder_Location = "Null";
                    if(Bidder.has_key('Country')):
                        Bidder_Country = Bidder['Country'];
                    else:
                        Bidder_Country = "Null";
                        
                    #Add " in Location
                    if('"' in Bidder_Location):
                        Bidder_Location = Bidder_Location.split('"');
                        Segement_Len = len(Bidder_Location);
                        Temp_Array = Bidder_Location[0];
                        for i in range(1,Segement_Len):
                            Temp_Array = Temp_Array+'""'+Bidder_Location[i];
                        Bidder_Location = Temp_Array;
                        
                    #Bids relation data    
                    Bids_BidderID = Bidder_UserID;
                    Bid_Time = transformDttm(Bid['Bid']['Time']);
                    Bid_Amount = transformDollar(Bid['Bid']['Amount']);
                    
                    Bids_InAuction.append((Bid_ItemID,Bids_BidderID,Bid_Time,Bid_Amount));
                    Users.append((Bidder_UserID,Bidder_Rating,Bidder_Location,Bidder_Country));
                    
            #Auctions relation data
            Auction_ItemID = item['ItemID'];
            Auction_Name = item['Name'];
            #Add " in Name
            if('"' in Auction_Name):
                Auction_Name = Auction_Name.split('"');
                Segement_Len = len(Auction_Name);
                Temp_Array = Auction_Name[0];
                for i in range(1,Segement_Len):
                    Temp_Array = Temp_Array+'""'+Auction_Name[i];
                Auction_Name = Temp_Array;
                
            Acution_StartTime = transformDttm(item['Started']);
            Auction_EndTime = transformDttm(item['Ends']);
            Auction_FirstBid = transformDollar(item['First_Bid']);
            if(item.has_key('Buy_Price')):
                Auction_BuyPrice = transformDollar(item['Buy_Price']);
            else:
                Auction_BuyPrice = "0.0";#which means no buy price
            Acution_NumOfBids = item['Number_of_Bids'];
            Acution_Currently = transformDollar(item['Currently']);
            
            Auction_Description = str(item['Description']);
            #Add " in Description
            if('"' in Auction_Description):
                Auction_Description = Auction_Description.split('"');
                Segement_Len = len(Auction_Description);
                Temp_Array = Auction_Description[0];
                for i in range(1,Segement_Len):
                    Temp_Array = Temp_Array+'""'+Auction_Description[i];
                Auction_Description = Temp_Array;
                
            Auction_SellerID = Seller_UserID;
            Auctions.append((Auction_SellerID,Auction_ItemID,Auction_Name,Acution_StartTime,Auction_EndTime
                            ,Auction_FirstBid,Auction_BuyPrice,Acution_NumOfBids,Acution_Currently
                            ,Auction_Description));
            
            Item_Category_Num = len(item['Category']);
            for i in range(0,Item_Category_Num):
                Item_Category_ItemID = Auction_ItemID;
                Item_Category_Category = item['Category'][i];
                Item_Category.append((Item_Category_ItemID,Item_Category_Category));
                
        Users=sorted(set(Users),key=Users.index);#Eliminate duplicates
        
        #Create file in case there doesn't exist this file
        UsersFile=open("Users.dat","a");
        UsersFile.close();
        
        UsersFile=open("Users.dat","r");
        Temp_Users = UsersFile.readlines();
        if(Temp_Users != ''):
            for Temp_User in Temp_Users:
                Temp_User = Temp_User[0:len(Temp_User)-1];
                Temp_User = Temp_User.split('|');
                Users.append((Temp_User[0][1:len(Temp_User[0])-1],Temp_User[1],
                              Temp_User[2][1:len(Temp_User[2])-1],Temp_User[3][1:len(Temp_User[3])-1]));
        UsersFile.close();
        Users=sorted(set(Users),key=Users.index);#Eliminate duplicates
        
        UsersFile=open("Users.dat","w");
        for user in Users:
            UsersFile.write('"'+user[0]+'"'+"|"+user[1]+"|"+'"'+user[2]+'"'+"|"+'"'+user[3]+'"'+"\n");
        UsersFile.close();    
        
        AuctionsFile=open("Auctions.dat","a");
        for Auction in Auctions:
            AuctionsFile.write('"'+Auction[0]+'"'+"|"+'"'+Auction[1]+'"'+"|"+'"'+Auction[2]+'"'+"|"+'"'
                               +Auction[3]+'"'+"|"+'"'+Auction[4]+'"'+"|"+Auction[5]
                               +"|"+Auction[6]+"|"+Auction[7]+"|"+Auction[8]
                               +"|"+'"'+Auction[9]+'"'+"\n");
        AuctionsFile.close();  
        
        Bids_InAuctionFile = open("Bids_InAuction.dat","a");
        for Bid in Bids_InAuction:
            Bids_InAuctionFile.write(Bid[0]+"|"+Bid[1]+"|"+Bid[2]+"|"+Bid[3]+"\n");
        Bids_InAuctionFile.close();  
        
        Item_Category=sorted(set(Item_Category),key=Item_Category.index);#Eliminate duplicates
        Item_CategoryFile=open("Item_Category.dat","a");
        for Category in Item_Category:
            Item_CategoryFile.write(Category[0]+"|"+Category[1]+"\n");
        Item_CategoryFile.close();  
                

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
