import pandas as pd
file  = '/content/2019 monthly sales.xlsx'
xlsx=pd.ExcelFile(file)

for items in xlsx.sheet_names:
    if items=="GL Sales":
        df1=pd.read_excel(file,sheet_name="GL Sales", )
        # generic_query_PickedUp = generic_query.format(ClientName=str(self.client),FileName = str(file.split("/")[-1]),FileType = str(file.split('.')[-1]) ,ProcessingStage ='PreProcessing',Reason='',ReasonCode='',Status='PickedUp',TimeStamp = dt.datetime.now())                  
        query_job = client.query(generic_query_PickedUp)
        df1=df1.rename(columns={"Store Number":"Store_No","Store Name":"Store_Name"})
        df1.dropna(axis=1, how='all', thresh=20, subset= None, inplace=True)
        df1.dropna(axis=0, how='all', inplace=True)
#           df1.tail(10)
        df1=df1[df1["Store_No"].notnull()]
        df1=df1[df1.Store_No != "Grand Totals"]
        df1=df1[df1.Store_No != "Zip Totals"]
        df1=df1[df1.Store_No != "Variance "]
        df_GL=pd.melt(df1, id_vars=["Store_No","Store_Name"], value_vars=None,var_name="Sales_Date",value_name='Store_Sales_Ttl',col_level=None)
    else:
        df2=pd.read_excel(file,sheet_name="Zip totals")
        generic_query_PickedUp = generic_query.format(ClientName=str(self.client),FileName = str(file.split("/")[-1]),FileType = str(file.split('.')[-1]) ,ProcessingStage ='PreProcessing',Reason='',ReasonCode='',Status='PickedUp',TimeStamp = dt.datetime.now())                  
        query_job = client.query(generic_query_PickedUp)
        df2=df2.rename(columns={"Store Number":"Store_No","Store Name":"Store_Name"})
        df2.dropna(axis=1, how='all', thresh=20, subset= None, inplace=True)
        df2.dropna(axis=0, how='all', inplace=True)
        df2=df2[df2.Store_No != "Grand Totals"]
        df_Zp=pd.melt(df2, id_vars=["Store_No","Store_Name"], value_vars=None,var_name="Sales_Date",value_name="Store_Sales_ZipRollup")
# print(df_GL.info())
# print(df_Zp.info())
# print(df_GL.tail())
# print(df_Zp.tail())
df_final=pd.merge(df_GL, df_Zp, on=["Store_No", "Store_Name","Sales_Date"], how='left')
# print(df_final)

df_final["TF_Year"] = df_final['Sales_Date'].apply(lambda x: x.year)
df_final["TF_Month"] = df_final['Sales_Date'].apply(lambda x: x.month)
df_final = df_final.drop(columns="Sales_Date")
df_final = df_final.drop(columns='Store_Name')
#        print(df_final)
df_final['Source']=file.split('/')[-1].replace(".xlsx", "")
df_final['Ingestion_Timestamp'] = dt.datetime.now()  
if current_year_override is not None: 
    df_final.TF_Year =current_year_override


    