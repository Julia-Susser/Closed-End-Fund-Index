
import xlrd
import os
import numpy as np
import pandas as pd

def path(y):
    global z
    if y == z:
        return "hey"
    global t
    for x in range(y,-1,-1):
        h = [x for x in range(y+1)]
        h.remove(x)
        t.append([x, h])
    path(y+1)
    if y == 0:
        return t
def change_down(weights, find, no_change_nums):
    k = [x + (.01/(len(weights)-len(no_change_nums)-1)) for x in weights[:find]+weights[find+1:]]
    k.insert(find, weights[find]-.01)
    for x in no_change_nums:
        k[x] = weights[x]
    return k


def change_up(weights, find, no_change_nums):
    k = [x - (.01/(len(weights)-len(no_change_nums)-1)) for x in weights[:find]+weights[find+1:]]
    k.insert(find, weights[find]+.01)
    for x in no_change_nums:
        k[x] = weights[x]
    negs = sum(list(filter(lambda x: max(x,0)==0, k)))
    zeros = list(filter(lambda x: max(k[x],0)==0, range(len(k))))
    for x in zeros:
        k[x] = 0
    zeros.append(find)
    not_zeros = list(filter(lambda x: x not in zeros, range(len(k))))
    for x in not_zeros:
        k[x] = k[x] + (negs/len(not_zeros))


    return k

def find(weights):
    global hf
    global sf
    global discount_df
    df = hf.multiply(weights).sum(axis=1).to_frame("ours")
    df = df.merge(sf, how="outer", right_on='Symbol', left_index=True)
    df = df.set_index("Symbol")
    #df = df.drop(["Symbol"], axis=1)
    df = df.fillna(0)
    w = [max(x,0) for x in weights]
    val = sum(discount_df['Discount_Weights'] * w)
    [max(x,0) for x in weights]
    close_val = sum(abs(df["ours"]-df["Weight"]))

    #close_val = sum([abs(5*x) if x < 0 else x for x in df["Weight"]-df["ours"]])
    #close_val = sum([ 5*x for x in filter(lambda x: x>0, df["ours"]-df["Weight"])])
    return close_val * val

def best(type, weights, ideal, ideal_weights):
    global no_change_nums
    global find_num
    num = find(weights)
    if num < ideal:
        if type == "up":
            if weights[find_num] + .01 > 0:
                return best("up",  change_up(weights, find_num, no_change_nums), num, weights)
            else:
                return weights
        if type == "down":
            if weights[find_num] - .01 > 0:
                return best("down", change_down(weights, find_num, no_change_nums), num, weights)
            else:
                return weights
    else:
        return ideal_weights





def go_through(weights):
    global hf
    global sf
    global no_change_nums
    global find_num
    num = find(weights)
    dw = change_down(weights, find_num, no_change_nums)
    uw = change_up(weights, find_num, no_change_nums)
    up = find(uw)
    down = find(dw)
    if up < down and up < num:
        return (best("up", uw,num, []))

    elif down < num:
        return best("down", dw,num, [])
    else:
        return weights

def equities_combo():
    print("doing")
    #os.chdir("/Users/jsusser/Desktop/code/funds/")
    global hf
    global sf
    global discount_df
    hf = pd.read_csv("./equities/dataframes/hf.csv", index_col=0)
    sf = pd.read_csv("./equities/dataframes/sf.csv", index_col=0)
    discount_df = pd.read_csv("./equities/dataframes/discount_df.csv", index_col=0)


    # In[89]:



    global t
    t = []
    global z
    z = len(hf.columns)-1




    way = path(0)
    len(way)






    # In[90]:
    global find_num
    global no_change_nums
    global weights
    weights = [1/len(hf.columns) for x in range(len(hf.columns))]
    n = 0
    for x in way:
        find_num = x[0]
        no_change_nums = x[1]

        weights = go_through(weights)

        n+=1



    # In[86]:


    def findy(weights):
        global hf
        global sf
        df = hf.multiply(weights).sum(axis=1).to_frame("ours")
        df = df.merge(sf, how="outer", right_on='Symbol', left_index=True)
        df = df.set_index("Symbol")
        #df = df.drop(["Symbol"], axis=1)
        df = df.fillna(0)
        val = sum(discount_df['Discount_Weights'] * weights)
        #close_val = sum(abs(df["ours"]-df["Weight"]))
        close_val = sum([abs(2*x) if x < 0 else x for x in df["Weight"]-df["ours"]])

    weights = [round(x,5) for x in weights]
    #weights = list(map(lambda x: max(x,0),weights))
    findy(weights)
    weights = [round(x,4) for x in weights]
    df = pd.DataFrame({"ticker":hf.columns, "weights": weights})
    #df = df[df["weights"] != 0]
    df = df.sort_values(by=['weights'], ascending=False)

    df.to_csv("./equities/dataframes/weights.csv", index=False)
