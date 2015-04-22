class Website:

    def __init__(self):
        self.dh = DataHandler()

    def json_data(self):
        return self.dh.get_data()

    def json_data_with_links(self):
        return self.dh.get_data_with_links()

    def display_root(self):
        # from json import dumps
        # return dumps(self.dh.get_data(), sort_keys=True, indent=4, separators=(',', ': '))

        # http://chason.me/posts/displaying-json-data-as-a-table-using-flask/
        from flask import render_template
        return render_template('grid_render.html', data=self.dh.get_data())


class DataHandler:

    def get_data(self):
        return self.data  # .copy()

    def get_metadata(self):
        return self.meta_data  # .copy()

    def __path2url(self, path):
        # from urllib.parse import urlparse
        from urllib.request import pathname2url
        return 'file:///' + pathname2url(path.replace('\\', '/'))

    # def get_data_with_links(self):
    #     return self.data_with_links

    def __init__(self):
        import os
        from config import get_config
        cfg = get_config()
        self.base = cfg['base_dir']
        self.MAX_RATING = cfg['max_rating']
        self.data = []
        # self.data_with_links = []
        for root, dirs, files in os.walk(self.base):
            for file in files:
                if file.endswith(".pdf") or file.endswith(".PDF"):
                    relative_root = root[len(self.base):]
                    file_info = self.__get_file_info(relative_root, file, self.MAX_RATING)
                    self.data.append(
                        {
                            # 'full_path': os.path.join(root, file),
                            'path': os.path.join(relative_root, file).replace('\\', '/'),
                            'type': 'pdf',
                            'rating': file_info['rating'],
                            'year': file_info['year'],
                            'author': file_info['author'],
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

        # data with links
        # if self.data_with_links:
        #    return self.data_with_links

        # self.data_with_links = self.data.copy()
        # for i in range(0, len(self.data_with_links)):
        #     self.data_with_links[i]['full_path_link'] = '<a href="{}">{}</a>'.format(
        #         self.__path2url(self.data_with_links[i]['full_path']),
        #         self.data_with_links[i]['title']
        #     )

    def __get_file_info(self, dirs, file, max_rating=4):
        import platform
        sep = '\\' if 'Windows' == platform.system() else '/'
        dir_list = dirs.split(sep)

        year = None
        publisher = None
        author = None
        citations = 0
        title = '.'.join(file.split('.')[:-1])
        rating = 0

        meta_count = 0
        file_tags = file.split(' - ')

        # remove file extension
        file_tags[-1] = '.'.join(file_tags[-1].split('.')[:-1])
        if 2 <= len(file_tags):

            import re
            regex_year      = re.compile('^(19|20)\d{2}$')
            regex_author    = re.compile('^\([a-zA-Z]+ ?[a-zA-Z]+\)$')
            regex_citations = re.compile('^([0-9])+c\s*\[?[^]]*\]?$')
            regex_publisher = re.compile('^[a-zA-Z3]+ ?[a-zA-Z3]+$')
            regex_rating    = re.compile('^(\d{2})_')

            for tag in file_tags[1:]:
                if not year or year <= 0:
                    m = regex_year.search(tag)
                    if m:
                        year = int(m.group(0))
                        meta_count += 1
                        continue
                if not author:
                    m = regex_author.search(tag)
                    if m:
                        author = m.group(0)[1:-1]
                        meta_count += 1
                        continue
                if not citations or citations <= 0:
                    m = regex_citations.search(tag)
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
                        continue
                if not publisher:
                    m = regex_publisher.search(tag)
                    if m:
                        publisher = m.group(0)
                        meta_count += 1
                        continue
            if 0 < meta_count:
                title = ' - '.join(file_tags[:-meta_count])

            # get rating
            m = regex_rating.search(title)
            if m:
                try:
                    rating = max_rating - int(m.group()[:2])
                except:
                    from sys import stderr as sys_stderr
                    print('WARNING: Invalid rating found in', title, file=sys_stderr)
                title = title[3:]

        res = {
            'year': year, 'author': author, 'publisher': publisher,
            'citations': citations, 'title': title, 'rating': rating
        }
        return res
