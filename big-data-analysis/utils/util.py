import json
from pathlib import Path
from collections import OrderedDict
from itertools import repeat
import pandas as pd
import os
import numpy as np
from glob import glob
import math

def load_folds_data_shhs(np_data_path, n_folds):
    files = sorted(glob(os.path.join(np_data_path, "*.npz")))
    r_p_path = r"utils/r_permute_shhs.npy"
    r_permute = np.load(r_p_path)
    npzfiles = np.asarray(files , dtype='<U200')[r_permute]
    train_files = np.array_split(npzfiles, n_folds)
    folds_data = {}
    for fold_id in range(n_folds):
        subject_files = train_files[fold_id]
        training_files = list(set(npzfiles) - set(subject_files))
        folds_data[fold_id] = [training_files, subject_files]
    return folds_data

def load_folds_data(np_data_path, n_folds):
    files = sorted(glob(os.path.join(np_data_path, "*.npz")))
    if "78" in np_data_path:
        r_p_path = r"utils/r_permute_78.npy"
    else:
        r_p_path = r"utils/r_permute_20.npy"

    if os.path.exists(r_p_path):
        r_permute = np.load(r_p_path)
    else:
        print ("============== ERROR =================")


    files_dict = dict()
    for i in files:
        file_name = os.path.split(i)[-1] 
        file_num = file_name[3:5]
        if file_num not in files_dict:
            files_dict[file_num] = [i]
        else:
            files_dict[file_num].append(i)
    files_pairs = []
    for key in files_dict:
        files_pairs.append(files_dict[key])
    files_pairs = np.array(files_pairs)
    files_pairs = files_pairs[r_permute]

    train_files = np.array_split(files_pairs, n_folds)
    folds_data = {}
    for fold_id in range(n_folds):
        subject_files = train_files[fold_id]
        subject_files = [item for sublist in subject_files for item in sublist]
        files_pairs2 = [item for sublist in files_pairs for item in sublist]
        training_files = list(set(files_pairs2) - set(subject_files))
        folds_data[fold_id] = [training_files, subject_files]
    return folds_data

def load_folds_data_custom(np_data_path, n_folds):
    files = sorted(glob(os.path.join(np_data_path, "*.npz")))
    
    r_permute = np.random.RandomState(seed=20220926).permutation(23)

    files_dict = dict()
    for i in files:
        file_name = os.path.split(i)[-1] 
        file_num = file_name[14:17]
        if file_num not in files_dict:
            files_dict[file_num] = [i]
        else:
            files_dict[file_num].append(i)
    files_pairs = []
    for key in files_dict:
        files_pairs.append(files_dict[key])
    files_pairs = np.array(files_pairs)
    files_pairs = files_pairs[r_permute]

    train_files = np.array_split(files_pairs, n_folds)
    folds_data = {}
    for fold_id in range(n_folds):
        subject_files = train_files[fold_id]
        subject_files = [item for sublist in subject_files for item in sublist]
        files_pairs2 = [item for sublist in files_pairs for item in sublist]
        training_files = list(set(files_pairs2) - set(subject_files))
        folds_data[fold_id] = [training_files, subject_files]
    return folds_data


def calc_class_weight(labels_count, method = None):
    total = np.sum(labels_count)
    class_weight = dict()
    num_classes = len(labels_count)
    # for key in range(num_classes):
    #     if method == "Log":
    #         score = math.log(total / float(labels_count[key]))
    #     elif method == "Scale":
    #         score = 1 - float(labels_count[key]/total)    
    #     else:
    #         score = 1.
    #     class_weight[key] = score        

    # class_weight = [class_weight[i] for i in range(num_classes)]
    if num_classes == 3:
        class_weight = [1.5, 1, 1.5]
    elif num_classes == 4:
        class_weight = [1.5, 1, 1.5, 1.5]
    elif num_classes == 5:
        class_weight = [1.5, 1, 1.5, 1.5, 1.5]
    return class_weight

# def calc_class_weight(labels_count, method = None):
#     total = np.sum(labels_count)
#     class_weight = dict()
#     num_classes = len(labels_count)

#     factor = 1 / num_classes

#     for key in range(num_classes):
#         score = 1 - float(labels_count[key]/total)  
#         class_weight[key] = score #if score > 1.0 else 1.0
#         class_weight[key] = round(class_weight[key] * factor, 2)

#     class_weight = [class_weight[i] for i in range(num_classes)]
#     print(class_weight)
#     return class_weight

# def calc_class_weight(labels_count):
#     total = np.sum(labels_count)
#     class_weight = dict()
#     num_classes = len(labels_count)
    
#     #factor = 1 / num_classes
#     for key in range(num_classes):
#         score = math.log(total / float(labels_count[key]))
#         class_weight[key] = score#*factor #if score > 1.0 else 1.0        

#     class_weight = [class_weight[i] for i in range(num_classes)]
#     print(class_weight)
#     return class_weight

# def calc_class_weight(labels_count, method = None):
#     total = np.sum(labels_count)
#     class_weight = dict()
#     num_classes = len(labels_count)

#     factor = 1 / num_classes
#     mu = [factor , factor*1.5 , factor] # 3class
#     for key in range(num_classes):
#         score = 1 - float(labels_count[key]/total)
#         class_weight[key] = score
#         class_weight[key] = round(class_weight[key] * mu[key], 2)

#     class_weight = [class_weight[i] for i in range(num_classes)]
#     print(class_weight)
#     return class_weight