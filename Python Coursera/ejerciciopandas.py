# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 14:40:50 2025

@author: User
"""

import pandas as pd
import os 

file_name = 'grocery_list.csv'

if os.path.exists(r"C:\Users\User\OneDrive\Documents\ARCHIVOS PYTHON\Python Coursera\grocery_list.csv"):
    # Load the grocery list from the CSV file
    grocery_list_df = pd.read_csv("grocery_list.csv")

    # Extract the items from the DataFrame and store t  hem in a list
    grocery_list = grocery_list_df['item'].tolist()

    # Print the grocery list and inspect the output
    print(grocery_list)
else:
    print(f"Error: The file '{grocery_list.csv}' was not found in the current directory.")
    print("Please ensure you have followed the instructions on the Coursera site to extract the files from the zip archive.")