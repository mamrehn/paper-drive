__author__ = 'Mario Amrehn'

class Website:

    def __init__(self):
        self.dh = DataHandler()

    def json_data(self):
        return self.dh.get_data()

    def json_data_with_links(self):
        return self.dh.get_data_with_links()

    def display_root(self):
        #from json import dumps
        #return dumps(self.dh.get_data(), sort_keys=True, indent=4, separators=(',', ': '))

        # http://chason.me/posts/displaying-json-data-as-a-table-using-flask/
        from flask import render_template
        return render_template('grid_render.html', data=self.dh.get_data())


class DataHandler:

    def get_data(self):
        return self.data #.copy()

    def get_metadata(self):
        return self.meta_data #.copy()

    def get_data_with_links(self):
        if self.data_with_links:
            return self.data_with_links
        self.data_with_links = self.data.copy()
        for i in range(0, len(self.data_with_links)):
            self.data_with_links[i]['full_path_link'] = '<a href="file:///{}">{}</a>'.format(
                self.data_with_links[i]['full_path'],
                self.data_with_links[i]['title']
            )
        return self.data_with_links

    def __init__(self):
        import os
        from config import get_config
        self.base = get_config()['base_dir']
        self.data = []
        self.data_with_links = []
        for root, dirs, files in os.walk(self.base):
            for file in files:
                if file.endswith(".pdf"):
                    relative_root = root[len(self.base):]
                    file_info = self.__get_file_info(relative_root, file)
                    self.data.append(
                        {
                            'full_path': os.path.join(root, file),
                            'path': os.path.join(relative_root, file),
                            'type': 'pdf',
                            'year': file_info['year'],
                            'publisher': file_info['publisher'],
                            'citations': file_info['citations'],
                            'title': file_info['title']
                        }
                    )
                    # test
                    if not file_info['title']:
                        print(self.data[-1])
        self.meta_data = {
            'length': len(self.data),
            'base': self.base
        }

    def __get_file_info(self, dirs, file):
        import platform
        sep = '\\' if 'Windows' == platform.system() else '/'
        dir_list = dirs.split(sep)

        year = None
        publisher = None
        citations = 0
        title = '.'.join(file.split('.')[:-1])

        meta_count = 0
        file_tags = file.split(' - ')

        # remove file extention
        file_tags[-1] = '.'.join(file_tags[-1].split('.')[:-1])
        if 2 <= len(file_tags):

            import re
            for tag in file_tags[1:]:
                if not year or year <= 0:
                    m = re.search('^(19|20)\d{2}$', tag)
                    if m:
                        year = int(m.group(0))
                        meta_count += 1
                if not citations or citations <= 0:
                    m = re.search('^([0-9])+c\s*\[?[^]]*\]?$', tag)
                    if m:
                        t = 0
                        try:
                            t = int(m.group(0))
                        except:
                            try:
                                t = int(m.group(0)[0:-1])
                            except:
                                if 0 < m.lastindex:
                                    t = int(m.group(1))
                        citations = t
                        meta_count += 1
                if not publisher:
                    m = re.search('^[a-zA-Z]+$', tag)
                    if m:
                        publisher =  m.group(0)
                        meta_count += 1
            if 0 < meta_count:
                title = ' - '.join(file_tags[:-meta_count])
        return {'year': year, 'publisher': publisher, 'citations': citations, 'title': title}
