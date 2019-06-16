import csv
import os
import statistics
import pandas

csv_file_path = 'data/keywordstats4.csv'  #TODO - Make Dynamic user input
campaign_csv_file_path = 'data/Campaign-Rules.csv' #TODO: Use OS relative file paths
write_csv_file_path = 'build/adgroups.csv'
group_csv_file_path = 'data/Group-Rules.csv'

#TODO DEFINE FUNCTIONS WHICH I CAN CALL FROM INSIDE WHILE LOOP TO CREATE CSV

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
    

#CSV READER CODE
    # #with open(csv_file_path, "r") as csv_file: # Code from class repository
    #    reader = csv.DictReader(csv_file) # assuming your CSV has headers
    #    for row in reader:
    #        print(row["keyword"], row["Currency"])

    #df = pandas.read_csv(csv_file_path, skiprows=2, nrows=50, encoding='utf-8')

df = pandas.read_csv(csv_file_path, encoding='utf-8')
#df = pandas.read_csv(csv_file_path)
print(df)
rows = df.to_dict("records")

#SETTING UP CAMPAIGNS
dfg = pandas.read_csv(campaign_csv_file_path, encoding='utf-8')
campaigns = dfg.to_dict("records")
treatment = [r['Treatment'] for r in campaigns]   #list of terms to define as treatment
symptoms = [r['Symptoms'] for r in campaigns]
condition = [r['Condition'] for r in campaigns]

#SETTING UP GROUPS
dfgroup = pandas.read_csv(group_csv_file_path, encoding='utf-8')
adgroups = dfgroup.to_dict("records") 

with open(write_csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Keyword", "Campaign", "Group", "Avg Monthly Searches"])
        writer.writeheader() # uses fieldnames set above
        #writer.writerow({"Keyword": "test", "Campaign": "test"})

#CAMPAIGN SORTER AND ORGANIZER - WRITE CSV
# THIS IS THE BULK OF THE PROGRAM
for r in rows:
    kw = [r['Keyword']] #for r in rows]
    searches = [r['Avg. monthly searches']] #for r in rows]
    kw = kw[0]
    searches = searches[0]
    kwlookuplist = kw.split()
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


    with open(write_csv_file_path, "a", newline='') as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Keyword", "Campaign", "Group", "Avg Monthly Searches"])
        writer.writerow({"Keyword": kw, "Campaign": kwcampaign, "Group": writegroup, "Avg Monthly Searches": searches})


#OUTPUT THE VOLUME PER CAMPAIGN

dfx = pandas.read_csv(write_csv_file_path, encoding='utf-8')
buildout = dfx.to_dict("records")

treatment_kwvol = [b["Avg Monthly Searches"] for b in buildout if b["Campaign"] == 'Treatment']
treatment_volume = sum(treatment_kwvol)
condition_kwvol = [b["Avg Monthly Searches"] for b in buildout if b["Campaign"] == 'Condition']
condition_volume = sum(condition_kwvol)
symptoms_kwvol = [b["Avg Monthly Searches"] for b in buildout if b["Campaign"] == 'Symptoms']
symptoms_volume = sum(symptoms_kwvol)

ctr = .03  #TODO : Make CTR and CPC a user input
cpc = 3    #TODO : Make CTR and CPC a user input



#PRINT THE TOTAL VOLUME
while True: #creating while function for purposes of minimizing code
    print("")
    print("--------------------------------------------------------")
    print("Projected Search Volume and Expected Traffic By Campaign")
    print("--------------------------------------------------------")
    print("Total Volume :" + str(treatment_volume + condition_volume + symptoms_volume))
    #PRINT SYMPTOMS
    print("")
    print("Symptoms")
    print("Impressions : " + str(condition_volume))
    print("Clicks : " + str(condition_volume * ctr))
    print("Cost : $" + str(condition_volume * ctr * cpc))
    #PRINT CONDITION
    print("")
    print("Condition : ")
    print("Impressions : " + str(symptoms_volume))
    print("Clicks : " + str(symptoms_volume * ctr))
    print("Cost : $" + str(symptoms_volume * ctr * cpc))
    print("")

    #PRINT TREATMENT
    print("Treatment :")
    print("Impressions : " + str(treatment_volume))
    print("Clicks : " + str(treatment_volume * ctr))
    print("Cost : $" + str(treatment_volume * ctr * cpc))
    break


print("done")