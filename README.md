# Ad-Group-Sorter
Ad Group Sorter for Pharma Campaigns by Erik Hamilton

IMPORTANT:

    Prior to running this program you MUST have a properly configured googleads.yaml file
    To create this, follow the Google Ads API instructions here https://github.com/googleads/googleads-python-lib
    
    Configuring the API is complicated and may take some time, and requires the creation of OAuth and OAuth refresh tokens

    When the googleads.yaml file is created, place it in the /yaml folder and name it googleads2.yaml. The file path relative to the main repository should then be /yaml/googleads2.yaml

    DO NOT share these credentials with anyone else, or publish them to Github



SETTING UP THE VIRTUAL ENVIRONMENT:

    Prior to running the program, create a conda virtual environment using the command line code:
        conda create -n adgroup-env python=3.7
    
    Once created, activate the environment and install the necessary modules (pandas, google ads)
        conda activate adgroup-env
        pip install pandas
        pip install googleads



RUNNING THE PROGRAM:

    Activate the program by using the command line input
        python sorter-v2.py

    This will activate the most recent version of the file. Sorter.py is the original version, and contains a few more lines of notes as well as some of the original functions as notes. Sorter-v2 has cleaned up the code, formatted the outputs more cleanly and added a try/except loop.

    When prompted, input the desired terms to send to the Google Ads API keyword lookup function. It is highly recommended that you use one word 'base' terms such as: 
        diabetes, diabete, insomnia, parkinson, parkinson's, als, adhd

    This will help the Google Ads API make the best possible suggestions, as well as allow the campaign sorter script to work most efficiently and accurately. 

    Enter in 4 or 5 terms for best results.


    The program will then begin to call the Google Ads API. If the Google Ads API returns an error - most likely a RateExceeded error, the program will wait 30 seconds before calling again, and will continue until finished.


    ONCE THE GOOGLE ADS API CALL IS COMPLETED:


    The program will ask for click through rate and cpc estimates, and then calculate the total estimated search volume, site traffic and cost per month, as well as a 12 month period.

    The suggested campaign and ad group structure will be written to a CSV in the /data folder. The file will be named after the condition entered and the time stamp during which the program was run. 

    For example: if your condition is parkinsons and the program ran at 06:41 on 06/20/19, the file will be named 
        parkinsons062019-0641




    




