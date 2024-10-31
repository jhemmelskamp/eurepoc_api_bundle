from endpoints import EuRepoC
import pandas as pd
import requests

HEADERS = {
        'Authorization': "<insert here>", # TODO Insert API KEY
        'Content-Type': 'application/json',
        'User-Agent': 'EuRepoC' # required 
    }

BASE_URL = "https://api.eurepoc.eu"



def get_eurepoc_data(endpoint: EuRepoC) -> pd.DataFrame:
    """
    Takes one API endpoint, pulls all data from it without filters and puts it into a pandas dataframe
    """

    response = requests.get(BASE_URL + endpoint.value, headers=HEADERS)

    if response.status_code == 200:
        json_response = response.json()
        df = pd.DataFrame(json_response)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)

    return df.set_index("incident_id")


def get_full_eurepoc_dataset(added_to_db: pd.Timestamp) -> pd.DataFrame:
    """
    Pulls the entire EuRepoC dataset and puts it into a pandas dataframe in long format.
    This will contain many (tens of thousands) duplicates, because one incident can have multiple receivers, attributions, etc.
    """
    
    # the easiest approach is to left join the dataframes
    for _i, endpoint in enumerate(EuRepoC):
        if _i == 0:
            df = get_eurepoc_data(EuRepoC.INCIDENTS)
            df.added_to_db = pd.to_datetime(df.added_to_db) # Transform EuRepoC detection date to timestamp
            df = df[df.added_to_db >= added_to_db] # filter the dataset based on start_date
        # Initiators are included in attributions and operation types in incidents. We also exclude sources because it makes the DF too giant.
        elif endpoint in [EuRepoC.INITIATORS, EuRepoC.OPERATION_TYPES, EuRepoC.SOURCES_URLS, EuRepoC.ATTRIBUTION_SOURCES]:
            continue
        else:
            df = df.join(get_eurepoc_data(endpoint))
    
    df = df.reset_index() # reset index so incident_id can be used for aggregations
    return df
        

"""
Some best practices for working with EuRepoC data, uncomment if required.
"""

# creating a df with the full dataset, filtered by the minimum date EuRepOC added the incident
# this will only include incidents added after 01.02.2024 
df = get_full_eurepoc_dataset(pd.Timestamp(2024,2,1))
print(df.tail().status)

# simple aggregations dealing with the long format, here: get incident count of operation types by receiver country
    #dff = df.groupby(["operation_type", "receiver_country"])["incident_id"].nunique().reset_index() # use incident_id -> nunique to avoid duplicates

# there are also IDs for other blocks in our system, like attributions. Since one incident can have many attributions, we can use it to count attributions.
    #dff = df.groupby(["attributing_country"])["attribution_id"].nunique().reset_index() # use incident_id -> nunique to avoid duplicates

# because there are multiple attributions per incident, you can also remove duplicates by selecting the "settled" attribution
# this matters when you want to have one initiator country per incident, as there can be contested attributions!
    # df = df[df["settled_initiator"] == True]


# if you don't want the full dataset, recommended in most cases, here: only interested in receivers, initiators and operation types.
# This might be useful if you are only interested in who attacks whom how often, and how
    #df = get_eurepoc_data(EuRepoC.INCIDENTS)
    #df = df.join(get_eurepoc_data(EuRepoC.RECEIVERS))
    #df = df.join(get_eurepoc_data(EuRepoC.INITIATORS))


# creating a csv from the dataset
# it is recommended to filter the full data before saving, because the full long format dataframe is giant.
    #df.to_csv("eurepoc_dataset.csv")



"""
general hints:

Sometimes, a column can be NA, for some aggregations you need to df.dropna(subset="column")
The string Not available has a specific meaning: For example, when the receiver type is not known.
Unknown has another meaning: For example, when the country of an attributed threat actor is not known, the initiator country is Unknown.
Attribution fields can be: Not attributed.

_date columns always need to be converted to timestamps with pd.to_datetime(df.column, format="mixed") with mixed format required for attribution date
it can also happen that there are NAs for the dates, in that case you might want to drop or handle the NA rows

data quality: Status open means the incidents have only been processed by the morning team, this is Sent to database after the incident is fully coded. 
For questions looking into the details of political responses, you might want to use the Sent to database subset. 

"""


