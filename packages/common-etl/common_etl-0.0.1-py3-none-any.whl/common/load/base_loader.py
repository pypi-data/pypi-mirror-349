import csv
import os
import shutil
from abc import ABC, abstractmethod

import requests
from common.autherization.auth_token import acquire_token
from common.data_backend.schemas.job_history_schemas import EtlJobSummary
from common.dependencies.depsys import get_job_meta_data
from loggers import logger
from starlette import status


class BaseLoaderService(ABC):

    async def perform_base_loader_service(
            self,
    ) -> dict[str, str | bool | dict] | dict[str, str | bool | dict] | set[str]:
        """
        This function performs additional loader service on the TC/PCM data.
        """
        current_directory = os.getenv("TEM_FOLDER_PATH_EXTRACTED_DATA")
        try:
            file_name = current_directory
            price_file, header_file, revision_file = self.get_file_data(file_name)
            logger.info(price_file)
            logger.info(header_file)
            logger.info(revision_file)

            # Assert that all files are there
            if not price_file or not header_file or not revision_file:
                logger.info(
                    "All files were not uploaded. Ensure that - Header, Revision & Price are uploaded."
                )
                return {
                    "response": False,
                    "message": "All files were not uploaded. Ensure that - Header, Revision & Price are uploaded.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }

            files = await self.read_file(
                current_directory, header_file, revision_file, price_file
            )

            guid_data = get_job_meta_data().bu.details
            guid_dict = {}
            for item in guid_data:
                guid_dict[item.name] = item.value

            json_data = await self.read_files_to_json(current_directory, header_file, revision_file, price_file)

            for _, file in files:
                file.close()

            # Extract values from the dataset in a single loop
            for item, data in json_data.items():
                configuration_guid = next(filter(lambda k: item.upper() in k.upper(), guid_dict.keys()), None)
                if not configuration_guid:
                    raise Exception("Configuration GUID not found.")
                headers, sending_service_calc_url, tc_pcm_server_url = self.create_header(
                    tc_pcm_server_url=guid_dict["TCPCM_API_BASE_URL"],
                    tc_pcm_plant_unique_key=os.getenv("PLANT_UNIQUE_KEY"),
                    configuration_guid=guid_dict[configuration_guid],
                    job_id=os.getenv("JOB_ID"),
                    import_type = item
                )
                logger.info(configuration_guid)
                logger.info("Sending request to sending service")
                logger.info(f"headers: {headers}")
                response = requests.request(
                    "POST",
                    sending_service_calc_url,
                    headers=headers,
                    json=data,
                    timeout=10800,
                )

                if response.status_code != 200:
                    logger.warning(f"Response header: {response.headers}")
                    logger.warning(f"Response body content: {response.content}")
                    logger.info(
                        f"Request to TcPCM ({tc_pcm_server_url}) via Sending Service {sending_service_calc_url}) failed with "
                        f"status code: {response.status_code} and "
                        f"error: {response.text}"
                    )
                    return {
                        "response": False,
                        "message": response.text,
                        "status": response.status_code,
                    }


            return {
                "response": True,
                "message": "tasks successfully sent to queue",
                "status": 200,
            }
        except Exception as error:
            logger.error(error)
            raise error
        finally:
            pass
            # await self.delete_temp_folder(current_directory)

    async def delete_temp_folder(self, current_directory):
        """Delete the directory after the task is completed."""
        if os.path.exists(current_directory):
            shutil.rmtree(current_directory)
            logger.info(f"Folder Path:- {current_directory} has been deleted")

    @abstractmethod
    async def read_file(
            self, current_directory, header_file, revision_file, all_price_file
    ):
        """This method will be overridden by subclasses."""
        pass

    async def read_csv_file(self, file_path, delimiter="\t"):
        """Reads a CSV file and converts each row into a JSON object."""
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                return [row for row in reader]
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

    async def read_files_to_json(self, current_directory, header_file, revision_file, all_price_file):
        """Reads multiple CSV files and returns their content as JSON."""
        job_def = get_job_meta_data().job_definition.name

        files = {
            "Header": os.path.join(current_directory, header_file),
            "Revision": os.path.join(current_directory, revision_file),
            "Staggered_Price" if job_def == "Price conditions (supplier related)" else "Material_Price":
                os.path.join(current_directory, all_price_file),
        }

        result = {key: await self.read_csv_file(path) for key, path in files.items()}

        # logger.info(json.dumps(result, indent=4))
        return result

    def get_file_data(self, folder_name):
        """Gets file paths from the folder."""
        try:
            price_file, header_file, revision_file = "", "", ""
            filenames = os.listdir(folder_name)
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                if filename == os.getenv("STAGGERED_PRICE_FILE_NAME"):
                    price_file = file_path
                    logger.info("Extracted Staggered Price Data")
                elif filename == os.getenv("HEADER_FILE_NAME"):
                    header_file = file_path
                    logger.info("Extracted Header Data")
                elif filename == os.getenv("REVISION_FILE_NAME"):
                    revision_file = file_path
                    logger.info("Extracted Revision Data")
                elif filename == os.getenv("PRICE_FILE_NAME"):
                    price_file = file_path
                    logger.info("Extracted Material Price Data")
            return price_file, header_file, revision_file
        except Exception as error:
            logger.error(error)
            raise error

    def create_header(self, tc_pcm_server_url, tc_pcm_plant_unique_key, configuration_guid, job_id, import_type):
        """Creates header for API request."""
        try:
            tc_pcm_sending_service_url = os.getenv("TCPCM_SENDING_SERVICE_URL")
            sending_service_calc_url = tc_pcm_sending_service_url + "/api/material-via-celery"
            token = acquire_token()
            logger.info("TcPCM token generated")
            headers = {
                "Content-Type": "application/json",
                "Tcpcm-Ip": tc_pcm_server_url,
                "PlantUniqueKey": tc_pcm_plant_unique_key,
                "Authorization": f"Bearer {token}",
                "ConfigurationGuid": configuration_guid,
                "JOB-ID": job_id,
                "IMPORT-TYPE": import_type
            }
            return headers, sending_service_calc_url, tc_pcm_server_url
        except Exception as error:
            logger.error(error)
            raise error
