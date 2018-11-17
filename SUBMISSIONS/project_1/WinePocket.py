
# coding: utf-8

# In[ ]:

from tempfile import NamedTemporaryFile
import csv
import re
import sys
import shutil

class Utility():
    
    def __init__(self):
        # read existing user accounts from Users.csv
        user_list = []
        with open('Users.csv', 'r') as f:
            reader = csv.reader(f)
            next(f, None)
            for row in reader:
                user_list.append(User(row[0], row[1], row[2]))
            self.users = user_list
        
        # read existing wine library from winemag-data-130k-v2.csv
        wine_list = []
        with open('winemag-data-130k-v2.csv', 'r') as f:
            reader = csv.reader(f)
            next(f, None)
            for row in reader:
                wine_list.append(Wine(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[11], row[12], row[13]))
            self.wines = wine_list
        
        # read existing user-and-wine relation from user_wine.csv
        user_wine_list=[]
        with open('user_wine.csv', 'r') as f:
            reader = csv.reader(f)
            next(f, None)
            for row in reader:
                user_wine_list.append(row)
            self.user_wine = user_wine_list
    
    def check_email(self, email):
        """A function to validate the format of email address and check if it exists in system."""
        email_list = [user.email for user in self.users]
        try:
            if type(email) != str:
                raise Exception("Invalid email address. Please re-enter.")
            email = email.strip().lower()
            
            if email in email_list:
                raise Exception("Email already exists in system. Please try another one.")
            
            if len(email) > 7:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    return True
            else:
                raise Exception("Invalid format of email address. Please re-enter.") 
        
        except Exception as e:
            print("User input error: " + str(e))
            return False
        
    def check_username(self, username):
        """A function to check if the username already exists in system."""
        username_list = [user.username for user in self.users]
        if username in username_list:
            user_row = username_list.index(username)
            return user_row
        else:
            return -1
    
    def create_user(self):
        """Create a user account in Wine Pocket:
        (1) check the email, username
        (2) ask user to confirm password
        (3) add new user to self.users attribute, at the same time the new user is constructed as a User() object
        (4) add new user to Users.csv file
        """
        # check email
        email = input("Please enter your email address: ")
        while self.check_email(email) != True:
            email = input("Please enter your email address: ")

        # check username
        username = input("Please create your username for Wine Pocket: ")
        while self.check_username(username) != -1:
            print("Username already exists. Please try another one.")
            username = input("Please create your username for Wine Pocket: ")

        # check password
        fail_flag = True
        while fail_flag:
            password1 = input("Please create your password: ")
            password2 = input("Please confirm your password: ")
            if password1 != password2:
                print("Passwords do not match!")
            else:
                fail_flag = False
        self.users.append(User(username, password1, email))
        with open('Users.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([username, password1, email])
        print("User account successfully created! You may now log into Wine Pocket.")
        self.outapp_menu() # after account is created, user is navigated to login page to log in.
        
    def user_login(self):
        """A function to take in user's username and password to allow user log into Wine Pocket."""
        self.login_ind = False # an indicator to set if user logs in successfully or nots
        
        while self.login_ind == False:
            username = input("Please enter your Wine Pocket username: ")
            password = input("Please enter your password: ")
            user_row = self.check_username(username)
            if user_row != -1:
                if password == self.users[user_row].password:
                    self.login_ind = True
                    print("Log in successfully!")
                else:
                    print("Username and password do not match!")
            else:
                print("User doesn't exist!")
        self.inapp_menu(self.users[user_row]) # after user login, user will be navigated to home page.
    
    def user_logout(self):
        """A function to allow user log out of Wine Pocket."""
        self.login_ind = False
        print("Log out successfully!")
        print("=" * 20)
        self.outapp_menu() # after user logout, user will be navigated to login page.
    
    def inapp_menu(self, user): 
        """A function to present menu options to users while they are logged in"""
        fail = True
        print("\n" + "*" * 15 + " Wine Pocket Home Page " + "*" * 15 + "\n")
        print("=" * 50)
        print("1. View Top 20 wines")
        print("2. Search a wine")
        print("3. My wine")
        print("4. Log out")
        print("-" * 50)
        while fail:
            menu_select = input("Please select from the menu options: ")
            if menu_select == "1":
                fail = False
                user.search_wine_result = self.show_top_wine(20)
                user.select_wine_by_seq(self)
                
            elif menu_select == "2":
                fail = False
                user.search_wine(self)
                
            elif menu_select == "3":
                fail = False
                user.show_my_wine(self)
            
            elif menu_select == "4":
                fail = False
                self.user_logout()
            
            else:
                print("Invalid input. Please try again!")
    
    def outapp_menu(self):
        """A function to present menu options to users while they are not logged in"""
        fail = True
        print("=" * 40)
        print("\n" + "*" * 15 + " Wine Pocket: A pocket guide for Wine Enthusiasts " + "*" * 15 + "\n" )
        print("*~" * 40)
        print("1. Log in Wine Pocket")
        print("2. Create user account")
        print("3. Quit application")
        print("-" * 40)
        while fail:
            menu_select = input("Please select one from the menu options: ")
            if menu_select == "1":
                fail = False
                self.user_login()
            elif menu_select == "2":
                fail = False
                self.create_user()
            elif menu_select == "3":
                fail = False
                sys.exit(0)
            else:
                print("Invalid input. Please try again!")
    
    def get_wine_by_seq(self, seq):
        """The function will accept the sequence number of a wine (int type), and return the wine information"""
        try:
            if type(seq) != int:
                raise Exception
            elif seq < 0 or seq > len(self.wines):
                raise Exception
            else:
                return self.wines[seq]
        except Exception:
            print("get_wine_by_seq: Invalid input!")
    
    def show_top_wine(self, num_wine):
        """The function will accept the top number (int type), 
        and return the top number of wines based off their points.
        """
        sorted_wines = sorted(self.wines, key=lambda x: x.points, reverse=True)
        sorted_wines = sorted_wines[:num_wine]
        print("Top", num_wine, "wines are:")
        for wine in sorted_wines:
            print(wine)
        return sorted_wines            
            
class User():
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def check_num_input(self, msg, default_value):
        """A function to error handling user input for numbers. In case of error, use default value."""
        var = input(msg)
        try:
            var = float(var)
        except ValueError or TypeError:
            return default_value
        return var
    
    def check_num_range(self, msg, upperbound, lowerbound):
        """A function to error handling user input for numbers to check number within range."""
        while True:
            var = input(msg)
            try:
                var = float(var)
                if var > upperbound or var < lowerbound:
                    raise Exception("Number not within range.")
                return var 
            except:
                pass
    
    def search_wine(self, utility):
        """A function for user to search wine by:
        1. Wine title; 2. Country; 3. Variety; 4. Price range; and 5. Score range.
        Before search, the self.search_wine_result list is empty.
        After search, search results will be appended to self.search_wine_result attribute.
        Function further calls self.select_wine_by_seq() function to allow user to take action on found results.
        """
        found = False
        count = 0
        self.search_wine_result = []
        title = input("Search by Wine Title (press ENTER to skip): ")
        country = input("Search by Country (press ENTER to skip): ")
        variety = input("Search by Variety (press ENTER to skip): ")
        max_price = self.check_num_input("Search by price range - maximum price (press ENTER to skip): ", 100000)
        min_price = self.check_num_input("Search by price range - minimum price (press ENTER to skip): ", -1)
        max_score = self.check_num_input("Search by score range - maximum score (press ENTER to skip): ", 100)
        min_score = self.check_num_input("Search by score range - minimum score (press ENTER to skip): ", 0)
        
        if min_price > max_price: # swap min and max in case user error
            print("Min price is greater than max price. They will be swapped for search.")
            temp = min_price
            min_price = max_price
            max_price = temp
            
        if min_score > max_score:
            print("Min score is greater than max score. They will be swapped for search.")
            temp = min_score
            min_score = max_score
            max_score = temp
                
        for wine in utility.wines:
            if title.lower().strip() in wine.title.lower() \
            and country.lower().strip() in wine.country.lower() \
            and variety.lower().strip() in wine.variety.lower() \
            and max_price >= wine.price \
            and min_price <= wine.price \
            and max_score >= wine.points \
            and min_score <= wine.points:
                self.search_wine_result.append(wine)
                found = True
                count += 1
                
        if found == False:
            print("\nNo wine found!")
        else:
            print("\nA total of", count, "results found:")
            print("=" * 100)
            print("\n".join(map(str,self.search_wine_result)))
            # after the search results are printed, call function to allow user to proceed.
            self.select_wine_by_seq(utility)  

    def show_my_wine(self, utility):
        """A function to show all wines that the user has taken action on, i.e. want-to-taste, or have-tasted;
        Calls Utility.get_wine_by_seq() function to present the wines;
        The returned results will be appended to self.search_wine_result attribute;
        Calls self.select_wine_by_seq() function to allow user to take action on found results.
        """
        self.my_wines = []
        for item in utility.user_wine:
            if self.username == item[0]:
                self.my_wines.append(utility.get_wine_by_seq(int(item[1])))
                print(utility.get_wine_by_seq(int(item[1])))
        self.search_wine_result = self.my_wines
        self.select_wine_by_seq(utility) 
            
    def select_wine_by_seq(self, utility):
        """Prompt user to select a wine by its sequence number, and return 
        (1) wine basic information 
        (2) user's tag and review on the wine to user, if any
        (3) and prompt user to take further action on the wine.
        """
        seq_list = [int(item.seq) for item in self.search_wine_result]
        fail = True
        if seq_list != []:
            while fail:
                wine_select = int(input("Please enter wine sequence number you would like to operate on: "))
                if wine_select in seq_list:
                    fail = False
                    self.selected_wine = utility.get_wine_by_seq(wine_select)
                    print(self.selected_wine)
                    self.show_user_wine_relation(utility)
                    self.prompt_user_wine_op(utility) 
                else:
                    print("Please enter a valid sequence number from the list!")
        else:
            # in case there is no records in the search result, user can go back to home and start over.
            print("No wine for you to operate on.")
            user_prompt = input("Press 1 to return to home page: ")
            if user_prompt == "1":
                return utility.inapp_menu(self)
    
    def prompt_user_wine_op(self, utility):
        """A function to prompt user to take operations on the selected wine: 
        1. tag as want to taste or have tasted
        2. or return to home page if quit.
        """
        fail = True # a flag to check if user inputs valid action
        while fail:
            print("=" * 50)
            print("You may take the following actions:")
            print("1. Tag the wine as Want-to-taste | 2. Tag the wine as Have-tasted and add review  | 3. Return to home page")
            user_prompt = input("Please select 1, 2, or 3: ")
            if user_prompt == "1":
                fail = False
                return self.want_taste(utility)
            elif user_prompt == "2":
                fail = False
                return self.have_tasted(utility)
            elif user_prompt == "3":
                fail = False
                return utility.inapp_menu(self)
            else:
                print("Invalid input. Please try again!")
    
    def show_user_wine_relation(self, utility):
        """A function to show user's relation with the wine:
        1. want-to-taste, or
        2. have tasted, score, brief review, and if recommend, or
        3. no interaction
        """
        found = False
        for item in utility.user_wine:
            if self.username == item[0] and self.selected_wine.seq == item[1]:
                print("\n" + "=" * 100)
                print("Here is your review of", self.selected_wine.title)
                print("-" * 100)
                if item[2] == "1":
                    print("You tag as Want-to-taste")
                if item[3] == "1":
                    print("You tag as Have-tasted")
                    print("Score:", item[4])
                    print("Brief Review:", item[5])
                    if item[6] != "":
                        if float(item[6]) > 0:
                            print("Mark as Recommend: Yes")
                        else:
                            print("Mark as Recommend: No")
                found = True
                break
        if found == False:
            print("=" * 100)
            print("You haven't interacted with", self.selected_wine.title, "yet.")
    
    def want_taste(self, utility):
        """A function to allow user to tag a wine as want-to-taste:
        1. if already want-to-taste or have-tasted, cannot want-to-taste again;
        2. otherwise, user can want-to-taste;
        3. Utility.user wine attribute will be appended with new record;
        4. user_wine.csv will be appended with new relation between user and wine.
        5. After action take, prompt user to go back to home page.
        """
        found = False
        for item in utility.user_wine:
            if self.username == item[0] and self.selected_wine.seq == item[1]:
                if item[2] == "1":
                    print ("You've already marked", self.selected_wine.title,"as want-to-taste!")
                if item[3] == "1":
                    print("You've already tasted " + self.selected_wine.title + "!")
                found = True
                break
        if found == False:
            utility.user_wine.append([self.username,self.selected_wine.seq,"1","0","","",""])
            with open('user_wine.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([self.username,self.selected_wine.seq,"1","0","","",""])
                print("Successfully want to taste " + self.selected_wine.title + "!")
                
        user_prompt = input("Press 1 to return to home page: ")
        if user_prompt == "1":
            utility.inapp_menu(self) 
    
    def have_tasted(self, utility):
        """A function to allow user to tag a wine as have-tasted:
        1. if already have-tasted, cannot have-tasted again;
        2. if already want-to-taste, user can update to have-tasted, and give score, review and recommend
           2a. in this case, the Utility.user_wine existing record will be updated with new relation
           2b. user_wine.csv existing row will be updated with new relation;
        3. if no relation, user can mark as have-tasted;
           3a. Utility.user wine attribute will be appended with new record;
           3b. user_wine.csv will be appended with new relation between user and wine.
        4. After action take, prompt user to go back to home page.
        """
        found = False
        for item in utility.user_wine:
            if self.username == item[0] and self.selected_wine.seq == item[1]:
                if item[3] == "1":
                    print("You've already tasted " + self.selected_wine.title + "!")
                    found = True
                    break
                if item[2] == "1":
                    row_num = utility.user_wine.index(item)
                    found = True
                    user_score = self.check_num_range("Please provide a score on a scale of 0 to 100 for the wine: ", 100, 0)
                    user_review = input("Please provide short review for the wine (press ENTER to skip): ")
                    user_recommend = self.check_num_range("Do you want to recommend this wine? Press 1 for Yes, 0 for No: ", 1, 0)
                    utility.user_wine[row_num] = [self.username, self.selected_wine.seq, "0", "1", user_score, user_review, user_recommend]
                    # update the corresponding row in the user_wine.csv file
                    tempfile = NamedTemporaryFile(mode='w', delete=False)
                    fields = ['user', 'wine', 'want_to_taste', 'have_tasted', 'score', 'review', 'recommend']
                    with open('user_wine.csv', 'r') as csvfile, tempfile:
                        reader = csv.DictReader(csvfile, fieldnames=fields)
                        writer = csv.DictWriter(tempfile, fieldnames=fields)
                        for row in reader:
                            if row['user'] == self.username and row['wine'] == self.selected_wine.seq:
                                row['want_to_taste'], row['have_tasted'], row['score'], row['review'], row['recommend'] = \
                                "0", "1", user_score, user_review, user_recommend
                            row = {'user': row['user'], 'wine': row['wine'], 'want_to_taste': row['want_to_taste'], 
                                    'have_tasted': row['have_tasted'], 'score':row['score'], 'review':row['review'], 
                                    'recommend':row['recommend']}
                            writer.writerow(row)
                            
                    shutil.move(tempfile.name, 'user_wine.csv')

        if found == False:
            user_score = self.check_num_range("Please provide a score on a scale of 0 to 100 for the wine: ", 100, 0)
            user_review = input("Please provide short review for the wine (press ENTER to skip): ")
            user_recommend = self.check_num_range("Do you want to recommend this wine? Press 1 for Yes, 0 for No: ", 1, 0)
            utility.user_wine.append([self.username, self.selected_wine.seq, "0", "1", user_score, user_review, user_recommend])
            with open('user_wine.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([self.username, self.selected_wine.seq, "0", "1", user_score, user_review, user_recommend])
                print("Successfully add review to " + self.selected_wine.title + "!")
        
        user_prompt = input("Press 1 to return to home page: ")
        if user_prompt == "1":
            utility.inapp_menu(self) 
    
    
class Wine():
    
    def __init__(self, seq, country, description, designation, points, price, province, title, variety, winery):
        self.seq = seq
        self.country = country
        self.description = description
        self.designation = designation
        self.points = float(points)
        if price == "": # NULL data handling for price range search
            self.price = -1.0
        else:
            self.price = float(price)
        self.province = province
        self.title = title
        self.variety = variety
        self.winery = winery
    
    def show_avg_score(self):
        """a function to show wine points"""
        print("The average score for", self.title, "is", self.points)
        return self.points

    def __str__(self):
        return self.seq + " | " + "Title: " + self.title + " | " + "Country: " + self.country + " | " + "Variety: " + self.variety + " | " + "Price: " + str(self.price) + " | " + "Points: " + str(self.points) 

    def __repr__(self):
        return self.seq + " | " + "Title: " + self.title + " | " + "Country: " + self.country + " | " + "Variety: " + self.variety + " | " + "Price: " + str(self.price) + " | " + "Points: " + str(self.points) 

u = Utility()
u.outapp_menu()
