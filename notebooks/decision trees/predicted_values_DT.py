# import numpy package for arrays and stuff 
import numpy as np 

# import matplotlib.pyplot for plotting our result 
import matplotlib.pyplot as plt 

# import pandas for importing csv files 
import pandas as pd 

#decision tree-based models for regression 
from sklearn.tree import DecisionTreeRegressor

#x_ref is a vector of type np.array([[value_ref1,value_ref2,...]]
#df_X is the input column or matrix of a dataframe 
#df_y is the output column of dataframe


def DT_handling(df_X,df_y,crits,dist=1000):
    # we call the x values of the dataframe
    df_X=pd.DataFrame(df_X) 
    df_y=pd.DataFrame(df_y) 
    xy = pd.concat([df_X,df_y],axis=1)# concatenate columns x and y
    sorted_xy=xy.drop_duplicates(subset=df_X.columns)
    sorted_xy.columns=range(len(xy.columns))
        
    df1=pd.DataFrame([]) # save new extra points for criteria of next or previous

    for i in range(len(df_X.columns)):
        if crits[i]=='next':# if argument is next
            #x axis
            sorted_xy=sorted_xy.sort_values(sorted_xy.columns[i], ascending = True)
            C=(np.vstack((sorted_xy.iloc[:,i]-sorted_xy.iloc[:,i].min()/dist,sorted_xy.iloc[:,i]+sorted_xy.iloc[:,i].min()/dist)).ravel('F'))#create a sequence of supplementary points  
            D=np.repeat(C, 2) #repeat each element of the column twice
            df_X_Next=np.column_stack(D[:-2]).reshape(-1,1)#convert an array in column

            #axis y    
            t=len(sorted_xy.columns)-len(df_y.columns)
            df_y1 = sorted_xy.iloc[:,t:]
            df_y1_C1 = df_y1-df_y1.min()/dist
            df_y1_C2 = df_y1+df_y1.min()/dist
            A=df_y1_C1.loc[df_y1_C1.index.repeat(2)].reset_index(drop=True)
            B=df_y1_C2.loc[df_y1_C2.index.repeat(2)].reset_index(drop=True)
            C=pd.concat([A, B]).sort_index(kind='merge')
            C=C.drop(C.index[[2,3]])
            df_y_Next=(C)
            df_y_Next=df_y_Next.reset_index(drop=True)     

            #rest of independent axis
            df_X_rest=sorted_xy.iloc[:,:len(df_X.columns)]# select the columns of X
            df_X_rest=df_X_rest.iloc[:, df_X_rest.columns != df_X_rest.columns[i]] #skip selected column
            df_X_rest=pd.concat([df_X_rest]*4).sort_index().iloc[2:] #repeat the rows 4 times and delete the first two ones
            df_X_rest=df_X_rest.reset_index(drop=True)
            df_X_rest.insert(i, sorted_xy.columns[i], df_X_Next)  #insert the column of dataframe in df_X_rest

            #Concatenate the new supplementary points together into a dataframe
            extra_pts=pd.concat([df_X_rest,df_y_Next],axis=1)
            df1=df1.append(extra_pts)

        if crits[i]=='previous':# if argument is previous    
            #x axis
            sorted_xy=sorted_xy.sort_values(sorted_xy.columns[i], ascending = True)
            C=(np.vstack((sorted_xy.iloc[:,i]-sorted_xy.iloc[:,i].min()/dist,sorted_xy.iloc[:,i]+sorted_xy.iloc[:,i].min()/dist)).ravel('F'))
            D=np.repeat(C, 2)
            df_X_Prev=np.column_stack(np.delete(np.delete(D,2),2)).reshape(-1,1)#convert an array in column

            #axis y    
            t=len(sorted_xy.columns)-len(df_y.columns)
            df_y1 = sorted_xy.iloc[:,t:]
            df_y1_C1 = df_y1-df_y1.min()/dist
            df_y1_C2 = df_y1+df_y1.min()/dist
            A=df_y1_C1.loc[df_y1_C1.index.repeat(2)].reset_index(drop=True)
            B=df_y1_C2.loc[df_y1_C2.index.repeat(2)].reset_index(drop=True)
            C=pd.concat([A, B]).sort_index(kind='merge')
            df_yPrev=(C[:-2])
            df_yPrev=df_yPrev.reset_index(drop=True)     

            #rest of independent axis
            df_X_rest=sorted_xy.iloc[:,:len(df_X.columns)]# select the columns of X
            df_X_rest=df_X_rest.iloc[:, df_X_rest.columns != df_X_rest.columns[i]] #skip selected column
            df_X_rest=pd.concat([df_X_rest]*4).sort_index().iloc[:-2] #repeat the rows 4 times and delete the first two ones
            df_X_rest=df_X_rest.reset_index(drop=True)
            df_X_rest.insert(i, sorted_xy.columns[i], df_X_Prev)  #insert the column of dataframe in df_X_rest

            #Concatenate the new supplementary points together into a dataframe
            extra_pts=pd.concat([df_X_rest,df_yPrev],axis=1)
            df1=df1.append(extra_pts)

#     sorted_xy.columns = df1.columns
    sorted_xy= df1.append(sorted_xy)
    df_X=sorted_xy.iloc[:,:len(df_X.columns)]
    df_y=sorted_xy.iloc[:,len(df_X.columns):]

    # create a regressor object (https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html)
    regressor = DecisionTreeRegressor(criterion='mse', max_depth=None, max_features=len(df_X.columns),
               max_leaf_nodes=len(df_X), min_impurity_decrease=0.0,
               min_impurity_split=None, min_samples_leaf=1,
               min_samples_split=2, min_weight_fraction_leaf=0.0,
               random_state=None, splitter='best')

    # fit the regressor with X and Y data 
    return regressor.fit(df_X, df_y) 

