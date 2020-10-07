import tabula
import pandas as pd
import numpy as np
import argparse
# Both beaver & centre work for this initial idea.  Cameron does not result in anything, Bradford comes up NAN, and Blair is missing one result.
#Beaver has 2-4 columns, Blair has 4-6 columns, Bradford has 8-9 columns, Centre has 2-4 columns.  
#Bradford has to be dealt with seperatly from the others
#beaver, blair & centre all work the same

def HeaderFooterRemoval(dataframe,row_count):
    dataframe.drop(dataframe.tail(row_count).index,inplace=True)
    dataframe.drop(dataframe.head(row_count).index,inplace=True)
    dataframe.dropna(subset=[dataframe.columns[0]],inplace=True)
def Bradford_scrapper():
    print('Bradford')

def scrapper(party, county):
    pd.set_option('display.max_colwidth',None)
    pd.set_option('display.max_columns',None)
    files = {'Beaver': 'data\Beaver PA 2020 Primary PrecinctResults.pdf',
             'Blair': 'data\Blair PA June 2 Elections Results.pdf',
             'Bradford': 'data\Bradford PA Primary SOVC_JUNEFINALREPORT.pdf',
             'Cameron': 'data\CAMERON PA OFFICIAL CANVASS_6-2-20_PRECINCT SUMMARY.pdf',
             'Centre': 'data\Centre PA 2020 Primary.pdf'}
    result_pdf = files[county]
    page = 1
    report_column_headers=['Candidate','Total','Vote %','Election Day','Absentee']
    remove_strings=['Vote For 1','Vote For 8','TOTAL','TOTAL VOTE %','Vote For 4','Election','Day','Vote For 3']
    data = tabula.read_pdf(result_pdf, guess=False,
                           multiple_tables=True, stream=True, pages=('1-600'))
    for x in data:
        df = x
        print(page)
        # print(df)
        # print('*******************')

        if county !='Bradford':
            county = df.iloc[1,-1]
            precinct = df.iloc[2,0]

            HeaderFooterRemoval(df,2)
            df.dropna(axis='columns',how='all',inplace=True)
            df = df.reset_index(drop=True)
            remove_strings_list = df.index[df.iloc[:,0].isin(remove_strings)].tolist()
            df = df.drop(df.index[remove_strings_list])
            df.dropna(axis='columns',how='all',inplace=True)
            #if 4 columns combine 1&2 on 1 nan
            #blair single column check for last char and split on ' '
            #if 3 columns combine 1&2 on nan
            df = df.reset_index(drop=True)
            var = len(df.columns)
            if var==1:
                print(df)
            elif var==2:
                # print(df)
                pass
            elif var==3:
                # print(df)
                pass

            
            elif var==4:
                # print(page)
                if 'OFFICIAL RESULTS' in df.columns:
                    # print(page)
                    # print(df)
                    # print('--------------------')
                    candidate = ''
                    vote = 0
                    percentage = ''
                    precinct = str(df.iloc[0,0])
                    race = ''
                    for x in df.index:
                        new = []
                        if df.iloc[x,0][-1] == '%':
                            candidate = df.iloc[x,0].rsplit(' ',2)[0]
                            vote = df.iloc[x,0].rsplit(' ',2)[1]
                            percentage = df.iloc[x,0].rsplit(' ',2)[2]
                        else:
                            if x > 0:
                                try:
                                    vote = int(df.iloc[x,0].rsplit(' ',1)[1])
                                    candidate = str(df.iloc[x,0].rsplit(' ',1)[0])
                                except:
                                    race = str(df.iloc[x,0].rsplit(' ',1)[0] + df.iloc[x,0].rsplit(' ',1)[1])
                                    candidate = np.nan
                                    percentage = ''
                        df.loc[x,report_column_headers[0]] = candidate
                        df.loc[x,report_column_headers[1]] = vote
                        df.loc[x,report_column_headers[2]] = percentage
                        df.rename(columns={'Unnamed: 0':'Election Day','Unnamed: 2':'Election Day','OFFICIAL RESULTS':'Absentee'},inplace=True)
                        df.loc[x,'precinct'] = precinct
                        df.loc[x,'race'] = race
                    df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                    df.drop(df.index[0],inplace=True)
                    df.dropna(subset=['Candidate'],inplace=True)
                    df = df.reset_index(drop=True)
                    # print(df)
                else:
                    vote = 0
                    candidate = ''
                    if str(df.iloc[1,0])=='STATISTICS':
                        found = False
                        precinct = df.iloc[0,0]
                        row_delete = []
                        df.drop(df.index[[0,1]],inplace=True)
                        df = df.reset_index(drop=True)                        
                        for index,row in df.iterrows():                            
                            if row.isnull().sum()==1 and found == False:
                                vote = df.iloc[index,0][-2:]
                                df.loc[index,'Unnamed: 0'] = df.iloc[index,0][-2:]
                                df.loc[index,'Summary Results Report'] = df.iloc[index,0][:-2]
                                found = True
                            if len(df.iloc[index,0].rsplit(' ',1)) == 1:
                                df.loc[index+1,'Unnamed: 1'] = df.iloc[index,0].rsplit(' ',1)[0]
                                row_delete.append(index)
                            else:
                                try:
                                    df.loc[index,'Unnamed: 0'] = int(df.iloc[index,0].rsplit(' ',1)[1])
                                    df.loc[index,'Summary Results Report'] = str(df.iloc[index,0].rsplit(' ',1)[0])
                                except:
                                    pass
                            if 'Ballots' in str(df.iloc[index,0].rsplit(' ',1)):
                                df.loc[index,'Unnamed: 1'] = df.loc[index,'Unnamed: 0']
                        df.drop(df.index[row_delete],inplace=True)
                        df.loc[14:len(df.index),'race'] = df.iloc[13,0]
                        df.drop(df.index[13],inplace=True)
                        df = df.reset_index(drop=True)
                        null_list = df.index[df['Unnamed: 0'].isnull()]
                        df.loc[null_list,'Unnamed: 0'] = df.loc[null_list,'Unnamed: 1'].shift(-1)
                        df.loc[14:len(df.index),'Unnamed: 2'] = df.loc[14:len(df.index),'Unnamed: 1']
                        df.loc[14:len(df.index),'Unnamed: 1'] = np.nan                       
                        df['precinct'] = precinct
                        df['Absentee'] = np.nan
                        df.rename(columns={'Summary Results Report':'Candidate','Unnamed: 0':'Total','Unnamed: 1':'Election Day','Unnamed: 2':'Vote %'},inplace=True)
                        df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                    else:
                        precinct = df.iloc[0,0]
                        race = df.iloc[1,0]
                        df.drop(df.index[[0,1]],inplace=True)
                        df = df.reset_index(drop=True)
                        df['Unnamed: 0'].fillna(df['Unnamed: 1'],inplace=True)
                        
                        df['precinct'] = precinct
                        df['Absentee'] = np.nan
                        df['race'] = race
                        
                        df.rename(columns={'Summary Results Report':'Candidate','Unnamed: 0':'Total','Unnamed: 1':'Election Day','Unnamed: 2':'Vote %'},inplace=True)
                        df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                # print(df)
            elif var==5:
                # print(df)
                pass


            # beaver 3 column:
            # if len(df.columns)==3:
            #     df['Unnamed: 0'].fillna(df['Unnamed: 1'],inplace=True)
            #     df.drop(columns=['Unnamed: 1'],inplace=True)
            #     print(df)


        else:
            Bradford_scrapper()
        county = df.iloc[1, -1]
        # print(df)
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
