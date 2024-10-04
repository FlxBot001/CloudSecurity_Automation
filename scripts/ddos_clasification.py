# Core modules
import pandas as pd
import numpy as np

# Graphical representation modules
import matplotlib.pyplot as plt
import seaborn as sns
import csv

# Machine learning module
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ML Model
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

# ML Evaluation
from sklearn.metrics import accuracy_score,f1_score, precision_score, recall_score, roc_curve, auc

from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from itertools import cycle

df = pd.read_csv("data/DDos.csv")
