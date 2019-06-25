import uuid
from googleads import adwords


# Initialize the AdWords client.
#adwords_client = adwords.AdWordsClient.LoadFromStorage()
adwords_client = adwords.AdWordsClient.LoadFromStorage("yaml/googleads.yaml")

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


#TODO : UPDATE THE QUERIES SECTION TO TAKE A USER INPUT - MAKE IT A LIST

selector['searchParameters'] = [{
    'xsi_type': 'RelatedToQuerySearchParameter',
    'queries': ['space cruise']
}]

#breakpoint()
page = targeting_idea_service.get(selector)

#PARSE THE RESPONSE - THE BELOW IS GOOGLE CODE

for result in page['entries']:
  attributes = {}
  for attribute in result['data']:
    attributes[attribute['key']] = getattr(
        attribute['value'], 'value', '0')
  print ('Keyword with "%s" text and average monthly search volume '
         '"%s" was found with Products and Services categories: %s.'
         % (attributes['KEYWORD_TEXT'],
            attributes['SEARCH_VOLUME'],
            attributes['CATEGORY_PRODUCTS_AND_SERVICES']))