import tabula
import pandas as pd
import PyPDF2
beaver = 'data\Beaver PA 2020 Primary PrecinctResults.pdf'#differnt then the others has fewer columns--guess=False--possibility
blair = 'data\Blair PA June 2 Elections Results.pdf'#a lot of nan columns
bradford = 'data\Bradford PA Primary SOVC_JUNEFINALREPORT.pdf'#really screwey--possibility
centre = 'data\Centre PA 2020 Primary.pdf'#empty columns/rows
cameron = 'data\CAMERON PA OFFICIAL CANVASS_6-2-20_PRECINCT SUMMARY.pdf'#doesnt open?

def HeaderFooterRemoval(dataframe,row_count):
    df.drop(df.tail(row_count).index,inplace=True)
    df.drop(df.head(row_count).index,inplace=True)

def StringVoteSplit(string,index):
    # try:
    #     # count = df.iloc[index]['Summary Results Report'].resplit(' ',1)
    # except:
    #     False

    count = df.loc[index]['Summary Results Report'].rsplit(' ',1)
    # print(type(count))
    return(count)
    
#67,71,75
data = tabula.read_pdf(beaver,guess=False,multiple_tables=True,pages=('67'))
pd.set_option('display.max_rows',None)
office_index = [0]
office=''
result = []
page=1
duplicate = True

for x in data:

    df = x

    # print(df)
    county = str(df.iloc[1,-1])
    HeaderFooterRemoval(x,2)
    df = df.reset_index(drop=True)
    df.dropna(axis='columns',how='all',inplace=True)
    precinct = str(df.iloc[0,0])

    df.drop([0],inplace=True)
    df = df.reset_index(drop=True)
    
    if len(df.columns)==3:
        df['Unnamed: 0'].fillna(df['Unnamed: 1'],inplace=True)
        df.drop(columns=['Unnamed: 1'],inplace=True)
    
    remove_strings=['Vote For 1','Vote For 8','TOTAL']
    remove_strings_list = df.index[df['Summary Results Report'].isin(remove_strings)].tolist()
    df = df.drop(df.index[remove_strings_list])
    df = df.reset_index(drop=True)

    if len(df.columns)==2:
        for x in df.index:
            if pd.isna(df.iloc[x,1]):
                try:
                    df.iloc[x,1] = float(StringVoteSplit(df.iloc[x,0],x)[-1])
                    df.iloc[x,0] = StringVoteSplit(df.iloc[x,0],x)[0]
                except:
                    pass
    if len(df.columns)==1:
        for x in df.index:
            if str(StringVoteSplit(df.iloc[x,0],x)[-1]):
                try:
                    df.loc[x,'Unnamed: 0'] = float(StringVoteSplit(df.iloc[x,0],x)[-1])
                    df.iloc[x,0] = StringVoteSplit(df.iloc[x,0],x)[0]
                except:
                    pass


    if str(df.iloc[0,0])=='STATISTICS':
        for x in df.index:
            df.loc[x,'county'] = county
            df.loc[x,'precinct'] = precinct
            if x>5:
                if 'DEM' in str(df.iloc[x,0]):
                    office_index.append(x)
                    office = df.iloc[x,0]
                df.loc[x,'office'] = office
                if 'REP' in str(df.iloc[x,0]):
                    office_index.append(x)
                    office = df.iloc[x,0]
                df.loc[x,'office'] = office
    else:
        for x in df.index:
            df.loc[x,'county'] = county
            df.loc[x,'precinct'] = precinct

            if 'DEM' in str(df.iloc[x,0]):
                office_index.append(x)
                office = df.iloc[x,0]
            df.loc[x,'office'] = office
            if 'REP' in str(df.iloc[x,0]):
                office_index.append(x)
                office = df.iloc[x,0]
            df.loc[x,'office'] = office

    df.drop(office_index,inplace=True)


    office_index=[]
    print(page)
    result.append(df)
    print(df)
    page +=1

pd.concat(result).to_csv('beaver_county.csv')
