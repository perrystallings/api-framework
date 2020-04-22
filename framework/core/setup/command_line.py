def main():
    import os, shutil
    template_folder = os.path.abspath(__file__).replace('setup/command_line.py', 'template/')
    for root, dirs, files in os.walk(template_folder):
        new_folder = root.replace(template_folder, './')
        if not os.path.isdir(new_folder):
            os.mkdir(new_folder)
        for file in files:
            old_path = os.path.join(root, file)
            new_path = os.path.join(new_folder, file)
            shutil.copyfile(old_path, new_path)
