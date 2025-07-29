import os
from abc import ABC, abstractmethod
from os.path import dirname as up

import cryptocode
import pandas as pd
import snowflake.connector
from common.custom_exception.data_extraction_exception import DataExtractionException
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

from common.utils.utils import RemoveLeadingZeros
from loggers import logger

load_dotenv(".env")


class AbstractSnowflakeQueryExecutor(ABC):

    @abstractmethod
    def get_query(self):
        pass

    def fetchConnection(self):
        try:
            if os.getenv("EXECUTOR_ENV") != "local":
                __p_key__ = self.deployment_server()
            else:
                __p_key__ = self.local_server()

            # Connect to Snowflake using the private key
            __conn__ = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                private_key=__p_key__,
                warehouse="",
                database="",
                schema="",
            )
            return __conn__

        except Exception as e:
            logger.error(e)
            raise DataExtractionException("Unable to make Connection!!!!!!")

    def deployment_server(self):
        try:
            env_dir = up(up(up(up(__file__))))
            load_dotenv(env_dir + "\\.env")
            encoded_pem = os.getenv("SNOWFLAKE_PEM2")
            logger.info(f"encoded_pem::::::::\n{encoded_pem}encoded_pem")
            snowflake_pwd = os.getenv("SNOWFLAKE_PWD2")
            logger.info(f"snowflake_pwd::::::::\n{snowflake_pwd}\nsnowflake_pwd")
            snowflake_pem = cryptocode.decrypt(encoded_pem, snowflake_pwd)
            logger.info(f"snowflake_pem::::::::\n{snowflake_pem}\nsnowflake_pem")
            __pkb__ = serialization.load_pem_private_key(
                snowflake_pem.encode(),
                password=snowflake_pwd.encode(),
                backend=default_backend(),
            )
            # Serialize the private key
            __p_key__ = __pkb__.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            return __p_key__

        except Exception as e:
            logger.error(e)
            raise DataExtractionException("Unable to load private key!!!!!!")

    def local_server(self):
        try:
            env_dir = up(up(up(up(__file__))))
            load_dotenv(env_dir + "\\.env")
            # Load private key from a PEM file and password from a text file
            snowflake_props_path = os.getenv("SNOWFLAKE_PROPS_PATH")
            with (
                open(snowflake_props_path + os.getenv("SNOWFLAKE_PEM"), "rb") as key,
                open(
                    snowflake_props_path + os.getenv("SNOWFLAKE_PWD"), "r"
                ) as password_file,
            ):
                __p_key__ = serialization.load_pem_private_key(
                    key.read(),
                    password=password_file.read().strip().encode(),
                    backend=default_backend(),
                )
            return __p_key__
        except Exception as e:
            logger.error(e)
            raise DataExtractionException("Unable to load private key!!!!!!")

    def execute(self, query: str = None):
        try:
            __conn__ = self.fetchConnection()
            sql_query = self.get_query()
            cs = __conn__.cursor()
            if query is not None:
                cs.execute(query)
            else:
                cs.execute(sql_query)
            rows = cs.fetchall()
            data_frame = pd.DataFrame(
                rows, columns=[desc[0] for desc in cs.description]
            )
            return data_frame
        except Exception as e:
            logger.error(e)
            raise DataExtractionException("Unable fetch data from Snowflake!!!!")
