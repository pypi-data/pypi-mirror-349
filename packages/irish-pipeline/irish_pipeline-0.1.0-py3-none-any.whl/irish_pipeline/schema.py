# Schema Generation for CSV and Excel Files individually
def data_schema(file_path, data_yaml_path=None): # by default, it is processing one CSV file and getting the schema.
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        file_type = 'csv'
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
        file_type = 'excel'
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel files.")
    
    # Minor preprocessing to make the column names standard.
    df.columns = [col.lower() for col in df.columns]  # converting the columns to lower_case.
    df.columns = [col.replace('.', '_') for col in df.columns]

    # Extract the column names and data types.
    columns = {col: str(df[col].dtype) for col in df.columns}

    # Add extra column "filename" with the type "string"
    columns["file_name"] = "string"

    # Add the metadata information to the schema.
    dataset_name = os.path.splitext(os.path.basename(file_path))[0] #splitting file path into a tuple and taking the first element.
    schema = {
        dataset_name: {
                'file_origin': os.path.basename(file_path),
                'path': file_path,
                'file_type': file_type,
                'columns': columns
        }
    }

    #If a YAML path is provided, write to the file. 
    if data_yaml_path:
        # Write to file_name.yaml with proper indentation.
        with open(data_yaml_path, 'w') as yaml_file:
            yaml.dump(schema, yaml_file, default_flow_style=False, indent=4, sort_keys=False) #write te schema to yaml file in block style for readability, and do not sort the keys.)
        
        print(f"YAML schema saved  to {data_yaml_path} file.")
    
    return schema


# Schema Generation for All CSV and Excel Files in a Directory
def all_data_schema(directory_path, output_yaml_path):
    #Getting the folders and files in the directory. 
    if not os.path.isdir(directory_path):
        raise ValueError(f"The provided {directory_path} is not a valid directory.")
    
    combined_schema = {} # dictionarry to hold the combined schema for all files
    
    #iterate through the directory, sub-direcctories and process each file. 
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            #Process each each CSV and Excel files
            if file_name.endswith(('.csv', '.xlsx', '.xls')):
                try:
                    #Use the existing schema generating function.
                    schema = data_schema(file_path, None) # Only write to output_yaml after getting combined schema

                    #Add the schema to the combined dictionary. 
                    combined_schema.update(schema)

                except Exception as e:
                    print(f"Error processing file '{file_name}':{e}")

    # Write the combined schema to the output YAML file
    with open(output_yaml_path, 'w') as yaml_file:
        yaml.dump(combined_schema, yaml_file, default_flow_style=False, indent=4, sort_keys=False)
        
    print(f"Combined schema saved to {output_yaml_path} file.")


# Schema Generation for Database based on the data schema
def db_schema(data_yaml, db_yaml):
    try:
        with open(data_yaml, 'r') as data_file:
            data_schema = yaml.safe_load(data_file)
    except FileNotFoundError:
        print(f"Error: File {data_yaml} not found.")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {data_yaml}: {e}")
        return

    #Initialize the database schema. 
    db_schema = {'tables':{}}

    #Mapping of Pandas data types to SQLAlchemy data types.
    pandas_to_sqlalchemy_dtype = {
        'object': 'Text', 
        'string': 'Text',
        'int64': 'Integer', 
        'int32': 'Integer',
        'float64': 'Float',
        'float32': 'Float', 
        'bool': 'Boolean', 
        'datetime64[ns]': 'DateTime', #with nanoseconds precision
        'timedelta64[ns]': 'Text' # For time differences, which are not directly supported in SQLAlchemy
    }


    #Iterate over the datasets in the data schema and create the database schema. 
    for dataset_name, dataset_info in data_schema.items():
        table_name = dataset_name
        columns = dataset_info['columns']

        #Convert Pandas data types to PostgreSQL data types. 
        converted_columns = {col: pandas_to_sqlalchemy_dtype.get(dtype, 'TEXT') for col, dtype in columns.items()} #Default dtype is TEXT

        #Add the table schema to the database schema. 
        db_schema['tables'][table_name] = {
            'columns': converted_columns
        }

    #Write the database schema to the db_schema.yaml file. 
    with open(db_yaml, 'w') as db_file:
        yaml.dump(db_schema, db_file, default_flow_style = False, indent = 4, sort_keys = False) # not to sort the elements in the database schema. 

    print(f"Database Configuration saved to {db_yaml} file.")
