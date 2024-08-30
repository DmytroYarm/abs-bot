import os
from ftplib import FTP

from emex.data.emex_data import EmexData
from methods.all_methods import AllMethods

from datetime import datetime, timedelta


class EmexMethods(AllMethods):


    @staticmethod
    def upload_files_to_ftp(directory, ftp_host, ftp_port, ftp_user, ftp_password, ftp_directory, file_format):
        with FTP(ftp_host, ftp_user, ftp_password) as ftp:
            if ftp_directory:
                ftp.cwd(ftp_directory)
            for filename in os.listdir(directory):
                if filename.endswith(file_format):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'rb') as file:
                        ftp.storbinary(f"STOR {filename}", file)


    @staticmethod
    def rename_csv_files_by_data(directory, data):
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                file_name, file_extension = os.path.splitext(filename)
                new_name = data[file_name][0] + file_extension
                new_file_path = os.path.join(directory, new_name)
                os.rename(file_path, new_file_path)


    @staticmethod
    def remove_string_from_csv_files(directory, value='PAK', target_column_name='"price_code"'):
        log_file = './error_log.txt'
        if os.path.exists(log_file):
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(log_file))
            if file_age > timedelta(days=30):
                os.remove(log_file)

        non_empty_files = ''

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)

                AllMethods.fill_cells_in_column(file_path, '"stock_quantity"', 100)

                with open(file_path, 'r') as input_file:
                    output_lines = []
                    lines = input_file.readlines()

                    output_lines.append(lines[0])
                    output_lines.append(lines[1])

                    if len(lines) > 2:
                        try:
                            header = lines[0].strip().split(';')
                            target_index = header.index(target_column_name)
                        except ValueError as e:
                            with open(log_file, 'a') as log:
                                log.write(f'ERROR in file {filename}: Column {target_column_name} not found\n')
                            continue
                        for line in lines[2:]:
                            columns = line.strip().split(';')
                            try:
                                if value not in columns[target_index]:
                                    output_lines.append(line)
                            except Exception as e:
                                with open(log_file, 'a') as log:
                                    log.write(f'ERROR in row {line}: {e}\n')

                with open(file_path, 'w') as output_file:
                    output_file.writelines(output_lines)

                if len(output_lines) > 2:
                    non_empty_files += f'{filename}\n'

        return non_empty_files


    @staticmethod
    def get_names_data():
        result = ''
        for key, value in EmexData.emex_data.items():
            result += f'{value[0]} -> {key}\n'
        return result
