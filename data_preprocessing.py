########   DATA PREPROCESSING   ########

import numpy as np
import pandas as pd

def data_prep():
    
    #READ ORGANICS FILE
    df = pd.read_csv('datasets/organics.csv')

    #AGE IMPUTATION
    df["DOB"] = pd.to_datetime(df["DOB"])
    df["EDATE"] = pd.to_datetime(df["EDATE"])
    df["AGE"] = df["EDATE"] - df["DOB"]
    df["AGE"] = pd.to_timedelta(df["AGE"])
    df["AGE"] = (df["AGE"] / np.timedelta64(1, 'D')).astype(int)//365

    #BILL VALUE CORRECTION
    mask = df["BILL"] < 1
    df.loc[mask, "BILL"] = np.nan
    df["BILL"].fillna(df["BILL"].mean(), inplace = True)

    #AFFL VALUE CORRECTION
    mask1 = (df["AFFL"] > 30) | ((df["AFFL"] < 1))
    df.loc[mask1, "AFFL"] = np.nan
    df["AFFL"].fillna(df["AFFL"].mean(), inplace = True)

    #CONVERTING NEIGHBORHOOD TO STRING 
    df["NEIGHBORHOOD"] = df["NEIGHBORHOOD"].astype(str)

    #DROP UNUSED ATTRIBUTE AND TARGET VARIABLE
    df.drop(["CUSTID", "GENDER", "DOB", "EDATE", "AGEGRP1", "AGEGRP2", "LCDATE", "ORGANICS"], axis = 1, inplace = True)

    #DROP THE ROWS WITH MISSING VALUE
    df = df.dropna(axis = 0, how = 'any')

    #ONE HOT ENCODING 
    df = pd.get_dummies(df)

    return df

	
def analyse_feature_importance(dm_model, feature_names, n_to_display=20):
    # grab feature importances from the model
    importances = dm_model.feature_importances_
    feature_names = X.columns
    # sort them out in descending order
    indices = np.argsort(importances)
    indices = np.flip(indices, axis = 0)

    # limit to 20 features, you can leave this out to print out everything
    indices = indices[:n_to_display]

    for i in indices:
        print(feature_names[i], ":", importances[i])
	   
	   
def visualize_decision_tree(dm_model, feature_names, save_name):
    import pydot
    from io import StringIO
    from sklearn.tree import export_graphviz
    
    dotfile = StringIO()
    export_graphviz(dm_model, out_file=dotfile, feature_names=feature_names)
    graph = pydot.graph_from_dot_data(dotfile.getvalue())
    graph.write_png(save_name) # saved in the following file