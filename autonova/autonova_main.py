from credentials.autonova_credentials import AutonovaCredentials
from methods.all_methods import AllMethods
from methods.autonova_methods import AutonovaMethods

from datetime import datetime


class AutonovaMain:

    def main(self):
        try:
            local_path = '.\\autonova\\temp'

            AllMethods.clear_directory_if_exist_or_create_new(local_path)
            AllMethods.download_zip_files_from_ftp_server_and_unzip(AutonovaCredentials.server,
                                                                    AutonovaCredentials.port,
                                                                    AutonovaCredentials.username,
                                                                    AutonovaCredentials.password,
                                                                    local_path)

            AutonovaMethods.cut_the_price_by_n_percent(local_path, 7)

            AllMethods.zip_files_in_folder(local_path)

            AllMethods.delete_files_in_folder_by_format(local_path, '.csv')
            AutonovaMethods.upload_files_to_ftp(local_path, AutonovaCredentials.server, AutonovaCredentials.port,
                                           AutonovaCredentials.username, AutonovaCredentials.password, None,
                                           '.zip')
            AllMethods.move_files_to_archive(local_path, '.zip', 7)
            AllMethods.delete_files_in_folder_by_format(local_path, '.zip')
            return f"\n<b><u>{datetime.now().date()}:</u>\nПрайс AUTONOVA оновлено</b>"
        except Exception as e:
            return f'{datetime.now().date()}\nПомилка завантаження прайсу AUTONOVA\n(Error: {e})'
