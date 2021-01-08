
import numpy as np
import pandas as pd
def equities_percents():
    df = pd.read_csv("./equities/dataframes/weights.csv", index_col=0)
    sf = pd.read_csv("equities/dataframes/sf.csv", index_col=0)
    hf = pd.read_csv("equities/dataframes/hf.csv", index_col=0)
    discount_df = pd.read_csv("equities/dataframes/discount_df.csv")

    funds = hf.columns



    hf2 = hf[df.index]


    df = hf2.multiply(df["weights"]).sum(axis=1).to_frame("ours")
    df = df.merge(sf, how="outer", right_on='Symbol', left_index=True)
    df = df.set_index("Symbol")
    df = df.fillna(0)
    df = df.loc[~(df==0).all(axis=1)]
    tf = df[df['Weight']!=0]
    not_in = df[df['Weight']==0]["ours"].sum()
    tf = tf.rename(columns={"Weight":"S&P500"})

    i = pd.DataFrame([[not_in, 0]], ["notINs&p500"], columns=["ours","S&P500"])
    tf = tf.append(i)
    tf = tf.sort_values(by=['ours'], ascending=False)



    tf = tf.reset_index()



    tf["more"] = tf["S&P500"] -tf["ours"]
    amount_more = str(round(abs(tf[tf["more"]<0]["more"]).sum()/(abs(tf[tf["more"]<0]["more"]).sum()+100)*100,2))
    amount_sp500 = str(round((100/(abs(tf[tf["more"]<0]["more"]).sum()+100)),2))
    #amount_not_in_sp500 = tf.loc["notINs&p500"]["ours"]/(abs(tf[tf["more"]<0]["more"]).sum()+100)+tf.loc["notINs&p500"]["ours"]
    amount_sp500_cef = str(round(((tf[tf["more"]>=0]["ours"].sum()+tf[tf["more"]<0]["S&P500"].sum())/(100))*100,2))
    amount_buy = str(round(tf[tf["more"]>0]["more"].sum()/(abs(tf[tf["more"]<0]["more"]).sum()+100)*100,2))
    amount_cef = str(round(tf["ours"].sum()/(abs(tf[tf["more"]<0]["more"]).sum()+100)*100,2))


    amount_more2 = str(round(abs(tf[tf["more"]<0]["more"]).sum(),2))
    amount_sp5002 = str(100)
    #amount_not_in_sp500 = tf.loc["notINs&p500"]["ours"]/(abs(tf[tf["more"]<0]["more"]).sum()+100)+tf.loc["notINs&p500"]["ours"]
    amount_sp500_cef2 = str(round((tf[tf["more"]>=0]["ours"].sum()+tf[tf["more"]<0]["S&P500"].sum())/(100)*100,2))
    amount_buy2 = str(round(tf[tf["more"]>0]["more"].sum(),2))
    amount_cef2 = str(round(tf["ours"].sum(),2))
    tf = tf.round(3)
    table = tf.drop(columns=["more"]).values.tolist()
    return table, [amount_more, amount_sp500, amount_buy, amount_cef, amount_sp500_cef], [amount_more2, amount_sp5002, amount_buy2, amount_cef2, amount_sp500_cef2]
