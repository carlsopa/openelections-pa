import tabula
import pandas as pd
import argparse
# Both beaver & centre work for this initial idea.  Cameron does not result in anything, Bradford comes up NAN, and Blair is missing one result.
#Beaver has 2-4 columns, Blair has 4-6 columns, Bradford has 8-9 columns, Centre has 2-4 columns.  
#Bradford has to be dealt with seperatly from the others
#beaver, blair & centre all work the same

def Bradford_scrapper():
    print('Bradford')

def scrapper(party, county):
    files = {'Beaver': 'data\Beaver PA 2020 Primary PrecinctResults.pdf',
             'Blair': 'data\Blair PA June 2 Elections Results.pdf',
             'Bradford': 'data\Bradford PA Primary SOVC_JUNEFINALREPORT.pdf',
             'Cameron': 'data\CAMERON PA OFFICIAL CANVASS_6-2-20_PRECINCT SUMMARY.pdf',
             'Centre': 'data\Centre PA 2020 Primary.pdf'}
    result_pdf = files[county]
    page = 1

    data = tabula.read_pdf(result_pdf, guess=False,
                           multiple_tables=True, stream=True, pages=('1-10'))
    for x in data:
        df = x
        print(page)
        print(df)

        # if county !='Bradford':
        #     print('other county')
        # else:
        #     Bradford_scrapper()
        df = x
        # county = df.iloc[1, -1]
        page = page + 1


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--party", choices=["Dem", "Rep", "All"],
                    help="the party of choice to output: Dem,Rep,All.")
parser.add_argument("-c", "--county", choices=["Beaver", "Blair", "Bradford", "Cameron", "Centre"],
                    help="specify the county of choice for records: Beaver,Blair,Bradford,Cameron,Centre.")
args = parser.parse_args()
if(args.county and args.party != None):
    scrapper(args.party, args.county)
else:
    print('please enter both a party and county.  Type -h for more details.')
