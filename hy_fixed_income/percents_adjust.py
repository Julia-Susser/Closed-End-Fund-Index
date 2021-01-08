
import numpy as np
import pandas as pd

def hy_fixed_income_percents_adjust(weights, index):

    final = pd.read_csv("hy_fixed_income/dataframes/final.csv", index_col=[0,1])

    sf = pd.read_csv("hy_fixed_income/dataframes/sf.csv", index_col=0)
    hf = pd.read_csv("hy_fixed_income/dataframes/hf.csv", index_col=0)

    i = final.iloc[final.index.get_level_values(0) == index]
    hf2 = hf[i.index.get_level_values(1)]
    tf = hf2.multiply(list(i["Weights"])).sum(axis=1).to_frame("ours")

    tf = tf.merge(sf, how="outer", right_on='Symbol', left_index=True)
    if weights != "hey":
        w = []
        for x in hf.columns:
            w.append(float(weights[x]))
        df = hf.multiply(w).sum(axis=1).to_frame("adjusted")
        tf = df.merge(tf, how="outer", right_on='Symbol', left_index=True)
    else:
        tf["adjusted"] = tf["ours"]
    df = tf.drop(columns=["Symbol"]).fillna(0).loc[~(tf==0).all(axis=1)]

    tf = df[df['Weight']!=0]
    not_in_ours = df[df['Weight']==0]["ours"].sum()
    not_in_adjusted = df[df['Weight']==0]["adjusted"].sum()
    tf = tf.rename(columns={"Weight":"S&P500"})[["Ticker","ours", "adjusted", "S&P500"]]

    tf.loc["N/A"] = ["Not in the Index", not_in_ours, not_in_adjusted, 0]
    tf = tf.sort_values(by=['ours'], ascending=False).reset_index()


    tf["more_adjusted"] = tf["S&P500"] -tf["adjusted"]
    amount_more = str(round(abs(tf[tf["more_adjusted"]<0]["more_adjusted"]).sum()/(abs(tf[tf["more_adjusted"]<0]["more_adjusted"]).sum()+100)*100,2))
    amount_sp500 = str(round((100/(abs(tf[tf["more_adjusted"]<0]["more_adjusted"]).sum()+100))*100,2))
    amount_sp500_cef = str(round(((tf[tf["more_adjusted"]>=0]["adjusted"].sum()+tf[tf["more_adjusted"]<0]["S&P500"].sum())/(100))*100,2))
    amount_buy = str(round(tf[tf["more_adjusted"]>0]["more_adjusted"].sum()/(abs(tf[tf["more_adjusted"]<0]["more_adjusted"]).sum()+100)*100,2))
    amount_cef = str(round(tf["adjusted"].sum()/(abs(tf[tf["more_adjusted"]<0]["more_adjusted"]).sum()+100)*100,2))

    data_points_adjusted = {
        "amount_more": amount_more,
        "amount_sp500": amount_sp500,
        "amount_sp500_cef" : amount_sp500_cef,
        "amount_buy":amount_buy,
        "amount_cef": amount_cef
    }

    tf["more_ours"] = tf["S&P500"] -tf["ours"]
    amount_more = str(round(abs(tf[tf["more_ours"]<0]["more_ours"]).sum()/(abs(tf[tf["more_ours"]<0]["more_ours"]).sum()+100)*100,2))
    amount_sp500 = str(round((100/(abs(tf[tf["more_ours"]<0]["more_ours"]).sum()+100))*100,2))
    amount_sp500_cef = str(round(((tf[tf["more_ours"]>=0]["ours"].sum()+tf[tf["more_ours"]<0]["S&P500"].sum())/(100))*100,2))
    amount_buy = str(round(tf[tf["more_ours"]>0]["more_ours"].sum()/(abs(tf[tf["more_ours"]<0]["more_ours"]).sum()+100)*100,2))
    amount_cef = str(round(tf["ours"].sum()/(abs(tf[tf["more_ours"]<0]["more_ours"]).sum()+100)*100,2))

    data_points = {
        "amount_more": amount_more,
        "amount_sp500": amount_sp500,
        "amount_sp500_cef" : amount_sp500_cef,
        "amount_buy":amount_buy,
        "amount_cef": amount_cef
    }
    tf = tf.round(3)
    table = tf.drop(columns=["more_adjusted", "more_ours"])[["Ticker","ours", "adjusted", "S&P500"]].values.tolist()
    return table, data_points, data_points_adjusted
