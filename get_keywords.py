import uuid
from googleads import adwords


# Initialize the AdWords client.
#adwords_client = adwords.AdWordsClient.LoadFromStorage()
adwords_client = adwords.AdWordsClient.LoadFromStorage("yaml/googleads2.yaml")

targeting_idea_service = adwords_client.GetService('TargetingIdeaService', version='v201809')

PAGE_SIZE = 100

# BELOW CODE FROM GOOGLE
# https://developers.google.com/adwords/api/docs/guides/targeting-idea-service

selector = {
    'ideaType': 'KEYWORD',
    'requestType': 'IDEAS'
}


selector['requestedAttributeTypes'] = [
    'KEYWORD_TEXT', 'SEARCH_VOLUME', 'AVERAGE_CPC']


offset = 0
selector['paging'] = {
    'startIndex': str(offset),
    'numberResults': str(PAGE_SIZE)
}


#INPUT THE QUERIES
input_array = []
finished_entering = False
while not finished_entering:
    user_input = input("Please Enter A Keyword Idea and Type DONE When Finished:   ")
    if user_input == "done" or user_input == "DONE" or user_input == "Done":
        finished_entering = True
    else:
        input_array.append(user_input)

#breakpoint()


selector['searchParameters'] = [{
    'xsi_type': 'RelatedToQuerySearchParameter',
    'queries': input_array
}]

#breakpoint()
page = targeting_idea_service.get(selector)

#PARSE THE RESPONSE - THE BELOW IS GOOGLE CODE
keyword_list = []

for result in page['entries']:
  attributes = {}
  for attribute in result['data']:
    attributes[attribute['key']] = getattr(
        attribute['value'], 'value', '0')

    

  #print ('Keyword with "%s" text and average monthly search volume '
  #       '"%s" was found with Avg CPC: %s.'
  #       % (attributes['KEYWORD_TEXT'],
  #          attributes['SEARCH_VOLUME'],
  #          attributes['AVERAGE_CPC']))
  
  kwrow = {
      "Keyword": attributes['KEYWORD_TEXT'],
      "Avg. monthly searches": attributes['SEARCH_VOLUME']
  }
  keyword_list.append(kwrow)

#parse_entries = page['entries']
#print(parse_entries)

#for r in keyword_list:
#    kw = r['Keyword']
#    searches = r['Avg. monthly searches']
#    print(kw + " " + str(searches))
#    breakpoint()
#   # print("Keyword: "+ kw + " and Searches:" + searches)

print(keyword_list)

