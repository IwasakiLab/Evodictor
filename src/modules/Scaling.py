# import modules
from sklearn import preprocessing

def normalization(X_array, normalize):

    if (normalize == 'standard' ):

        scaler = preprocessing.StandardScaler()
        normed_X_array = scaler.fit_transform(X_array)

    elif (normalize == 'minmax' ):

        scaler = preprocessing.MinMaxScaler()
        normed_X_array = scaler.fit_transform(X_array)
    
    return normed_X_array