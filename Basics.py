#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets ##
# 
# In this guided project I am going to analize the data set from two markets: Google Play and App Store to find potentialy the most profitable application types.
# 
# I am going to be focused only on the free apps, for english speaking usesers, making their revenue based on in-app adds.
# In few steps I am going to present data cleaning and further analysing.
# 
# Google Play store data set comes from __[here](https://www.kaggle.com/lava18/google-play-store-apps/home)__
# 
# Apps Store data set comes from __[here](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)__

# ##  Step 1: Opening Google Play and Apps Store data sets

# In[1]:


from csv import reader

#android dataset
file_and = open('googleplaystore.csv')
read_and = reader(file_and)
android = list(read_and)
header_and = android[0]
data_and = android[1:]

#IOS dataset
file_ios = open('AppleStore.csv')
read_ios = reader(file_ios)
ios = list(read_ios)
header_ios = ios[0]
data_ios = ios[1:]


# ## Using explore_data() function to investigate both data sets.

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


print(explore_data(data_and,0,5,True))


# In[4]:


print(explore_data(data_ios,0,5,True))


# Displaying both header rows for easier data identification.

# In[5]:


print(header_and)


# In[6]:


print(header_ios)


# # Step I : Cleaning Data

# On kaggle.com webiste there is a forum group where people are discussing about this dta sets and they have found an error in Google Play data set which I am going to fix next. Topic can be found and follwed __[here](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015)__
# 

# In[7]:


#Printing row 10472 from android data set with missing data at index 9.
print(data_and[10472])


# Deleting an error row from the Google Play data set:

# In[8]:


del data_and[10472]


# ## Checking if data set does not contain any duplicates:

# In[9]:


unique_apps = []
duplicate_apps = []

#iterating  over data set and appending duplicate entries to separate list
for row in data_and:
    name = row[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    unique_apps.append(name)
    
#displaying number of duplicate entries
print(len(duplicate_apps))

    


# ## Removing duplicate Apps from Google Play dataset

# Removing duplicate enries using criterias such as: number of reviews, last updated or number of installs to find the most recent row in data set.

# In[ ]:





# ### Step 1 
# ### Creating a dictionary where the  key is the app name and value is highest number of reviews found in the data set.

# In[10]:


reviews_max = {}

for app in data_and:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    if name not in reviews_max:
        reviews_max[name] = n_reviews
    
        


# Displaying lenght of the dictionary to make sure it is as long as the data set

# In[37]:


print(len(reviews_max))
print(len(data_and) - len(duplicate_apps))


# ### Step 2
# ### Removing duplicate rows from Google Palay data set

# In[12]:


#creating two empty lists

android_clean = []
already_added = []

# iterating through the Google Play data set

for app in data_and:
    name = app[0]
    n_reviews = float(app[3])
# adding unique app names to the new list
    if reviews_max[name] == n_reviews and name not in already_added: 
        android_clean.append(app)
        already_added.append(name)
        


# ### Step 3
# ### Removing non - english apps using is_ang() funcion

# In[38]:


# creating function

def is_ang(string):
    for char in string:
        if ord(char) > 127:
            return False
        
    return True
        
        


# Checking sample app names to see if they are english and if the function works

# In[14]:


is_ang('Instagram')


# In[15]:


is_ang('爱奇艺PPS -《欢乐颂2》电视剧热播')


# In[16]:


is_ang('Docs To Go™ Free Office Suite')


# In[17]:


is_ang('Instachat 😜')


# Amending function to make sure that it will chceck apps data corectly including names with special characters (up to 3).

# In[39]:


# creating updated function

def is_ang(string):
    count = 0
    for char in string:
        if ord(char) > 127:
            count = count + 1
        
        if count > 3:
             return False
        
    return True


# Checking updated function:

# In[19]:


is_ang('Docs To Go™ Free Office Suite')


# In[20]:


is_ang('Instachat 😜')


# In[21]:


is_ang('爱奇艺PPS -《欢乐颂2》电视剧热播')


# Using updated is_ang() function to analize both data sets and remove non-english apps.

# In[22]:


#creating new lists for english apps and ireatating over both data sets to filter them.

andr_english = []
ios_engish = []

for app in android_clean:
    name = app[0]
    if is_ang(name):
        andr_english.append(app)
        
for app in data_ios:
    name = app[1]
    if is_ang(name):
        ios_engish.append(app)       
    


# Exploring number of rows left in each data set

# In[23]:


print(len(andr_english))


# In[24]:


print(len(ios_engish))


# ### Step 4
# ### Isolating apps which can be downloaded free of charge

# In[40]:


andr_final = []
ios_final = []

for app in andr_english:
    if app[7] == '0':
        andr_final.append(app)
        
for app in ios_engish:
    if app[4] == '0.0':
        ios_final.append(app)  
        
print(len(andr_final))
print(len(ios_final))


# #  Step II : Data Analysis

# I am going to try to find an app profile which is the most popular on both markets using criterias from column Genres and Category for Android or prime_genre for IOS. It will help me to understad which apps are the most comon on each market and I will be able to ideantify app profile with the bigges potential.
# 

# ### Creating function frequency table for further analysis.
# Funcion displays how often each app apears in the data set.
# In this subject the values will be displayed in percentage.

# In[41]:


def freq_table(dataset,index):
    freq_dict = {}
    count = 0
    
    for row in dataset:
        count = count +  1
        value = row[index]
        if value in freq_dict:
            freq_dict[value] = freq_dict[value] + 1
        else:
            freq_dict[value] = 1
            

# transforming values to percentages          

    freq_perc = {}
    
    for each in freq_dict :
        percentage = (freq_dict[each] / count) * 100
        freq_perc[each] = percentage
       
    return freq_perc
    


# ### Using display_table() function for presenting sorted  results.

# In[27]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# Displaying and analising prime_genre column from IOS dataset and  Genres, Category from Google Play data set.

# In[28]:


display_table(ios_free,11) #IOS dataset


# Looking at IOS apps frequency table we can see that over a half of the apps are games - 58%, second place has been taken by Entertaiment apps - nearly 8% and theird place apps in ratting are Photo & Video which score just below 5%.
# Looks like it there have to be a big demand for the entertaining apps such us games in the IOS dataset if there is so many of them comparing to much smalleer numers infortational apps.
# 

# In[29]:


display_table(andr_free,1) #Google Play data set


# Looking at the Goole Play frequency table for Category column it can be noticed that games do not appear as offten as in Apps Store data set. Number of game apps in ios data set is still high which can be a pattern that there is a  market for the android game apps too. Esecially that the first place with nearly 19% of all apps in the data set has been taken by familly apps which are also entertaining and there is propably a number of games for kids too. However for more acurate suggestions we will need number of installs per Genre to see how many user each Genre actually have.

# In[42]:


#displayig Genre column from Google Play data set
display_table(andr_free,9)


# As we can see that one of the most popular apps by Genre are still entertainig apps. We can not also underestimate the Tool apps which have taken the first place.
# 
# So far we could be under impression that if there is so many entertaining apps there have to be a demand for it online.
# In the further analisys we wil havea look an number of install per Genre to see how many users each type of the app has and see exactly market proportions.

# ### Counting the average app installs per Genre from IOS dataset based on the number os users ratings column.

# In[31]:


def freq_table(dataset,index):
    freq_dict = {}
    
    for row in dataset:
        value = row[index]
        if value in freq_dict:
            freq_dict[value] = freq_dict[value] +  1
        else:
            freq_dict[value] = 1
            
    return freq_dict


# In[32]:


rat_count_tot = freq_table(ios_free,-5)


# In[33]:


for genre in rat_count_tot:
    total = 0 # number of user ratings
    len_genre = 0 # number of apps per genre
    for each in ios_free:
        genre_app = each[-5] # 'prime genre' column
        if genre_app == genre:
            num_ratings = float(each[5]) # 'rating count total' column
            total = total + num_ratings
            len_genre = len_genre + 1
    average = total / len_genre
    print(genre, ':', average)
        
    
    


# The most popular apps in the Apps Store are Navigation apps and Social Networking. It might be coused by apps such us Facebbok, Instagram or Google Maps so to come up with recomedation I would also consider generes just below the top 3. 
# Games and Entertaining apps have still aslo large number of installs and looks like it there is a big marked there however seeing frequency of number of papps per genre there is a lot of cometition in this type of the apps too.

# ### Removing spare characters from installs column in the Google Play data set to count the number of installs per Genre

# In[43]:


category_table = freq_table(andr_free, 1)


# In[45]:


for category in category_table:
    total = 0 # sum of installs per genre
    len_category = 0 # num apps per category
    for each in andr_free:
        category_app = each[1]
        if category_app == category:
            num_installs = each[5]
            num_installs = num_installs.replace('+', '')
            num_installs = num_installs.replace(',','')
            num_installs = float(num_installs)
            total = total + num_installs
            len_category = len_category + 1
            
    average_installs = total / len_category
    print(category, ':',average_installs)
    


# Looking at this table we can clearly see that the most installs have the comunication apps which is not a supprise as we all these days use apps such as messenger, whatsapp or hangout to comunicate each other. Similar to the IOS data set there is a big potetial to come up with a new comuniactional app however we need also consider how difficoul it has to be to drag people away from egzisting well known apps. So to come up with a new potentially popular app profile we could chose between following trends and competing with the giants on the market or try to find a nish in betewtn already popular apps where comeptition is much easier and the chance for taking a lead is much bigger.

# In[ ]:





# In[ ]:




