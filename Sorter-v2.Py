import csv
import os
import time
import statistics
import pandas
import uuid
from datetime import datetime
from googleads import adwords
from get_keywords_func import get_adwords_keywords

today = datetime.now().strftime('%Y-%m-%d')
hour = datetime.now().strftime('%H-%M')

#csv_file_path = 'data/keywordstats8.csv'  #TODO - Make Dynamic user input or pull from API
#campaign_csv_file_path = 'data/Campaign-Rules.csv' #TODO: Use OS relative file paths
campaign_csv_file_path = os.path.join(os.path.dirname(__file__), "data", "Campaign-Rules.csv")
#write_csv_file_path = 'build/adgroups3.csv'
#group_csv_file_path = 'data/Group-Rules.csv'
group_csv_file_path = os.path.join(os.path.dirname(__file__), "data", "Group-Rules.csv")


def get_user_input():
    print("")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("Welcome to the Ad Group Sorter")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("Instructions: ")
    print("   Enter in the primary condition keywords for your account")
    print("   (e.g. diabetes, parkinsons, what is insomnia)")
    print("   Input four or five terms for best results but do not include treatment or symptoms terms")
    print("-----------------------------------------------------------------")
    print("-----------------------------------------------------------------")
    print("")
    #INPUT THE QUERIES
    input_array = []
    finished_entering = False
    while not finished_entering:
        user_input = input("Please Enter A Keyword Idea and Type DONE When Finished:   ")
        if user_input == "done" or user_input == "DONE" or user_input == "Done":
            finished_entering = True
        else:
            user_input = user_input.lower()
            input_array.append(user_input)
    return(input_array)

def campaign_lookup_function(inputkeywordlist):
    for k in inputkeywordlist:
        #breakpoint()
        if k in treatment:
            return("Treatment")
        elif k in symptoms:
            return("Symptoms")
        else:
            pass

def campaign_lookup_function2(inputkeywordlist):
    for k in inputkeywordlist:
        #breakpoint()
        if k in condition:
            return("Condition")
        else:
            pass
            
def adgroup_lookup_function(inputgroupkeyword):
    for x in adgroups:
        returngroup = [x["Ad Group"] for x in adgroups if x["Term"] in inputgroupkeyword]
        return(returngroup)
    # for term in kwindex
    #group = i["group"] if i["identifying term"] == term
    

#SETTING UP CAMPAIGNS
dfg = pandas.read_csv(campaign_csv_file_path, encoding='utf-8')
campaigns = dfg.to_dict("records")
treatment = [r['Treatment'] for r in campaigns]   #list of terms to define as treatment
symptoms = [r['Symptoms'] for r in campaigns]
#condition = [r['Condition'] for r in campaigns]   
#Making the user input = condition so that it is more dynamic - see row ~100


#SETTING UP GROUPS
dfgroup = pandas.read_csv(group_csv_file_path, encoding='utf-8')
adgroups = dfgroup.to_dict("records") 


#GET USER INPUT

input_array = get_user_input()
condition = input_array #Definining my condition terms as the user input

#SEND TO ADWORDS - Send user input and get back rows (the keywords / search volume)
#ADDED IN TRY/Except per prof suggestions

api_success = False
while not api_success:
    try:
        rows = get_adwords_keywords(input_array)
        print("The Google Ads API call was a success")
        api_success = True
    except:
        print("Apologies for the delay while we call the Google Ads API")
        #print("There has been an error - likely due to overloading of the Google Ads API")
        #print("Trying again in 30 seconds")
        time.sleep(15)
        #print("Trying again in 15 seconds")
        time.sleep(15)

#CREATE CSV

today_condition = today + hour + input_array[0] + ".csv"
write_csv_file_path = os.path.join(os.path.dirname(__file__), "build", today_condition)

with open(write_csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Keyword", "Campaign", "Group", "Avg Monthly Searches"])
        writer.writeheader() # uses fieldnames set above
        #writer.writerow({"Keyword": "test", "Campaign": "test"})


#CAMPAIGN SORTER AND ORGANIZER - WRITE CSV
# THIS IS THE BULK OF THE PROGRAM !!! Important
for r in rows:
    kw = [r['Keyword']] #for r in rows]
    searches = [r['Avg. monthly searches']] #for r in rows]
    kw = kw[0]
    searches = searches[0]
    kwlookuplist = kw.split() #h/t stackoverflow for the .split tip
    #print(kwlookuplist)

    kwcampaign = campaign_lookup_function(kwlookuplist)
    #print("campaign1 = " + kwcampaign)
    if kwcampaign not in ["Symptoms", "Treatment"]:
        kwcampaign = campaign_lookup_function2(kwlookuplist)
    else:
        pass
    if kwcampaign not in ["Symptoms", "Treatment", "Condition"]:
       kwcampaign = "Unclassified"
    else:
        pass
    
    kwgroup = adgroup_lookup_function(kwlookuplist)
    writegroup = ''.join(str(e) for e in kwgroup)


    with open(write_csv_file_path, "a", newline='', encoding='utf-8') as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Keyword", "Campaign", "Group", "Avg Monthly Searches"])
        writer.writerow({"Keyword": kw, "Campaign": kwcampaign, "Group": writegroup, "Avg Monthly Searches": searches})


#OUTPUT THE VOLUME PER CAMPAIGN
dfx = pandas.read_csv(write_csv_file_path, encoding='latin1') #latin1 since i was having writing / ascii issues - stackoverflow again with the tip
buildout = dfx.to_dict("records")

#TODO MAKE THIS ALL A FUNCTION
treatment_kwvol = [b["Avg Monthly Searches"] for b in buildout if b["Campaign"] == 'Treatment']
treatment_volume = round(sum(treatment_kwvol),2)

condition_kwvol = [b["Avg Monthly Searches"] for b in buildout if b["Campaign"] == 'Condition']
condition_volume = round(sum(condition_kwvol),2)

symptoms_kwvol = [b["Avg Monthly Searches"] for b in buildout if b["Campaign"] == 'Symptoms']
symptoms_volume = round(sum(symptoms_kwvol),2)


print("")
print("--------------------------------------------------------")
ctr = float(input("Please enter your expected click through rate in decimal format (ie: 3% = 0.03)  ")) #TODO MAKE FUNCTION WITH QA LOOP
cpc = float(input("Please enter your expected CPC in numerical format (ie: $2.5 = 2.5)  "))
print("--------------------------------------------------------")

#TODO Make all this math and cleaning up of the numbers a function

treatment_clicks = treatment_volume * ctr
treatment_cost = treatment_clicks * cpc
treatment_clicks = round(treatment_clicks,2)
treatment_cost = round(treatment_cost,2)

condition_clicks = condition_volume * ctr
condition_cost = condition_clicks * cpc
condition_clicks = round(condition_clicks,2)
condition_cost = round(condition_cost,2)

symptoms_clicks = symptoms_volume * ctr
symptoms_cost = symptoms_clicks * cpc
symptoms_clicks = round(symptoms_clicks,2)
symptoms_cost = round(symptoms_cost,2)

total_volume = symptoms_volume + condition_volume + treatment_volume
total_clicks = symptoms_clicks + condition_clicks + treatment_clicks
total_cost = symptoms_cost + condition_cost + treatment_cost
total_volume = round(total_volume,2)
total_clicks = round(total_clicks,2)
total_cost = round(total_cost,2)


#PRINT THE TOTAL VOLUME
while True: #creating while function for purposes of minimizing code
    print("")
    print("----------------------------------------------------------------")
    print("Projected Monthly Search Volume and Expected Traffic By Campaign")
    print("----------------------------------------------------------------")
    print("Campaign Totals: ")
    print("Impressions :" + str(total_volume))
    print("Clicks :" + str(total_clicks))
    print("Cost : $" + str(total_cost))
    #PRINT SYMPTOMS
    print("")
    print("Symptoms")
    print("Impressions : " + str(symptoms_volume))
    print("Clicks : " + str(symptoms_clicks))
    print("Cost : $" + str(symptoms_cost))
    #PRINT CONDITION
    print("")
    print("Condition : ")
    print("Impressions : " + str(condition_volume))
    print("Clicks : " + str(condition_clicks))
    print("Cost : $" + str(condition_cost))
    print("")

    #PRINT TREATMENT
    print("Treatment :")
    print("Impressions : " + str(treatment_volume))
    print("Clicks : " + str(treatment_clicks))
    print("Cost : $" + str(treatment_cost))

    #Print Yearly Volume
    print("----------------------------------------------------------------")
    print("Projected Yearly Search Volume and Expected Traffic")
    print("----------------------------------------------------------------")
    print("Campaign Totals: ")
    print("Impressions :" + str(round(total_volume * 12,2)))
    print("Clicks :" + str(round(total_clicks * 12,2)))
    print("Cost : $" + str(round(total_cost * 12,2)))

    break


print("")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("")