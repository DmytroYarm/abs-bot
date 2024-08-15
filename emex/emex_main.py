from credentials.emex_credentials import EmexCredentials
from emex.data.emex_data import EmexData
from methods.all_methods import AllMethods
from methods.emex_methods import EmexMethods

from datetime import datetime


class EmexMain:
    def main(self):
        try:
            local_path = '.\\emex\\temp'

            AllMethods.clear_directory_if_exist_or_create_new(local_path)
            AllMethods.download_zip_files_from_ftp_server_and_unzip(EmexCredentials.server,
                                                                    EmexCredentials.port,
                                                                    EmexCredentials.username,
                                                                    EmexCredentials.password,
                                                                    local_path)
            txt = EmexMethods.remove_string_from_csv_files(local_path)
            EmexMethods.rename_csv_files_by_data(local_path, EmexData.emex_data)
            # EmexMethods.upload_files_to_ftp(local_path, EmexCredentials.emex_server, EmexCredentials.emex_port,
            #                                EmexCredentials.emex_username, EmexCredentials.emex_password,
            #                                EmexCredentials.emex_path,
            #                                '.csv')
            AllMethods.move_files_to_archive(local_path, '.csv', 7)
            AllMethods.delete_files_in_folder_by_format(local_path, '.csv')
            return f'<b><u>Перелік файлів з наявністю за {datetime.now().date()}:</u>\n{txt}</b>'
        except Exception as e:
            return f'{datetime.now().date()}\nПомилка завантаження прайсів EMEX\n(Error: {e})'


    def get_emex_names_data(self):
        return EmexMethods.get_names_data()
