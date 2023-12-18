import json
import os

class DataManager:
    def __init__(self):
        self.file_extension = ".vas"
        self.data_directory = "D:/Documents/GitHub/VascuIAR/GUIApp/"
        
    def save_combined_data(self):
        combined_data = {}

        # List of JSON files to be combined
        json_files = [
            "analysis_data.json",
            "class_data.json",
            "draw_data.json",
            "patient_data.json",
            "ROI_data.json",
            "paths.json"
        ]

        for file_name in json_files:
            # Read each JSON file and add its content to the combined_data dictionary
            with open(os.path.join(self.data_directory, file_name), 'r') as json_file:
                data = json.load(json_file)
                combined_data[file_name] = data

        # Save the combined data to the "combined_data.vas" file
        with open(os.path.join(self.data_directory, f"combined_data{self.file_extension}"), 'w') as vas_file:
            json.dump(combined_data, vas_file, indent=4)

    def load_combined_data(self):
        # Load the combined data from the "combined_data.vas" file
        with open(os.path.join(self.data_directory, f"combined_data{self.file_extension}"), 'r') as vas_file:
            combined_data = json.load(vas_file)

        return combined_data

# Example usage
data_manager = DataManager()

# Save the combined data to "combined_data.vas"
# data_manager.save_combined_data()

# Load the combined data from "combined_data.vas"
loaded_combined_data = data_manager.load_combined_data()

# Access individual JSON files from the loaded data
analysis_data = loaded_combined_data["analysis_data.json"]
class_data = loaded_combined_data["class_data.json"]
draw_data = loaded_combined_data["draw_data.json"]
patient_data = loaded_combined_data["patient_data.json"]
ROI_data = loaded_combined_data["ROI_data.json"]
paths_data = loaded_combined_data["paths.json"]


print(analysis_data)

