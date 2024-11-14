# Run this program before running main.py the very first time

import pickle
knownEncodingsWithIDs={}
with open("knownIDs.pkl","wb") as fileEncodes:
    pickle.dump(knownEncodingsWithIDs,fileEncodes)