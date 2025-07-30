# Collaborative_Research_Center_Development_Pipeline

This repository contains the complete Data Science pipeline for CRC development. It documents the entire process, from importing data from OwnCloud to performing analysis on Metabase, covering all the involved steps.

# Functions of Different Files

* `main.ipynb` is the central file which loads the configuration file and create the necessary tables in the database based on the data types specified in the `file_configuration.yaml` file.
* The folder ``config`` contains different  ``.yaml`` files. The ``database_connection.yaml`` files is created for the connection to the postgres database. The ``combined_irish_data.yaml`` and ``combined_irish_database.yaml`` is automatically created schema and database configuration files based on the CSV and Excel files provided.
