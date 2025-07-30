import click
from .config import load_config
from .schema import data_schema, all_data_schema, db_schema
from .database import create_database, import_dataset, write_to_postgres
from directory_config import DATA_DIRECTORY, DATA_CONFIGURATION_DIRECTORY, DATABASE_CONFIGURATION_DIRECTORY, DATABASE_CONNECTION_DIRECTORY

@click.command()
# @click.group()

def main():
    #Creating schema for datasets, and database.
    data_directory_path = DATA_DIRECTORY
    combined_data_yaml_path = DATA_CONFIGURATION_DIRECTORY
    combined_database_yaml_path = DATABASE_CONFIGURATION_DIRECTORY

    # Uncomment this part for the automated schema generation for the first time. ##
    # all_data_schema(data_directory_path, combined_data_yaml_path)
    
    db_schema(combined_data_yaml_path, combined_database_yaml_path)

    ##############################################################################

    #Load the configuration file
    db_config = load_config(DATABASE_CONFIGURATION_DIRECTORY)
    data_config = load_config(DATA_CONFIGURATION_DIRECTORY) 
    database_connection = load_config(DATABASE_CONNECTION_DIRECTORY)
    print(db_config)
    print(data_config)
    print(database_connection)

    #Load the database configuration (irish_db.yaml) and create database tables.
    load_dotenv() #load the .env file for the credentials. 
    database_connection["database"]["user"] = os.getenv("DB_USER")
    database_connection["database"]["password"] = os.getenv("DB_PASSWORD")
    
    create_database(database_connection, db_config)

    #Imports datasets and preprocess it. 
    datasets_dict = import_dataset(data_config)

    #Write data to PostgreSQL
    write_to_postgres(database_connection, db_config, datasets_dict)
    pass

def run():
    """Do the main work: Run the Irish pipeline."""
    click.echo("Running the Irish pipeline...")