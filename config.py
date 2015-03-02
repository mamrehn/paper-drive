
def get_config():
    config_data = {}
    config_data['debug'] = True
    config_data['base_dir'] = 'C:\\Users\\username\\Google Drive\\Students\\Paper collection\\'
    config_data['max_rating'] = 4

    # config_data['resource_download_and_bundle'] = {
    #     'is_active': True,
    #     'js': [
    #         'https://code.angularjs.org/snapshot/angular.js',
    #         'https://code.angularjs.org/snapshot/angular-touch.js',
    #         'https://code.angularjs.org/snapshot/angular-animate.js',
    #         'http://ui-grid.info/docs/grunt-scripts/csv.js',
    #         'http://ui-grid.info/docs/grunt-scripts/pdfmake.js',
    #         'http://ui-grid.info/docs/grunt-scripts/vfs_fonts.js',
    #         'http://ui-grid.info/release/ui-grid-unstable.js',
    #         'static/js/mygrid.js'
    #     ]
    # }

    # debug options
    config_data['_save_data_as_static_json'] = {
        'is_active': True,
        'path': config_data['base_dir'] + '..\\.static_db.json'
    }

    return config_data