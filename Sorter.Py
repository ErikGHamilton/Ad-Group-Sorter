import csv
import os
import pandas

csv_file_path = 'data/keywordstats4.csv'  #TODO - Make Dynamic
campaign_csv_file_path = 'data/Campaign-Rules.csv'
write_csv_file_path = 'build/adgroups.csv'

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
    #Logic: 
    # kwindex = inputkeyword.split()
    # for term in kwindex
    #group = i["group"] if i["identifying term"] == term
    return("asf")



#CSV READER CODE
    # #with open(csv_file_path, "r") as csv_file: # Code from class repository
    #    reader = csv.DictReader(csv_file) # assuming your CSV has headers
    #    for row in reader:
    #        print(row["keyword"], row["Currency"])

    #df = pandas.read_csv(csv_file_path, skiprows=2, nrows=50, encoding='utf-8')

df = pandas.read_csv(csv_file_path, encoding='utf-8')

print(df)
rows = df.to_dict("records")
#print("")
#keywords = [r['Keyword'] for r in rows]
#kw = keywords[5] 
#searches = [r['Avg. monthly searches'] for r in rows]
#print(keywords[0],",",searches[0])
#print(keywords)

#SETTING UP CAMPAIGNS
dfg = pandas.read_csv(campaign_csv_file_path, encoding='utf-8')
campaigns = dfg.to_dict("records")
treatment = [r['Treatment'] for r in campaigns]
symptoms = [r['Symptoms'] for r in campaigns]
condition = [r['Condition'] for r in campaigns]


for r in rows:
    kw = [r['Keyword']] #for r in rows]
    searches = [r['Avg. monthly searches']] #for r in rows]
    kw = kw[0]
    searches = searches[0]
    kwlookuplist = kw.split()
    print(kwlookuplist)

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

    print(kw + kwcampaign + str(searches))
    print("")

    with open(write_csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=["Keyword", "Campaign"])
        writer.writeheader() # uses fieldnames set above
        writer.writerow({"Keyword": kw, "Campaign": kwcampaign})
