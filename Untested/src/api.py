"""
==================================================================================
Title:          network.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    Class for managing the API network
Verson:         2.0
==================================================================================
"""
import requests
import json

#TODO: This is the least tested object so far, test alongslied jacob to ensuer proper functionality
#===============================================================================
# Class for User Data
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.training_data = {'ma_xlist': [], 'x_list': [], 'y_list': [], 'blood_loss': []}

    def setTrainingData(self, ma_xlist, x_list, y_list, blood_loss):
        self.training_data['ma_xlist'] = ma_xlist
        self.training_data['x_list'] = x_list
        self.training_data['y_list'] = y_list
        self.training_data['blood_loss'] = blood_loss


#===============================================================================
# Class for Training Class
class TrainingClass:
    def __init__(self, class_id, users):
        self.class_id = class_id
        self.users = users


#===============================================================================
# Primary Class for network management
class API_Network:

    # Class Intializer
    def __init__(self, api_address):
        self.__address = api_address # Should be static within object
        self.__selected_User = None
        self.__current_class = None

    #===============================================================================
    # Method for making request to the API
    def make_http_get_request(self, trainingKey):
        url = f"{self.__address}/classUsers"
        data = {'trainingKey': trainingKey}

        try:
            response = requests.get(url, json=data)
            json_data = response.json()

            class_id = json_data.get("classID")
            users_data = json_data.get("users", [])

            users_list = [User(user_data["ID"], user_data["Name"]) for user_data in users_data]
            self.Class = TrainingClass(class_id=class_id, users=users_list)

        except Exception as e:
            print(f"Error making HTTP request: {e}")

    #===============================================================================
    # Method for making put request to API
    def make_http_put_request(self, success: bool):

        #TODO: update for training type option
        if not (self.Class and self.User):
            raise Exception("Class and User must be set before making PUT request")

        url = f"{self.__address}/updateTrainingData"
        data =  {'class_id': self.__current_class.class_id, 'user_id': self.__selected_User.user_id,
                 'x_list': self.__selected_User.training_data['x_list'], 'y_list': self.__selected_User.training_data['y_list'],
                 'bloodloss': self.__selected_User.training_data['blood_loss'], 'passed': success}

        try:
           response = request.put(url, json=data)
        except Exception as e:
            print(f"Error making HTTP request: {e}")

    #===============================================================================
    # Methods for managing current class
    @property
    def Class(self):
        return self.__current_class

    @Class.setter
    def Class(self, value):
        if not isinstance(value, TrainingClass):
            raise Exception("Class must be of type TrainingClass")
        self.__current_class = value

    @Class.deleter
    def Class(self):
        self.__current_class = None

    #===============================================================================
    # Methods for managing selected user
    @property
    def User(self):
        return self.__selected_User

    @User.setter
    def User(self, value):
        if not isinstance(value, User):
            raise Exception("User must be of type User")
        self.__selected_User = value

    @User.deleter
    def User(self):
        self.__selected_User = None

    def submit_TrainingData(self,  ma_xlist, x_list, y_list, blood_loss, passed):
        self.__selected_User.setTrainingData(ma_xlist, x_list, y_list, blood_loss)
        self.make_http_put_request(passed)

