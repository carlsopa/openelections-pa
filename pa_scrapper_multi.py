import tabula
import pandas as pd
import numpy as np
import argparse
# Both beaver & centre work for this initial idea.  Cameron does not result in anything, Bradford comes up NAN, and Blair is missing one result.
#Beaver has 2-4 columns, Blair has 4-6 columns, Bradford has 8-9 columns, Centre has 2-4 columns.  
#Bradford has to be dealt with seperatly from the others
#beaver, blair & centre all work the same
report_column_headers=['Candidate','Total','Vote %','Election Day','Absentee']
page_result = []

def HeaderFooterRemoval(dataframe,row_count):
    dataframe.drop(dataframe.tail(row_count).index,inplace=True)
    dataframe.drop(dataframe.head(row_count).index,inplace=True)
    dataframe.dropna(subset=[dataframe.columns[0]],inplace=True)
def Bradford_scrapper():
    print('Bradford')

def seperator():
    print('------------------------------------')

def entry_split(dataframe):
    # print(dataframe)
    for x in dataframe.index:
        if(type(dataframe.iloc[x,1])==str):
            if (dataframe.iloc[x,1][-1]=='%')==False:
                # print(dataframe.iloc[x,0].rsplit(' ',3))
                candidate = dataframe.iloc[x,0].rsplit(' ',3)[0]
                total = dataframe.iloc[x,0].rsplit(' ',3)[1]
                vote_percentage = dataframe.iloc[x,0].rsplit(' ',3)[2]
                election_day = dataframe.iloc[x,0].rsplit(' ',3)[3]
                dataframe.rename(columns={'OFFICIAL RESULTS':'Absentee'},inplace=True)
                dataframe.loc[x,report_column_headers[0]] = candidate
                dataframe.loc[x,report_column_headers[1]] = total
                dataframe.loc[x,report_column_headers[2]] = vote_percentage
                dataframe.loc[x,report_column_headers[3]] = election_day
                # print(candidate)
            else:
                # print(dataframe.iloc[x,0].rsplit(' ',1))
                candidate = dataframe.iloc[x,0].rsplit(' ',1)[0]
                total = dataframe.iloc[x,0].rsplit(' ',1)[1]
                # print(dataframe.iloc[x,0].rsplit(' ',1)[0]e)
                dataframe.rename(columns={'Unnamed: 0':'Vote %'},inplace=True)
                dataframe.loc[x,report_column_headers[0]] = candidate
                dataframe.loc[x,report_column_headers[1]] = total
                dataframe.loc[x,report_column_headers[3]] = np.nan
                dataframe.loc[x,report_column_headers[4]] = np.nan
    dataframe = dataframe[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
    return dataframe

def two_entries(data):
    candidate = str(data[0])
    vote = int(data[1])
    return candidate, vote

def equals_value(data):
    a = data.to_numpy()
    return(a[0]==a).all()


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
    remove_strings=['Vote For 1','Vote For 8','TOTAL','TOTAL VOTE %','Vote For 4','Election','Day','Vote For 3']
    data = tabula.read_pdf(result_pdf, guess=False,
                           multiple_tables=True, stream=True, pages=('1-800'))
    for x in data:
        df = x
        if county !='Bradford':
            county = df.iloc[1,-1]
            precinct = df.iloc[2,0]

            HeaderFooterRemoval(df,2)
            df.dropna(axis='columns',how='all',inplace=True)
            df = df.reset_index(drop=True)
            remove_strings_list = df.index[df.iloc[:,0].isin(remove_strings)].tolist()
            df = df.drop(df.index[remove_strings_list])
            df.dropna(axis='columns',how='all',inplace=True)
            df = df.reset_index(drop=True)
            var = len(df.columns)
            if var==1:
                pass
            elif var==2:
                candidate = ''
                vote = 0
                percentage = 0
                print(page)
                removal_index = []
                precinct = df.iloc[0,0]
                race = df.iloc[1,0]
                df.drop(df.index[[0,1]],inplace=True)
                df = df.reset_index(drop=True)
                if str(df.iloc[0,1])[-1]=='%':
                    for x in df.index:
                        if isinstance(df.iloc[x,1],float) !=True:
                            candidate = two_entries(df.iloc[x,0].rsplit(' ',1))[0]
                            vote = two_entries(df.iloc[x,0].rsplit(' ',1))[1]
                            percentage = df.iloc[x,1]
                        else:
                            race = df.iloc[x,0]
                            removal_index.append(x)
                        df.loc[x,report_column_headers[0]] = candidate
                        df.loc[x,report_column_headers[2]] = percentage
                        df.loc[x,report_column_headers[1]] = vote
                        df.loc[x,report_column_headers[3]] = np.nan
                        df.loc[x,report_column_headers[4]] = np.nan
                        df.loc[x,'precinct'] = precinct
                        df.loc[x,'race'] = race
                    df.drop(df.index[removal_index],inplace=True)
                    df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]    
                else:
                    if df.iloc[0,1] == '0':
                        for x in df.index:
                            df.loc[x,report_column_headers[0]] = df.iloc[x,0].rsplit(' ',3)[0]
                            df.loc[x,report_column_headers[1]] = df.iloc[x,0].rsplit(' ',3)[1]
                            df.loc[x,report_column_headers[2]] = df.iloc[x,0].rsplit(' ',3)[2]
                            df.loc[x,report_column_headers[3]] = df.iloc[x,0].rsplit(' ',3)[3]
                            df.loc[x,report_column_headers[4]] = df.iloc[x,1]
                            df.loc[x,'precinct'] = precinct
                            df.loc[x,'race'] = race
                        df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                    else:
                        if df.iloc[0,1] == 'Absentee':
                            found = False
                            row_delete = []
                            df.drop(df.index[[0]],inplace=True)
                            df = df.reset_index(drop=True)
                            for index,row in df.iterrows(): 
                                result = df.iloc[index,0].rsplit(' ',1)   
                                if row.isnull().sum()==0:
                                    if len(result) > 1:
                                        candidate = result[0].replace(str(df.iloc[index,0].rsplit(' ',1)[1]),'')
                                        vote = result[1]
                                        result_length = len(vote)
                                        total, election_day = vote[:len(vote)//2],vote[len(vote)//2:]
                                        if total != election_day:
                                            election_day = vote
                                            total = result[0][-len(vote):]
                                        df.loc[index,report_column_headers[0]] = candidate
                                        df.loc[index,report_column_headers[1]] = total
                                        df.loc[index,report_column_headers[2]] = np.nan
                                        df.loc[index,report_column_headers[3]] = election_day
                                        df.loc[index,report_column_headers[4]] = df.iloc[index,1]
                                    else:
                                        election_day = df.iloc[index,0]
                                        absentee = df.iloc[index,1]
                                        df.loc[index,report_column_headers[2]] = np.nan
                                        df.loc[index+1,report_column_headers[3]] = election_day
                                        df.loc[index+1,report_column_headers[4]] = df.iloc[index,1]
                                        row_delete.append(index)
                                else:
                                    total = 0
                                    if str(df.iloc[index,0])[-1:]=='%':
                                        result = df.iloc[index,0].rsplit(' ',2)
                                        if len(result) > 1:
                                            df.loc[index,report_column_headers[0]] = result[0]
                                            df.loc[index,report_column_headers[1]] = result[1]
                                            df.loc[index,report_column_headers[2]] = result[2]
                                            pass
                                        else:
                                            total = result
                                            df.loc[index+1,report_column_headers[1]] = total
                                            df.loc[index+1,report_column_headers[0]] = df.iloc[index+1,0]
                                            row_delete.append(index)
                                            pass
                                    else:
                                        try:
                                            total = int(df.iloc[index,0].rsplit(' ',1)[1])
                                            candidate = str(df.iloc[index,0].rsplit(' ',1)[0])
                                            df.loc[index,report_column_headers[0]] = candidate
                                            df.loc[index,report_column_headers[1]] = total
                                        except:
                                            if 'Voter' in df.iloc[index,0]:
                                                df.loc[index,report_column_headers[0]] = df.iloc[index,0]
                                            else:
                                                race = df.iloc[index,0]
                                    df.loc[index,'race'] = race
                            df.drop(df.index[row_delete],inplace=True)
                        else:
                            df.drop(df.index[0],inplace=True)
                            df = df.reset_index(drop=True)
                            if equals_value(df.iloc[:,1]):
                                for x in df.index:
                                    df.loc[x,report_column_headers[0]] = df.iloc[x,0].rsplit(' ',3)[0]
                                    df.loc[x,report_column_headers[1]] = df.iloc[x,0].rsplit(' ',3)[1]
                                    df.loc[x,report_column_headers[2]] = df.iloc[x,0].rsplit(' ',3)[2]
                                    df.loc[x,report_column_headers[3]] = df.iloc[x,0].rsplit(' ',3)[3]
                                    df.loc[x,report_column_headers[4]] = df.iloc[x,1]
                                    df.loc[x,'precinct'] = precinct
                                    df.loc[x,'race'] = race
                                df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                            else:
                                secondary_race = df.iloc[3,0]
                                remove_list = df.index[df[df.columns[0]].isin(['TOTAL VOTE % Absentee','Vote For 2'])].tolist()
                                df.drop(df.index[remove_list],inplace=True)
                                df.drop(df.index[3],inplace=True)
                                df = df.reset_index(drop=True)
                                for x in df.index:
                                    try:
                                        vote = int(df.iloc[x,0].rsplit(' ',3)[1])
                                        candidate = df.iloc[x,0].rsplit(' ',3)[0]
                                        percentage = df.iloc[x,0].rsplit(' ',3)[2]
                                        election_day = df.iloc[x,0].rsplit(' ',3)[3]
                                    except:
                                        candidate = df.iloc[x,0].rsplit(' ',3)[0] + df.iloc[x,0].rsplit(' ',3)[1]
                                        vote = int(df.iloc[x,0].rsplit(' ',3)[2])
                                        percentage = df.iloc[x,0].rsplit(' ',3)[3]
                                        election_day = np.nan
                                    df.loc[x,report_column_headers[0]] = candidate
                                    df.loc[x,report_column_headers[1]] = vote
                                    df.loc[x,report_column_headers[2]] = percentage
                                    df.loc[x,report_column_headers[3]] = election_day
                                    df.loc[x,report_column_headers[4]] = absentee
                                    df.loc[x,'precinct'] = precinct
                                    if x <= 2:
                                        df.loc[x,'race'] = race
                                    else:
                                        df.loc[x,'race'] = secondary_race
                                df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                page_result.append(df)
            elif var==3:
                pass
            elif var==4:
                candidate = ''
                vote = 0
                percentage = ''
                election_day = 0
                absentee = 0
                precinct = str(df.iloc[0,0])
                race = ''
                if 'OFFICIAL RESULTS' in df.columns:                    
                    df[df.columns[1]].fillna(df[df.columns[2]],inplace=True)
                    for x in df.index:
                        new = []
                        if df.iloc[x,0][-1] == '%':
                            candidate = df.iloc[x,0].rsplit(' ',2)[0]
                            vote = df.iloc[x,0].rsplit(' ',2)[1]
                            percentage = df.iloc[x,0].rsplit(' ',2)[2]
                            election_day = df.iloc[x,1]
                            absentee = df.iloc[x,3]
                        else:
                            if x > 0:
                                try:
                                    candidate = two_entries(df.iloc[x,0].rsplit(' ',1))[0]
                                    vote = two_entries(df.iloc[x,0].rsplit(' ',1))[1]
                                    percentage = df.iloc[x,1]
                                    election_day = df.iloc[x,2]
                                    absentee = df.iloc[x,3]
                                except:
                                    race = str(df.iloc[x,0].rsplit(' ',1)[0] + df.iloc[x,0].rsplit(' ',1)[1])
                                    candidate = np.nan
                                    percentage = ''
                        df.loc[x,report_column_headers[0]] = candidate
                        df.loc[x,report_column_headers[1]] = vote
                        df.loc[x,report_column_headers[2]] = percentage
                        df.loc[x,report_column_headers[3]] = election_day
                        df.loc[x,report_column_headers[4]] = absentee
                        df.loc[x,'precinct'] = precinct
                        df.loc[x,'race'] = race
                    df = df[['Candidate','precinct','race','Total','Vote %','Election Day','Absentee']]
                    df.drop(df.index[0],inplace=True)
                    df.dropna(subset=['Candidate'],inplace=True)
                    df = df.reset_index(drop=True)
                else:
                    if str(df.iloc[1,0])=='STATISTICS':
                        found = False
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
                                df.loc[index+1,'Unnamed: 0'] = df.iloc[index,0].rsplit(' ',1)[0]
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
                        df = df.reset_index(drop=True)
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
                        df['Unnamed: 0'].fillna(df['Unnamed: 1'],inplace=True)
                        df.drop(df.index[[0,1]],inplace=True)
                        df.drop(columns=['Unnamed: 1'])
                        df = df.reset_index(drop=True)
                        df['precinct'] = precinct
                        df['Absentee'] = np.nan
                        df['race'] = race
                        
                        df.rename(columns={'Summary Results Report':'Candidate','Unnamed: 0':'Total','Unnamed: 2':'Vote %'},inplace=True)
                        df = df[['Candidate','precinct','race','Total','Vote %','Absentee']]
                page_result.append(df)
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
        page +=1
    pd.concat(page_result).to_csv('multi_county.csv')


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
