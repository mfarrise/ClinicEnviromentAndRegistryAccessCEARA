import json

setting_dic={"patient_dir":" "}


with open("PatientDashBoard_settings.json","w")as file:
    json.dump(setting_dic,file,indent=4)
