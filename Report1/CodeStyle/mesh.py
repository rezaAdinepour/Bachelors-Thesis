"""
Classification ORL faces dataset using multilayer perceptron. In this program,
i first divided the data into train and test parts and started training on the 
train data. After that, i test the network using test data and show the results.
"""

import numpy as np
import torch
import os
import glob
import cv2
from sklearn.model_selection import train_test_split
from util import to_categorical, calculate_hog


def load_image_from_folder(PATH):
    labels = []
    folders = []
    for it in os.scandir(PATH):
        if it.is_dir():
            path = it.path
            folders.append(path)
            labels.append(int(path.split('s')[-1]) - 1)

    files_train = []
    files_test = []
    for folder in folders:
        files = []
        files.extend(glob.glob(folder+'/*.pgm'))
        paths_train, paths_test, _, _ = train_test_split(
            files, np.zeros(np.array(files).shape), test_size=0.4)
        files_train.append(paths_train)
        files_test.append(paths_test)

    return labels, files_train, files_test



def main():
    X_train, X_test, Y_train, Y_test = generate_data()

    model = Net()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_func = torch.nn.MSELoss()

    train(torch.tensor(X_train), torch.tensor(Y_train), torch.tensor(X_test), torch.tensor(Y_test), model, optimizer, loss_func, epochs=500)
    test(torch.tensor(X_test), torch.tensor(Y_test), model)


if __name__ == '__main__':
    main()