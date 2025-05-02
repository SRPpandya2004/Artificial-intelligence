import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"______Add URL here____________"
})

ref = db.reference('Students')

data = {
    "30241":{
        "Name":"Patel Ayush",
        "Major":"Web Development",
        "starting_year":2022,
        "total_attendance":0,
        "Standing":"G",
        "year":3,
        "last_attendance": "10-01-2005 00:00:00",
    },
    
    "30460":{
        "Name":"Manthan Upadhyay",
        "Major":"Data Scientist",
        "starting_year":2022,
        "total_attendance":0,
        # "last_attendance_time": "10-01-2005 00:00:00",
        "Standing":"G",
        "year":3,
        "last_attendance":"10-01-2005 00:00:00"
    },
    "30200":{
        "Name":"Pawar Sahil",
        "Major":"flutter",
        "starting_year":2022,
        "total_attendance":0,
        "Standing":"G",
        "year":3,
        "last_attendance": "10-01-2005 00:00:00",
    },
 
    "30259":{
        "Name":"Patel Dev",
        "Major":"Cybersecurity",
        "starting_year":2022,
        "total_attendance":0,
        "Standing":"A",
        "year":3,
        "last_attendance": "10-01-2005 00:00:00",
    },

    "30295":{
        "Name":"Lad Viraj",
        "Major":"Cloud Engineer",
        "starting_year":2022,
        "total_attendance":0,
        "Standing":"G",
        "year":3,
        "last_attendance": "10-01-2005 00:00:00",
    },
    "30159":{
        "Name":"Makwana Harsh",
        "Major":"Data Scientist",
        "starting_year":2022,
        "total_attendance":0,
        "Standing":"G",
        "year":3,
        "last_attendance": "10-01-2005 00:00:00",
    },

}

for key,value in data.items():
    ref.child(key).set(value)