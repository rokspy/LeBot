import json

MainDict = {}
RedDict = {'min': [0, 0, 0], 'max': [0, 0, 0]}
BlueDict = {'min': [0, 0, 0], 'max': [0, 0, 0]}
GreenDict = {'min': [0, 0, 0], 'max': [0, 0, 0]}

MainDict['red'] = RedDict
MainDict['blue'] = BlueDict
MainDict['green'] = GreenDict

out_file = open("color_parameters.json", "w")
json.dump(MainDict, out_file, indent=4)
out_file.close()