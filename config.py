
def get_config():
    config_data = {}
    config_data['debug'] = True
    config_data['base_dir'] = 'C:\\Users\\z0032d6f\\Google Drive\\Students\\Paper collection\\'
    config_data['max_rating'] = 4

    # debug options
    config_data['_save_data_as_static_json'] = {'is_active': True, 'path': config_data['base_dir'] + '..\\.static_db.json'}

    return config_data