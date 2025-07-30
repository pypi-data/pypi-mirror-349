
# Function to create database tables using the credentials from the configuration file and schema configuration from the database configuration schema file. 
def create_database(database_connection_config, database_config):
    """Create database tables using SQLAlchemy to align with df.to_sql in write_to_postgres."""
    try:
        # Create database connection using SQLAlchemy
        engine = create_engine(
            f"postgresql://{database_connection_config['database']['user']}:{database_connection_config['database']['password']}@"
            f"{database_connection_config['database']['host']}:{database_connection_config['database']['port']}/{database_connection_config['database']['db_name']}"
        )
        
        print("Database connected successfully!")

        # Iterate over tables to create them dynamically
        for table_name, table_data in database_config["tables"].items():
            columns = table_data["columns"]
            dtype_mapping = {
                col: SQLALCHEMY_TYPE_MAP.get(dtype, Text)
                for col, dtype in columns.items()
            }

            # Convert schema dictionary to DataFrame for df.to_sql()
            df_schema = pd.DataFrame(columns=columns.keys() )
            df_schema.to_sql(
                table_name, 
                engine, 
                if_exists='replace', 
                index=False, 
                dtype=dtype_mapping) 
            
            print(f"Table {table_name} has been created successfully.")

        print("All tables have been successfully created using df.to_sql.")
    except Exception as e:
        print(f"Error creating database tables: {e}")


#Function to import datasets from the YAML file and load them into Pandas DataFrames.
def import_dataset(data_config):
    """Read and load all datasets specified in the YAML file into Pandas DataFrames."""
    try:
        datasets = {} #Declare a dictionary for storing datasets names and respective dataframes. 
        
        for dataset_name, dataset_info in data_config.items():
            file_origin = dataset_info["file_origin"]
            file_path = dataset_info["path"]
            file_type = dataset_info["file_type"]
            column_name = dataset_info["columns"].items()

            #Split off simple dtypes vs. date columns
            dtype_map = {}
            parse_dates = []

            for col, typ in column_name:
                if typ in ("int64", "float64", "string", "object", "bool"):
                    dtype_map[col] = typ
                elif typ in ("datetime64"):
                    parse_dates.append(col)
                else:
                    raise ValueError(f"Unknown type {typ!r} in column {col!r}")
            

            #Read CSV and Excel files
            if file_type == "csv":
                df = pd.read_csv(
                    file_path, 
                    dtype = dtype_map, 
                    parse_dates = parse_dates, 
                    na_values = ["", " ", "NA", "null"]
                ) #Read all as string (by default).
            elif file_type == "excel":
                df = pd.read_excel(
                    file_path, 
                    engine="openpyxl", 
                    dtype = dtype_map, 
                    parse_dates = parse_dates, 
                    na_values = ["", " ", "NA", "null"])
            else:
                raise ValueError(f"Unknown type {typ!r} in column {col!r}")
            
            #Transformations (if any). It seems that file_specific script can also be associated to the file here for preprocessing and related transformations.
            
            #Example: Convert all column names to lowercase and replace '.' with '_' in names. 
            df.columns = [col.lower() for col in df.columns]
            df.columns = [col.replace('.', '_') for col in df.columns]
            df["file_name"] = file_origin #Addding the filenames in the new column.
            print(f"Following is the preprocessed column name:{df.columns}\n")


            #Store the dataset_name and respective dataframe in dictionary. 
            datasets[dataset_name] = df
            print(f"Loaded dataset: {dataset_name} | Shape: {df.shape}\n")
            print(f"Datasets data: {datasets}\n")

        return datasets
    
    except Exception as e:
        print(f"Error loading data file: {e}")
        return None


#Function to write the dataframes to the PostgreSQL database using bulk ingestion for efficiency.
def write_to_postgres(db_conn_config, db_config, datasets_dict):
    """Write DataFrame to PostgreSQL using bulk ingestion for efficiency."""
    try:
        # Create database connection using SQLAlchemy for bulk operations
        engine = create_engine(
            f"postgresql://{db_conn_config['database']['user']}:{db_conn_config['database']['password']}@"
            f"{db_conn_config['database']['host']}:{db_conn_config['database']['port']}/{db_conn_config['database']['db_name']}"
        )
        
        print("Connected to the database successfully!")
        

        # Iterate over tables
        for table_name in db_config['tables'].keys():
            if table_name in datasets_dict:
                df = datasets_dict[table_name]

                # Use df.to_sql for bulk insertion
                df.to_sql(table_name, engine, if_exists='append', index=False, method='multi')
                
                print(f"Bulk inserted data into {table_name} successfully.")

        print("Data written to PostgreSQL successfully.")
    except Exception as e:
        print(f"Error writing to PostgreSQL: {e}")
