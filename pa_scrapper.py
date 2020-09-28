import tabula
import pandas as pd
import PyPDF2

def HeaderFooterRemoval(dataframe,row_count):
    df.drop(df.tail(row_count).index,inplace=True)
    df.drop(df.head(row_count).index,inplace=True)

def StringVoteSplit(string,index):
    count = df.loc[index]['Summary Results Report'].rsplit(' ',1)
    return(count)
#function created for the odd instance where all the data is placed into column header, instead of actual tables.  An example of this issue can be seen on pages: 67 & 71 amongst others.
def ColumnHeaderSplit(dataframe):
    lst = dataframe.columns.str.split('\r').tolist()
    collector = False
    summary_results = []
    official_results = []
    #manually entering data into a newly created so that it will work further down the line.
    summary_results.append(lst[0][1])
    official_results.append('')
    summary_results.append('June 2, 2020')
    official_results.append('Beaver County')
    summary_results.append(lst[0][3])
    official_results.append('')
    #going through the list I only need the data that is between two sets of data.  The for loop will go through my list and look for those specific sets to pull the data out.
    for x in lst[0]:
        if x == 'TOTAL':
            collector = True
        if 'DEM ALT DEL' in x:
            collector = False
        if collector:
            index = 1
            while x[-index].isdigit():
                index = index+1
            summary_results.append(x[:-index+1])
            official_results.append(x[-index+1:])
    data = {'Summary Results Report':summary_results,'Unnamed: 0':official_results}
    return(pd.DataFrame(data=data))

#set different variables for the output
pd.set_option('display.max_rows',None)
office_index = [0]
office=''
result = []
#the page number to start with 
first_page=1
last_page = 1009
page = first_page
duplicate = True


#start

while page<=last_page:
    
    data = tabula.read_pdf(centre,guess=False,multiple_tables=True,pages=(page))
    x = data[0]
    # print(x)
#determine if all the data is inside the row header
    if len(x)!=1:
        df = x
    else:
        df = ColumnHeaderSplit(x)
    
    county = str(df.iloc[1,-1])
    HeaderFooterRemoval(df,2)
    df = df.reset_index(drop=True)
    df.dropna(axis='columns',how='all',inplace=True)
    precinct = str(df.iloc[0,0])
    df.drop([0],inplace=True)
    df = df.reset_index(drop=True)  
    #check the number of columns, based on the amount of columns, the corresponding data was formatted differently.  
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
    #if the data 'STATISTICS' is in the data set, treat it differently
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
    df.drop(df.index[0])
    df.drop(df[df['Summary Results Report']==''].index, inplace=True)
    df.drop(df[df['Summary Results Report']=='STATISTICS'].index, inplace=True)
    df.drop(df[df['Summary Results Report']=='Vote For'].index, inplace=True)
    df = df.reset_index(drop=True)
    print(page)
    office_index=[]
    result.append(df)
    page +=1
pd.concat(result).to_csv('blair_county.csv')
