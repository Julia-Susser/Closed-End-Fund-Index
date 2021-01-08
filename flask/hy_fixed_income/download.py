
import numpy as np
import pandas as pd

def hy_fixed_income_download(weights):

    df = pd.read_csv("hy_fixed_income/dataframes/weights.csv", index_col=0)
    sf = pd.read_csv("hy_fixed_income/dataframes/sf.csv", index_col=0)
    hf = pd.read_csv("hy_fixed_income/dataframes/hf.csv", index_col=0)
    discount_df = pd.read_csv("hy_fixed_income/dataframes/discount_df.csv")
    w = []
    for x in df.index:
        w.append(float(weights[x]))
    hf2 = hf[df.index]
    hf = hf2.multiply(w).sum(axis=1).to_frame("ours")
    hf = hf.merge(sf, how="outer", right_on='Symbol', left_index=True)
    hf = hf.set_index("Symbol")
    hf = hf.fillna(0)
    hf = hf.loc[~(hf==0).all(axis=1)]
    tf = hf[hf['Weight']!=0]
    not_in = hf[hf['Weight']==0]["ours"].sum()
    tf = tf.rename(columns={"Weight":"S&P500"})

    i = pd.DataFrame([[not_in, 0]], ["notINs&p500"], columns=["ours","S&P500"])
    tf = tf.append(i)
    tf = tf.sort_values(by=['ours'], ascending=False)



    tf = tf.reset_index()




    tf["more"] = tf["S&P500"] -tf["ours"]

    amount_buy = tf[tf["more"]>0][["index", "more"]]
    amount_buy = amount_buy.set_index("index")
    amount_buy.columns = ["weights"]

    df["weights"] = w
    df["weights"] = df["weights"] *100

    df = pd.concat([df, amount_buy])

    df["weights"] = df["weights"]/df["weights"].sum()
    df = df.loc[~(df==0).all(axis=1)]
    df = round(df*100,3)
    df.to_csv("./hy_fixed_income/dataframes/download.csv")
    tf = tf.round(3)
    table = tf.drop(columns=["more"]).values.tolist()
    return ""
