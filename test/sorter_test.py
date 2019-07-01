import os
import pytest

from sorter-v2 import campaign_lookup_function

def test_campaign_lookup:
    inputkeywordlist = ['parkinsons', 'disease', 'treatment']
    kwcampaign = campaign_lookup_function(inputkeywordlist)
    assert kwcampaign == 'Treatment'
