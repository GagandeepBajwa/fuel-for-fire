import numpy as np
import matplotlib.pyplot as plt
import os
import rasterio
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier

"""
This function taken from
https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
"""


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    # fig.tight_layout()
    return ax


"""
getData returns a list of the file names in the data folder.
"""


def getData(fp):
    # Specify the path to our data

    rasterBin = []
    for root, dirs, files in os.walk(fp, topdown=False):
        for file in files:
            if ".hdr" not in file:
                rasterBin.append(os.path.join(fp, file))

    print("files retrieved")
    return rasterBin


"""
Fill the data frame with data
"""


def populateDataFrame(rasterBin):
    data_frame = pd.DataFrame(columns=(
        'coastal_aerosol',
        'blue',
        'green',
        'red',
        'vre1',
        'vre2',
        'vre3',
        'nir',
        'narrow_nir',
        'water_vapour',
        'swir_cirrus',
        'swir2',
        'label_water_val',
        'label_water_bool',
        'label_river_val',
        'label_river_bool',
        'label_broadleaf_val',
        'label_broadleaf_bool',
        'label_shrub_val',
        'label_shrub_bool'))

    for raster in rasterBin:
        print(raster)
        if "S2A.bin_4x.bin_sub.bin" in raster:

            dataset = rasterio.open(raster)
            for idx in dataset.indexes:
                """
                reads in the current band which is a mat of 401, 410 and ravels it
                storing the result in the current column
                """
                data_frame.iloc[:, idx-1] = dataset.read(idx).ravel()

        elif "WATERSP.tif_project_4x.bin_sub.bin" in raster:
            water = rasterio.open(raster).read(1)
            data_frame['label_water_val'] = water.ravel()
            data_frame['label_water_bool'] = data_frame['label_water_val'] != 128

        elif "RiversSP.tif_project_4x.bin_sub.bin" in raster:
            river = rasterio.open(raster).read(1)
            data_frame['label_river_val'] = river.ravel()
            data_frame['label_river_bool'] = data_frame['label_river_val'] == 1.0

        elif "BROADLEAF_SP.tif_project_4x.bin_sub.bin" in raster:
            broadleaf = rasterio.open(raster).read(1)
            data_frame['label_broadleaf_val'] = broadleaf.ravel()
            data_frame['label_broadleaf_bool'] = data_frame['label_broadleaf_val'] == 1.0

        elif "SHRUB_SP.tif_project_4x.bin_sub.bin" in raster:
            shrub = rasterio.open(raster).read(1)
            data_frame['label_shrub_val'] = shrub.ravel()
            # yet to decode the shrub values boolean correspondance
    print(data_frame)
    return data_frame


"""
Undersample the data (take a subset of false pixels 
the same size as the true pixels)
"""


def getSample(data_frame, underSample, normalize):
    # get initial true and false for water
    X_true = data_frame[data_frame['label_water_bool'] == True]

    if underSample:
        X_false = data_frame[data_frame['label_water_bool']
                             == False].sample(len(X_true))

        undersample_water_frames = [X_true, X_false]

        # Concat the undersampled true and false pixels
        X_full = pd.concat(undersample_water_frames)
        X = X_full.loc[:, : 'swir2']  # only considers the columns up to swir2
        y = X_full['label_water_bool']

        # Normalize the data
        if normalize:
            scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
            X_norm = scaler.fit_transform(X)

            return X_norm, y
        else:
            return X, y
    else:


"""
        LIST OF THE AVAILABLE DATA

    # vri_s2_objid2.tif_project_4x.bin_sub.bin
    ## S2A.bin_4x.bin_sub.bin
    ## BROADLEAF_SP.tif_project_4x.bin_sub.bin
    ## WATERSP.tif_project_4x.bin_sub.bin
    # MIXED_SP.tif_project_4x.bin_sub.bin
    ## SHRUB_SP.tif_project_4x.bin_sub.bin
    # vri_s3_objid2.tif_project_4x.bin_sub.bin
    ## RiversSP.tif_project_4x.bin_sub.bin
    # L8.bin_4x.bin_sub.bin
    # CONIFER_SP.tif_project_4x.bin_sub.bin
    # HERB_GRAS_SP.tif_project_4x.bin_sub.bin
    # CCUTBL_SP.tif_project_4x.bin_sub.bin
    # EXPOSED_SP.tif_project_4x.bin_sub.bin
"""

if __name__ == "__main__":

    dataPath = "../data/"

    rasters = getData(dataPath)

    data_frame = populateDataFrame(rasters)
    class_names = ['water', 'not-water']
    X, y = getSample(data_frame, normalize=true)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=0, test_size=0.2)

    sgd_classifier = SGDClassifier(random_state=42, verbose=1, warm_start=True)
    y_pred = sgd_classifier.fit(X_train, y_train).predict(X_test)

    print("Test score: {:.2f}".format(sgd_classifier.score(X_test, y_test)))

    np.set_printoptions(precision=3)

    cm = confusion_matrix(y_test, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    truenegative, falsepositive, falsenegative, truepositive = confusion_matrix(
        y_test, y_pred).ravel()

    truenegnorm = truenegative / (truenegative + falsenegative)
    falseposnorm = falsepositive / (falsepositive + truepositive)
    falsenegnorm = falsenegative / (falsenegative + truenegative)
    trueposnorm = truepositive / (truepositive + falsepositive)

    print("Confusion Matrix\n", cm)
    print("True Negative", truenegnorm)  # land guessed correctly
    print("True Positive", trueposnorm)  # water guessed correctly
    print("False Negative", falsenegnorm)  # Land guessed as water
    print("False Positive", falseposnorm)  # Water guessed as land
    """
    # Plot non-normalized confusion matrix
    plot_confusion_matrix(y_test, y_pred, classes=class_names,
                          title='Confusion matrix, without normalization')

    # Plot normalized confusion matrix
    plot_confusion_matrix(y_test, y_pred, classes=class_names, normalize=True,
                          title='Normalized confusion matrix')
    plt.show()
    """
