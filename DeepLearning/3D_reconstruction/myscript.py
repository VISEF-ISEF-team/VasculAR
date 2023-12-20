import json
import subprocess
import sys
import os

def run_script_with_dictionary(dictionary):
    # Serialize the dictionary to a JSON-formatted string
    json_string = json.dumps(dictionary)

    # Get the path to the virtual environment activate script
    venv_activate_script = os.path.join('D:/Documents/GitHub/VascuIAR/.venv/Scripts', 'bin', 'activate')  # Adjust the path accordingly

    # Run the activation command and then run the script with the JSON string as a command line argument
    activation_command = f"source {venv_activate_script}" if sys.platform.startswith('linux') or sys.platform.startswith('darwin') else f"activate {venv_activate_script}"
    subprocess.run(f"{activation_command} && python automatic_reconstruction.py 020", shell=True)
    
    
info_patient_dict = {
    "Organization": "Benh vien Cho Ray",
    "Patient's name": "Ton That Hung",
    "Modality": "MRI",
    "Patient ID": "0000097031",
    "Body Part Examined": "CHEST_TO_PELVIS",
    "Acquisition Date": "20231019"
}
    

run_script_with_dictionary(info_patient_dict)

