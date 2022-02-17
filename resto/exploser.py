import os

fichier = input("le fichier à traiter:")
destination = "".join(fichier.split(".")[:-1])
os.mkdir(destination)

with open(fichier, "r") as file:
	new_file = open(os.path.join(destination, "dependancies.py"), "a+")
	init = open(os.path.join(destination, "__init__.py"), "w+")

	for line in file.readlines():
		if line.startswith("class ") or line.startswith("def ") :
			new_file.close()
			class_name = line.split("(")[0].replace("class ", "").replace("def ", "")
			init.write(f"from .{class_name} import {class_name}\n")
			new_file = open(os.path.join(destination, f"{class_name}.py"), "w+")
			new_file.write("from .dependancies import *\n\n")
		new_file.write(line)
	new_file.close()
	init.close()
