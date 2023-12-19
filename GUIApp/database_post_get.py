import pyrebase
import base64

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

case1 = {
    "dict_info":{
        "Organization": "Benh vien Cho Ray",
        "Patient's name": "Nguyen Xuan Manh",
        "Modality": "CT",
        "Patient ID": "0000096570",
        "Body Part Examined": "CHEST_TO_PELVIS",
        "Acquisition Date": "20230920",
    },
    "analysis_data":{
        "number": 0
    },
    "class_data" : {
        "class1": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class2": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class3": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class4": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class5": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class6": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class7": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class8": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class9": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class10": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class11": {
            "visible": False,
            "color": "#FFFFFF"
        },
        "class12": {
            "visible": False,
            "color": "#FFFFFF"
        }
    },
    'ROI_data':{
        "axial": {
            "rec": {
                "x1": 50,
                "y1": 50,
                "x2": 500,
                "y2": 500
            },
            "nw": {
                "x": 0,
                "y": 0
            },
            "ne": {
                "x": 0,
                "y": 0
            },
            "sw": {
                "x": 0,
                "y": 0
            },
            "se": {
                "x": 0,
                "y": 0
            }
        },
        "sagittal": {
            "rec": {
                "x1": 50,
                "y1": 50,
                "x2": 500,
                "y2": 500
            },
            "nw": {
                "x": 0,
                "y": 0
            },
            "ne": {
                "x": 0,
                "y": 0
            },
            "sw": {
                "x": 0,
                "y": 0
            },
            "se": {
                "x": 0,
                "y": 0
            }
        },
        "coronal": {
            "rec": {
                "x1": 50,
                "y1": 50,
                "x2": 500,
                "y2": 500
            },
            "nw": {
                "x": 0,
                "y": 0
            },
            "ne": {
                "x": 0,
                "y": 0
            },
            "sw": {
                "x": 0,
                "y": 0
            },
            "se": {
                "x": 0,
                "y": 0
            }
        }
    },
    "draw_data" : {
        "number_of_elements": 1,
        "Bat thuong 1": {
            "canvas": "axial",
            "type": "rectangle",
            "slice": 100,
            "x1": 100,
            "y1": 100,
            "x2": 300,
            "y2": 300,
            "color": "red",
            "note": "default analysis"
        }
    },
    "folder_imgs" :{
        
    }
}

filename = "test.png"



storage.child(filename).put("D:/Documents/GitHub/VascuIAR/GUIApp/temp8.png")
image_url = storage.child(filename).get_url(None)
downloaded_file_path = "nice.png"
case1["folder_imgs"]['temp8'] = filename

db.child("case1").set(case1)

data_from_db = db.child("case1").get().val()
print(data_from_db["folder_imgs"])

# storage.child(filename).download(filename, downloaded_file_path)