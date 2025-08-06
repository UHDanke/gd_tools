from level_tools.classes.object import ObjectList
from level_tools.classes.level import Level
from level_tools.classes.serialization import decode_string
import os
from pathlib import Path
import base64
import glob

from level_tools.mappings import obj_id

txt_files = glob.glob("*.txt")


def convert_official_coins(obj):
    
    if obj.get(1) == 142:
        obj[1] = obj_id.collectible.user_coin
        obj.pop(12,None)
        print(obj)

def print_13(obj):
    
    if obj.get(1) == 13:
        print(obj)

INPUT_FOLDER = r"D:\SteamLibrary\steamapps\common\Geometry Dash\Resources\levels"
OUTPUT_FOLDER = r"D:\Downloads\official levels"

if __name__ == "__main__":
    
    if INPUT_FOLDER:
        input_folder = Path(INPUT_FOLDER)
    else:
        input_folder = Path(input("Enter the input folder path: ").strip())
    if OUTPUT_FOLDER:
        output_folder = Path(OUTPUT_FOLDER)
    else:
        output_folder = Path(input("Enter the output folder path: ").strip())
    
    os.makedirs(output_folder, exist_ok=True)
    
    stereo_madness = Level.from_plist(r"D:\Downloads\official levels\Stereo Madness copy.gmd")
    
    with open(output_folder / "stereo_madness.txt","w") as file:
        file.write(stereo_madness.object_string.replace(";",";\n"))
        
    files = glob.glob(str(input_folder / "*.txt"))
    for file_path in files:
        
        basename = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(basename)

        print("File:",file_name)
        
        with open(file_path,"r") as file:
            string = (file.read()).strip()
            
            print(string[:30])
            

            level = Level(**{'k2':file_name,'k4':string,'k5':"RobTop"})
    
            objects = level.objects
            
            start = level.start
            
            level.objects.apply(convert_official_coins,print_13)
            level.save()
            objstr = level.object_string
            level.to_plist(output_folder)
            with open(output_folder / basename, "w") as file:
                file.write(level.object_string.replace(";",";\n"))
            with open(output_folder / ("originals_" + str(basename)), "w") as file:
                file.write(decode_string(string).replace(";",";\n"))