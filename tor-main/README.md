 
sudo pip install stem
pip install beautifulsoup4
pip3 install confluent-kafka
pip3 install msgpack
need docker compose
pip install networkx[default]

findData
    After data is downloaded, use this to calculate number of unique IP addresses of 
    tor relays, the unique number of ASes contaning those relays, and their bandwidth options 
    Same as running both unique_AS and unique_Tor
    ./findData {startMonth} {startYear} {endMonth} {endYear} {bandwidth: bool} 

downloadData
    Downloads and unzips all necessary data for findData from Consensus and Caida
    ./findData {startMonth} {startYear} {endMonth} {endYear}
    
unique_AS:
    Use to create list of unique ASes per month stored under file 
    data/formatted/asLists/sortedListOfAS-startYearstartMonth-endYearendMonth.txt
    ./unique_AS startMonth startYear endMonth endYear

unique_Tor:
    Code to find number of unique IP addresses of tor over 24 hours of first day 
    of month
    Downloads datasets from the torproject, downloads IP to AS mapping data from caida 
    creates list of unique tor IPs
    create tree of ASes with sortTree.py and search for each IP's AS, returns ASes
    .unique_Tor startMonth startYear endMonth endYear
    Stored under uniqueTorIP-startYearstartMonth-endYearendMonth.txt

findTor_Parallel.py
    python3 findTor_Parallel.py -s 4 2022 -b true
        If you have data in data/formatted/torIPLists
        -s for start date (month year)
        -e for end date (month year)
        -b for bandwidth (true/false)

findURL.py
    Returns end of URL to unique_Tor.py so it can download IP to AS mappings from caida.

sortTree_parallel.py
    Downloads data from caida, creates a tree of ASes in binary form, then searches for the as
    assosiated with an IP address found in findTor_Parallel.py. saves this data to
    "data/formatted/asLists/listOfAS-%s-%s"

    python3 sortTree_Parallel.py -s 4 2022 -b true
        If you have data in data/formatted/torIPLists
        -s for start date (month year)
        -e for end date (month year)
        -b for bandwidth (true/false)

Graphs/createPlot.py
    python3 createPlot.py
    creates plot of unique Tor IPs, unique Tor ASes, and unique ASes based on saved data from 11 2007 to 8 2021 found using unique_Tor and unique_AS

kafka/BGP_parallel.py
    python3 findTor_Parallel.py -s 4 2022 -b true
        If you have data in data/formatted/torIPLists
        -s for start date (month year)
        -e for end date (month year)
        -b for bandwidth (true/false)
    Uses BGPStream to get As paths and sends these through kafka. 
    Reads from data/formatted/asLists/sortedListOfAS-
    if bandwidth == True, it sends object through
    use with consumer.py

consumer.py
    Uses confluent kafka to receive messages contaning a AS number and paths given in BGP that
    originate from this ASN then saves this to json.