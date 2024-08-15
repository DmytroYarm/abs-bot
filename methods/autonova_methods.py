import ftplib
import os
from ftplib import FTP

from methods.all_methods import AllMethods

import csv


class AutonovaMethods(AllMethods):


    @staticmethod
    def upload_files_to_ftp(directory, ftp_host, ftp_port, ftp_user, ftp_password, ftp_directory, file_format):
        with FTP() as ftp:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_user, ftp_password)
            if ftp_directory:
                ftp.cwd(ftp_directory)
            for filename in os.listdir(directory):
                if filename.endswith(file_format):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'rb') as file:
                        ftp.storbinary(f"STOR {filename}", file)


    @staticmethod
    def cut_the_price_by_n_percent(folder_path, n):
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                temp_file_path = os.path.join(folder_path, "temp_" + filename)

                with open(file_path, mode='r', encoding='utf-8') as infile, open(temp_file_path, mode='w', newline='',
                                                                                 encoding='utf-8') as outfile:
                    reader = csv.DictReader(infile, delimiter=';')
                    fieldnames = reader.fieldnames
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()
                    for row in reader:
                        original_price = float(row['price'])
                        discounted_price = original_price * (1 - n / 100)
                        row['price'] = f"{discounted_price:.2f}"
                        writer.writerow(row)
                os.replace(temp_file_path, file_path)

        print("Цены успешно обновлены во всех CSV файлах в папке")