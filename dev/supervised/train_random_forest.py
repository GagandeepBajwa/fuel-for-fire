from Utils.Helper import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ## TUNING
    class_to_train = 'shrub'
    number_of_estimators = 46
    # 23 features here, reduce the number of features each tree will see
    max_features = 4

    ## DATA WRANGLE
    data = Helper.init_data()
    print(data.Target.keys())
    X = data.Combined.Data()
    y = data.Target[class_to_train].Binary
    print("X Shape:", X.shape)
    print("y Shape:", y.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    ## not necessary to center here
    # mean_vals, std_val = Helper.mean_center_normalize(X_train)

    # X_train_centered = (X_train - mean_vals) / std_val
    # X_test_centered = (X_test - mean_vals) / std_val

    # n jobs uses all the available cores
    forest = RandomForestClassifier(n_estimators=number_of_estimators,
                                    random_state=2,
                                    max_features=max_features,
                                    n_jobs=-1)

    forest.fit(X_train, y_train)

    print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
    print("Accuracy on testing set: {:.3f}".format(forest.score(X_test, y_test)))
