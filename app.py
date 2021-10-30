
import json
from backend import callpicker
from backend.callpicker import CallPicker
import pandas as pd




if __name__ == '__main__':
    '''
    This is the main entry point for the application.
    '''
    callpicker = CallPicker()
    calls_row = callpicker.get_calls()
    calls_df = pd.DataFrame(calls_row)
    calls_df.to_csv('temp/calls.csv', index=False)
    

    

