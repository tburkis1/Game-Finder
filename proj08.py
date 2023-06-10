#####################################################
#
#   Computer Poject #8
#
#   Menu options
#
#   Open File
#       Get file pointer of either games or discounts
#
#   Read File
#       Turn games or discounts into dictionaries
#       Each colomn correspondes to some info
#
#   In Year
#       Filter games by year
#
#   By Genre
#       Filter games by genre
#
#   By Dev
#       Filter by developer
#
#   By Dev Year
#       Filter by Developer and Year
#
#   By Genre No Discount
#       Filter games by genre with no discount
#
#   By Dev Discount
#       Filter games by devleoper with discount
#
#   Print Games
#       Make a string of games list
#
#   Main
#       Get input from user
#       Proceed with each option
#
#####################################################



import csv
from operator import itemgetter


MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
def open_file(s):
    '''Loop until valid inputs
    Open valid files with input name
    Either games or discount file
    Return file pointer'''
    while True:
        try:
            file_name = input('\nEnter {} file: '.format(s))
            fp = open(file_name, encoding='UTF-8')
            break
        except:
            print('\nNo Such file')
    return fp

def read_file(fp_games):
    '''Read csv file
    Skip header line
    Make dictionary with following format
    {name: [date, [developer], [genre], mode, price, overall_reviews, 
reviews, percent_positive, [support]]}'''
    reader = csv.reader(fp_games)
    next(reader,None)
    
    d = {}
    
    for line in reader:
        #Name
        name = line[0]
        
        d[name] = []
        
        #Date
        d[name].append(str(line[1]))
        
        #Developer(s)
        devs = line[2].split(";")
        d[name].append(devs)
    
        #Genre(s)
        genres = line[3].split(";")
        d[name].append(genres)
        
        #Modes
        mode = line[4].split(";").pop(0)
        if mode.lower() == "multi-player":
            mode = 0
        else:
            mode = 1
        d[name].append(int(mode))
        
        #Price
        s = ""
        for ch in line[5]:
            if ch != ",":
                s += ch
        
        price = 0.00
        try:
            price = float(s)
        except:
            pass
        #1 rupee = 0.012 dollars
        price = price * 0.012
        d[name].append(float(price))
        
        #Overall reviews
        d[name].append(line[6])
        
        #Number of Reviews
        d[name].append(int(line[7]))
        
        #Percent Reviews Positive
        d[name].append(int(line[8][:-1]))
        
        #Supports
        l = []
        
        if int(line[9]) == 1:
            l.append("win_support")
        if int(line[10]) == 1:
            l.append("mac_support")
        if int(line[11]) == 1:
            l.append("lin_support")
            
        d[name].append(l)
        
    return d
        
def read_discount(fp_discount):
    '''Read discount file
    Skip header line
    Make into dictionary with following format
    {Name: Discount}'''
    reader = csv.reader(fp_discount)
    next(reader,None)
    
    d = {}
    
    for line in reader:
        val = round(float(line[1]), 2)
        d[line[0]] = val
        
    return d
    
def in_year(master_D,year):
    '''Add games released in given year to list
    ]Return list'''
    l = []
    
    for key in master_D:
        if master_D[key][0][-4:] == str(year):
            l.append(key)
    
    l.sort()
    
    return l
    
    

def by_genre(master_D,genre):
    '''Add games with a given genre to a list
    Sort list
    Return list'''
    l = []
    final = []
    
    for key in master_D:
        if genre in master_D[key][2]:
            l.append((key, master_D[key][7]))
    
    l = sorted(l, key=itemgetter(1),reverse = True)
    
    for element in l:
        final.append(element[0])
        
    return final
    
def by_dev(master_D,developer): 
    '''Add games to a list with a given developer
    Sort list
    Return list'''
    l = []
    final = []
    
    for key in master_D:
        if developer in master_D[key][1]:
            l.append((key, master_D[key][0][-4:]))
    
    l = sorted(l, key=itemgetter(1),reverse = True)
    
    for element in l:
        final.append(element[0])
        
    return final

def per_discount(master_D,games,discount_D): 
    '''If game has a discount, calculate discount prices
    Add prices to a list and return'''
    
    l = []
    
    for game in games:
        if game in list(discount_D.keys()):
            price = master_D[game][4] * (1-discount_D[game]/100)
            l.append(round(price, 6))
        if game not in list(discount_D.keys()):
            l.append(round(master_D[game][4], 6))
  
    return l

def by_dev_year(master_D,discount_D,developer,year):
    '''Get games released in given year
    Filter again by developer
    Sort list by increasing prices
    Return list'''
    final = []
    d = {}
    
    by_devs = by_dev(master_D, developer)
    
    for game in by_devs:
        d[game] = master_D[game]
        
    by_year = in_year(d, year)
           
    lop = per_discount(d, by_year, discount_D)
    
    l = []
    
    for i in range(0,len(by_year)):
        l.append((by_year[i], lop[i]))
    
    l = sorted(l, key=itemgetter(1))
    
    for element in l:
        final.append(element[0])
    return final
          
def by_genre_no_disc(master_D,discount_D,genre):
    '''Filter games by a given genre
    Do not apply discount prices
    Sort by positive reviews
    Return list of games'''
    final = []
    
    games = by_genre(master_D, genre)
    
    l = []
    
    for game in games:
        if game not in discount_D:
            l.append(game)
            
    d = {}      
    for game in l:
        d[game] = master_D[game]
    
    lot = []
    for game in d:
        lot.append((game, d[game][4], d[game][7]))
        
    lot = sorted(lot, key=itemgetter(2), reverse=True)
    lot = sorted(lot, key=itemgetter(1))
    
    for game in lot:
        final.append(game[0])
        
    return final

def by_dev_with_disc(master_D,discount_D,developer):
    '''Filter games by developer
    Apply discounts if available
    Sort by release date
    Return list'''
    final = []
    
    games = by_dev(master_D, developer)
    
    l = []
    for game in games:
        if game in discount_D:
            l.append(game)
            
    d = {}
    for game in l:
        d[game] = master_D[game]
        
    lot = []
    
    for game in d:
        lot.append((game, d[game][4], int(d[game][0][-4:])))
    
    lot = sorted(lot, key=itemgetter(2), reverse=True)
    lot = sorted(lot, key=itemgetter(1))
             
    for game in lot:
        final.append(game[0])
        
    return final

def print_games(l):
    '''Add a space an comma after every game
    Remove final column
    Return string'''
    s = ""
    
    for game in l:
        s += game + ", "
    s = s[:-2]
    
    return s

def main():
    
    #Open games and discount file
    games_fp = open_file("games")
    discount_fp = open_file("discount")
    
    #Turn games and discounts into dictionaries
    games = read_file(games_fp)
    discounts = read_discount(discount_fp)
    
    #Loop until user quits
    while True:
        
        #Get option from user
        option = input(MENU)
        
        #If option = 7, quit program
        if option == "7":
            print("\nThank you.")
            break
        
        #Option 1
        elif option == "1":
            
            #Loop until given valid year
            while True:
                try:
                    year = int(input('\nWhich year: '))
                    break
                except:
                    print("\nPlease enter a valid year")
                    continue
            
            #Filter games by year
            l = in_year(games,year)
            
            #if empty list, nothing to print, restart
            if len(l) == 0:
                print("\nNothing to print")
                continue
            
            l.sort()
            
            #Print list of games b y criteria
            print("\nGames released in {}:".format(year))
            print(print_games(l))
        
        #Option 2
        elif option == "2":
            
            #Ask for dev
            dev = input('\nWhich developer: ')
            l = by_dev(games, dev)
            
            #if empty list, nothing to print, restart
            if len(l) == 0:
                print("\nNothing to print")
                continue
            
            #Print list of games b y criteria
            print("\nGames made by {}:".format(dev))
            print(print_games(l))
        
        #Option 3
        elif option == "3":
            
            #Ask for genre
            genre = input('\nWhich genre: ' )
            
            l = by_genre(games, genre)
            
            #if empty list, nothing to print, restart
            if len(l) == 0:
                print("\nNothing to print")
                continue
            
            #Print list of games b y criteria
            print("\nGames with {} genre:".format(genre))
            print(print_games(l))
        
        #Option 4
        elif option == "4":
            
            #Ask for dev
            dev = input('\nWhich developer: ')
            
            #Get valid year
            try:
                year = input('\nWhich year: ')
                year = int(year)
            except:
                print("\nPlease enter a valid year")
                continue
            
            l = by_dev_year(games, discounts, dev, year)
            
            #if empty list, nothing to print, restart
            if len(l) == 0:
                print("\nNothing to print")
                continue
            
            #Print list of games b y criteria
            print("\nGames made by {} and released in {}:".format(dev,year))
            print(print_games(l))
        elif option == "5":
            
            #Ask for genre
            genre = input('\nWhich genre: '  )
            
            l = by_genre_no_disc(games, discounts, genre)
            
            #if empty list, nothing to print, restart
            if len(l) == 0:
                print("\nNothing to print")
                continue
             
            #Print list of games b y criteria
            print("\nGames with {} genre and without a discount:"\
                   .format(genre))
            print(print_games(l))
            
        elif option == "6":
            dev = input('\nWhich developer: ')
            
            l = by_dev_with_disc(games, discounts, dev)
            
            #if empty list, nothing to print, restart
            if len(l) == 0:
                print("\nNothing to print")
                continue
            
            #Print list of games b y criteria
            print("\nGames made by {} which offer discount:".format(dev))
            print(print_games(l))
            
        #Get new input if invalid option
        else:
            print("\nInvalid option")
            continue
            

if __name__ == "__main__":
    main()
                                           
