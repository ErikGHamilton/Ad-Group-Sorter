import os
import pytest

from Sorter import campaign_lookup_function

#Still ironing out the kinks

def test_campaign_lookup():
    inputkeywordlist = ['parkinsons', 'disease', 'treatment']
    kwcampaign = campaign_lookup_function(inputkeywordlist)
    assert kwcampaign == "Treatment"
