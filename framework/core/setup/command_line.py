directories = [
    './app',
    './app/schema',
    './app/schema',
]


def main():
    import os, shutil
    for root, dirs, files in os.walk('../template'):

        new_folder = root.replace('../', './')
        if new_folder != './':
            pass

        for file in files:
            old_path = os.path.join(root, file)
            new_path = os.path.join(new_folder, file)
            shutil.copyfile(old_path, new_path)
