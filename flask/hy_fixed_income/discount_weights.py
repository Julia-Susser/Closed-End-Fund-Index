import os
import numpy as np
import pandas as pd
def hy_fixed_income_discount_weights(weights, index):
    final = pd.read_csv("hy_fixed_income/dataframes/final.csv", index_col=[0,1])

    df = pd.read_csv("hy_fixed_income/dataframes/Discount.csv", index_col=0)
    my_dir = os.listdir("./hy_fixed_income/funds")
    funds = list(map(lambda x: x.split(".")[0].upper(), my_dir))
    df = df[df.index.isin(funds)].iloc[:,:4]
    df = df.apply(lambda x: [x["Discount"].strip("%"),x["52W Discount"].strip("%"), x["Effective"].strip("%"), x["Distribution Rate"].strip("%")], axis=1, result_type='expand')
    df = df.replace("--",0)
    df.columns = ["Discount", "52W Discount", "Effective","Distribution"]
    df = df.astype('float')




    i = final.iloc[final.index.get_level_values(0) == index]

    #list(filter(lambda x: x not in list(i.index.get_level_values(1)), df.index))
    i.index = i.index.get_level_values(1)
    df = df.merge(i, how="outer", right_index=True, left_index=True).fillna(0)

    df = df.sort_values(by=["Weights"], ascending=False)
    df = df.round(3)

    if weights=="hey":
        df["Weights2"] = df["Weights"].round(4)
    else:
        w = []
        for x in df.index:
            w.append(float(weights[x]))
        df["Weights2"] = w

    df = df.reset_index()
    table = df.values.tolist()
    #df["Discount"].multiply(df["Weights"], axis=0).sum()
    discount = np.average(df["Discount"],weights=df.to_numpy()[:,-2])
    adjusted_discount = np.average(df["Discount"],weights=df.to_numpy()[:,-1])
    #adjusted_discount = (df["Discount"]*df["Weights2"]/df["Weights2"].sum()).sum()
    effective = round(np.average(df["Effective"],weights=df.to_numpy()[:,-2]),2)
    adjusted_effective = round(np.average(df["Effective"],weights=df.to_numpy()[:,-1]),2)

    distribution = round(np.average(df["Distribution"],weights=df.to_numpy()[:,-2]),2)
    adjusted_distribution = round(np.average(df["Distribution"],weights=df.to_numpy()[:,-1]),2)
    cef_data = {
        "discount": discount,
        "adjusted_discount": adjusted_discount,
        "effective":effective,
        "adjusted_effective":adjusted_effective,
        "distribution": distribution,
        "adjusted_distribution":adjusted_distribution
    }
    return table, cef_data
