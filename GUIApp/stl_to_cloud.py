import zipfile
import os
import pyrebase
import sys

firebaseConfig = {
    'apiKey': "AIzaSyCoG09bln3Qrmws87pxnNak-dLC58wCeWE",
    'authDomain': "vascular-68223.firebaseapp.com",
    'databaseURL': "https://vascular-68223-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "vascular-68223",
    'storageBucket': "vascular-68223.appspot.com",
    'messagingSenderId': "1068291063816",
    'appId': "1:1068291063816:web:a1c19e8d2bd465cf7c91bd",
    'measurementId': "G-27VPL4BB1D"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

specified_data = sys.argv[1]

path = f'D:/Documents/GitHub/VascuIAR/DeepLearning/data/VnRawData/VHSCDD_sep_labels/VHSCDD_{specified_data}_label/'
files = os.listdir(path)
for file in files:
    if (file.endswith('.stl')):
        filename = f"reconstruction/case_{specified_data}/{file}"
        storage.child(filename).put(path + file)
        print('Successful')
