import ftplib
import os
import shutil
import zipfile

from ftplib import FTP
from datetime import datetime, timedelta


class AllMethods:

    @staticmethod
    def download_zip_files_from_ftp_server_and_unzip(server, port, username, password, local_path, ftp_path=None):
        with ftplib.FTP() as ftp:
            ftp.connect(server, port)
            ftp.login(user=username, passwd=password)
            if ftp_path:
                ftp.cwd(ftp_path)
            for file in ftp.nlst():
                local_file_path = os.path.join(local_path, file)
                with open(local_file_path, 'wb') as f:
                    ftp.retrbinary(f'RETR {file}', f.write)
                with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
                    zip_ref.extractall(local_path)
                os.remove(local_file_path)


    @staticmethod
    def clear_directory_if_exist_or_create_new(local_path):
        if os.path.exists(local_path):
            for file in os.listdir(local_path):
                file_path = os.path.join(local_path, file)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            os.makedirs(local_path)


    @staticmethod
    def move_files_to_archive(directory, file_format, days, path=False):
        archive = f'./archive/{path}' if path else './archive/'

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dated_archive_dir = os.path.join(archive, timestamp)

        os.makedirs(archive, exist_ok=True)
        os.makedirs(dated_archive_dir, exist_ok=True)

        now = datetime.now()
        for root, dirs, files in os.walk(archive):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                dir_age = now - datetime.fromtimestamp(os.path.getmtime(dir_path))
                if dir_age > timedelta(days=days):
                    shutil.rmtree(dir_path)

        for filename in os.listdir(directory):
            if filename.endswith(file_format):
                filepath = os.path.join(directory, filename)
                shutil.move(filepath, os.path.join(dated_archive_dir, filename))

    @staticmethod
    def zip_files_in_folder(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                zip_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.zip")
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(file_path, os.path.basename(file_path))
                print(f"Файл {filename} успешно заархивирован в {zip_file_path}")


    @staticmethod
    def delete_files_in_folder_by_format(folder_path, format):
        for filename in os.listdir(folder_path):
            if filename.endswith(format):
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)
                print(f"Файл {filename} успешно удален")

