from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import base64
from typing import Dict


import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.sqlalchemy import URL as snowflake_URL
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine.base import Engine


def mysql_engine_factory(
        args: Dict[str, str], 
        hostname: str, 
        database: str=""
    ) -> Engine:
    """
    Create a database engine for mysql from a dictionary of database info.
    """

    mysql_host = {
        "PROD_MAIN": {
            "ADDRESS": "MYSQL_PROD_MAIN_HOST",
            "DATABASE": database,
            "PORT": 3306,
            "USERNAME": "MYSQL_PROD_MAIN_SERVICE_USER",
            "PASSWORD": "MYSQL_PROD_MAIN_SERVICE_PASSWORD" 
        },
        "PROD_MAIN_REPLICA": {
            "ADDRESS": "MYSQL_PROD_MAIN_REPLICA_HOST",
            "DATABASE": database,
            "PORT": 3306,
            "USERNAME": "MYSQL_PROD_MAIN_REPLICA_SERVICE_USER",
            "PASSWORD": "MYSQL_PROD_MAIN_REPLICA_SERVICE_PASSWORD" 
        },
        "PROD_SHARED": {
            "ADDRESS": "MYSQL_PROD_SHARED_HOST",
            "DATABASE": database,
            "PORT": 3306,
            "USERNAME": "MYSQL_PROD_SHARED_SERVICE_USER",
            "PASSWORD": "MYSQL_PROD_SHARED_SERVICE_PASSWORD" 
        },
        "PROD_DA": {
            "ADDRESS": "MYSQL_PROD_DA_HOST",
            "DATABASE": database,
            "PORT": 3306,
            "USERNAME": "MYSQL_PROD_DA_SERVICE_USER",
            "PASSWORD": "MYSQL_PROD_DA_SERVICE_PASSWORD" 
        },
        "DEV_MAIN": {
            "ADDRESS": "MYSQL_DEV_MAIN_HOST",
            "DATABASE": database,
            "PORT": 3306,
            "USERNAME": "MYSQL_DEV_MAIN_SERVICE_USER",
            "PASSWORD": "MYSQL_DEV_MAIN_SERVICE_PASSWORD" 
        },
        "DEV_SHARED": {
            "ADDRESS": "MYSQL_DEV_SHARED_HOST",
            "DATABASE": database,
            "PORT": 3306,
            "USERNAME": "MYSQL_DEV_SHARED_SERVICE_USER",
            "PASSWORD": "MYSQL_DEV_SHARED_SERVICE_PASSWORD" 
        },
    }

    vars_dict = mysql_host[hostname]

    db_username = args[vars_dict["USERNAME"]]
    db_password = args[vars_dict["PASSWORD"]]
    db_address = args[vars_dict["ADDRESS"]]
    db_port = vars_dict["PORT"]
    db_database = vars_dict["DATABASE"]

    conn_string = (
        f"mysql+pymysql://{db_username}:{db_password}@{db_address}:{db_port}/{db_database}"
    )

    return create_engine(conn_string)


def get_private_key(private_key_base64):
    """
    Decode base64-encoded PEM private key and return it in DER (bytes) format.
    """

    key = load_pem_private_key(
        base64.b64decode(private_key_base64),
        password=None,
    )

    return key.private_bytes(
        encoding=Encoding.DER,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    )

def snowflake_engine_factory(
    args: Dict[str, str],
    role: str,
    schema: str = "",
    load_warehouse: str = "SNOWFLAKE_DS_WAREHOUSE",
) -> Engine:
    """
    Create a database engine for snowflake from a dictionary of database info.
    """

    # Figure out which vars to grab
    role_dict = {
        "LOADER": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PASSWORD": "SNOWFLAKE_LOAD_PASSWORD",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "accountadmin",
        },
        "LOADER_SECURED": {
            "USER": "SNOWFLAKE_LOAD_USER",
            "PRIVATE_KEY": "SNOWFLAKE_LOADER_PRIVATE_KEY_BASE64",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_LOAD_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "accountadmin",
        },
        "DATA_SCIENCE_LOADER": {
            "USER": "SNOWFLAKE_DS_USER",
            "PRIVATE_KEY": "SNOWFLAKE_DS_PRIVATE_KEY_BASE64",
            "ACCOUNT": "SNOWFLAKE_ACCOUNT",
            "DATABASE": "SNOWFLAKE_GENERIC_DATABASE",
            "WAREHOUSE": load_warehouse,
            "ROLE": "accountadmin",
        }
    }

    vars_dict = role_dict[role]

    conn_string = snowflake_URL(
        user=args[vars_dict["USER"]],
        account=args[vars_dict["ACCOUNT"]],
        database=args[vars_dict["DATABASE"]],
        warehouse=args[vars_dict["WAREHOUSE"]],
        role=vars_dict["ROLE"],
        schema=schema,
    )

    conn_args = {
        "private_key": get_private_key(args[vars_dict["PRIVATE_KEY"]])
    }

    return create_engine(
        conn_string, connect_args=conn_args
    )