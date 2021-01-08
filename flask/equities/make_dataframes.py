import xlrd
import os
import numpy as np
import pandas as pd
def equities_make_dataframes():
    print("making frames")
    hf = pd.DataFrame({})
    #os.chdir("/Users/jsusser/Desktop/code/funds/")
    workbook = xlrd.open_workbook("./equities/Closed End Holdings 3.xlsx")

    names = workbook.sheet_names()
    for x in range(1,workbook.nsheets):
        sheet = workbook.sheet_by_index(x)
        df = pd.DataFrame([sheet.row_values(x) for x in range(1, sheet.nrows)])
        df.columns = df.iloc[0]
        df = df[1:]
        name = names[x]
        if name != "ead":
            df.to_csv("./equities/funds/"+name.upper()+".csv")


    # In[58]:


    hf = pd.DataFrame({})
    my_dir = os.listdir("equities/funds")


    for x in my_dir:
        if x == ".DS_Store":
            continue

        df = pd.read_csv("equities/funds/"+x)
        name = x.split(".csv")[0]
        cf = df["ID.WEIGHTS"].to_frame(name)
        cf.index = df.iloc[:,-1].replace(np.nan, "N/A")
        cf = cf.dropna(axis=0)
        na = cf[cf.index=="N/A"].astype('float').sum(axis=0)
        na += cf.iloc[cf.index.str[:4]=="#N/A"].sum(axis=0)
        cf = cf[(cf.index != "N/A") & (cf.index.str[:4]!="#N/A")]
        cf.loc["N/A"] = na
        cf = cf.groupby(level=0).sum()
        hf = hf.merge(cf, how='outer', left_index=True, right_index=True)


    hf = hf.fillna(0)

    #hf.index = pd.Series(hf.index).replace(np.nan, "N/A")
    #hf = hf.reindex(columns=["aod","adx","peo", "aio"])
    hf = hf.astype('float')
    hf = hf.div(hf.sum(), axis=1)*100
    sf = pd.read_csv("./equities/s&p500.csv")
    sf = sf[["Symbol","Weight"]]
    #https://www.slickcharts.com/sp500

    hf.to_csv("./equities/dataframes/hf.csv")
    sf.to_csv("./equities/dataframes/sf.csv")

    # In[59]:


    funds = hf.columns
    df = pd.read_csv("./equities/Discounts.csv", index_col=0)
    my_dir = os.listdir("./equities/funds")

    funds = list(map(lambda x: x.split(".")[0].upper(), my_dir))
    df = df[df.index.isin(funds)]
    df = df.iloc[:,1:3]


    df["Discount"] = list(map(lambda x: str(x).strip("%"), list(df["Discount"])))

    df["52W Discount"] = [0 if x=="--" else str(x).strip('%') for x in list(df["52W Discount"])]
    df = df.astype('float')
    df["Discount_Weights"] = ((df["Discount"] + (df["Discount"] - df["52W Discount"]))+100)/100
    discount_df = df[['Discount_Weights']]
    discount_df = df.reindex([x.upper() for x in hf.columns])
    discount_df.head()
    discount_df.to_csv("./equities/dataframes/discount_df.csv")
