import os
import time
import json
import numpy as np
import pickle

class Logger:
    """
    A general-purpose logger.
    Simplify the saving of diagnostics, hyperparameter configurations, and the 
    state of a training run. Saves the data in the form of a dictionary, and dumps them into a .json file
    """
    def __init__(self, output_dir=None, output_fname='logs.json'):
        """
        Initialize a Logger.
        Args:
            output_dir (string): A directory for saving results to. If 
                ``None``, defaults to a temp directory of the form
                ``tmp/experiments/somerandomnumber``.
            output_fname (string): Name for the tab-separated-value file 
                containing metrics logged throughout a training run. 
                Defaults to ``progress.txt``. 
        """
        self.output_dir = output_dir or os.path.join("tmp", "experiments", f"{int(time.time())}")
        os.makedirs(self.output_dir, exist_ok=True)

        self.output_filepath = os.path.join(self.output_dir, output_fname)
        self.logger_dict = {}
        self.logger_list = [self.logger_dict]
        if os.path.isfile(self.output_filepath):
            with open(self.output_filepath, 'r') as f:
                self.logger_list = json.loads(f.read())
        self.init = True
        

    def store(self, **kwargs):
        """
        Save something into the logger's current state.
        Provide an arbitrary number of keyword arguments with numerical 
        values.
        """
        for k, v in kwargs.items():
            if not(k in self.logger_dict.keys()):
                self.logger_dict[k] = []
            self.logger_dict[k].append(v)

    def dump(self):
        """
        Write all of the diagnostics from the current iteration.
        Writes to the output file.
        """
        # print(self.logger_dict)
        # with open(self.output_filepath, 'wb') as f:
        #     pickle.dump(self.logger_dict, f)

        if self.init:
            assert self.logger_dict == True, "no variables stored inside dictionary to dump!"
            self.logger_list.append(self.logger_dict)
            self.init = False
        else:
            self.logger_list[-1] = self.logger_dict

        with open(self.output_filepath, 'w') as f:
            f.write(json.dumps(self.logger_list, indent=4))
    
    def reset(self):
        '''
        Reset the log dict for a new experiment. Used for training the same algorithm multiple times
        '''
        self.logger_dict = {}
        self.logger_list.append(self.logger_dict)

        with open(self.output_filepath, 'w') as f:
            f.write(json.dumps(self.logger_list, indent=4))

    def load_results(self, keys):
        '''
        return all the stored variables in the .json file
        Args:
            keys (list): list of keys to extract from logger
        '''

        output = []
        for json_dict in self.logger_list:
            output_dict = []
            for key in keys:
                assert key in json_dict.keys(), "Attempted to get variables that are not stored in this .json file"
                output_dict.append(json_dict[key])
        
            output.append(output_dict)
        return output