import os
import sys
import subprocess

def convert_ui():
    root_directory = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(".ui"):
                ui_path = os.path.join(subdir, filename)
                py_filename = f"{os.path.splitext(filename)[0]}.py"
                py_path = os.path.join(subdir, py_filename)

                # Check if the .py file needs to be generated or updated
                if not os.path.exists(py_path) or os.path.getmtime(ui_path) > os.path.getmtime(py_path):
                    command = f"pyside6-uic {ui_path} -o {py_path}"
                    subprocess.run(command, shell=True, check=True)
                    print(f"Converted {ui_path} -> {py_path}")
                else:
                    print(f"No update needed for {py_path}")

if __name__ == "__main__":
    convert_ui()
