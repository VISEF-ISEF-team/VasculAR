import json
import os

class DataManager:
    def __init__(self):
        self.file_extension = ".vas"
        self.data_directory = "D:/Documents/GitHub/VascuIAR/GUIApp/default_data/"
        
    def save_after_data(self, file_name, directory, 
                        ROI_data, draw_data, 
                        class_data, analysis_data, 
                        dict_info, paths, folder_imgs):
        combined_data = {
            "ROI_data.json": ROI_data,
            "draw_data.json": draw_data,
            "class_data.json": class_data,
            "analysis_data.json": analysis_data,
            "dict_info.json": dict_info,
            "paths.json" : paths,
            "folder_imgs.json": folder_imgs,
        }
        combined_file_path = os.path.join(directory, f"{file_name}{self.file_extension}")
        with open(combined_file_path, 'w') as vas_file:
            json.dump(combined_data, vas_file, indent=4)
        
    def save_default_data(self):
        default_data = {}

        # List of JSON files to be combined
        json_files = [
            "analysis_data.json",
            "class_data.json",
            "draw_data.json",
            "ROI_data.json",
        ]

        for file_name in json_files:
            # Read each JSON file and add its content to the default_data dictionary
            with open(os.path.join(self.data_directory, file_name), 'r') as json_file:
                data = json.load(json_file)
                default_data[file_name] = data

        # Save the combined data to the "default_data.vas" file
        with open(os.path.join(self.data_directory, f"default_data{self.file_extension}"), 'w') as vas_file:
            json.dump(default_data, vas_file, indent=4)

    def load_default_data(self):
        # Load the combined data from the "default_data.vas" file
        with open(os.path.join(self.data_directory, f"default_data{self.file_extension}"), 'r') as vas_file:
            default_data = json.load(vas_file)
        return default_data
    
    def load_saved_vas_data(self, vas_file_path):
        # Load the combined data from the "default_data.vas" file
        with open(vas_file_path, 'r') as vas_file:
            vas_data = json.load(vas_file)
        return vas_data
    
    def load_dict_info_data(self, filepath):
        with open(filepath, 'r') as json_file:
            dict_info = json.load(json_file)
            return dict_info
    
