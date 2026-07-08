import pickle
from matplotlib import pyplot as plt
import numpy as np


def load_pickle(dir_path, file_name) -> np.ndarray:
    with open(dir_path + file_name, 'rb') as f:
        return pickle.load(f)
    
def save_pickle(dir_path, file_name, data: np.ndarray):
    with open(dir_path + file_name, 'wb') as f:
        pickle.dump(data, f)
        
def plot_file(dir_path, file_name, sample_rate):
    data = load_pickle(file_name)
    #use file name as title
    plt.title(file_name)
    
    #plot data, with x axis in seconds. it is now in samples
    plt.plot(np.arange(data.shape[0])/sample_rate, data)
    plt.show()