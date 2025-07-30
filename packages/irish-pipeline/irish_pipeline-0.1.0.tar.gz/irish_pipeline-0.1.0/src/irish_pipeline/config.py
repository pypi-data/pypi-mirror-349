def load_config(config_file_path): #file path of irish_data.yaml file
    """Load YAML configuration file."""
    with open(config_file_path, 'r') as file: #opening the file in the read mode.
        print(f"Following Configuration files has been loaded successfully: \n{file}")
        return yaml.safe_load(file) #loading the cofiguration_yaml file. 