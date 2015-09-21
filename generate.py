import os
import calendar
import time
import subprocess

from jinja2 import Environment, PackageLoader
from slugify import slugify
import yaml

class AtillaLearn:
    output_dir = 'web/'
    authors_files = 'content/authors/'
    items_dirs = map(lambda d: 'content/' + d, ['conferences', 'talks', 'trainings'])
    templates_map = {
        'conference': 'conference.html',
        'talk': 'talk.html',
        'training': 'training.html'
    }
    
    def __init__(self):
        # Jinja stuff
        self.env = Environment(loader=PackageLoader('generate', 'templates'))

        # Content stuff
        self.authors = {} # nick -> infos dict
        self.items = {} # slug -> infos dict

        self.collect_authors()
        self.collect_items()
        
        # Nerd stuff
        self.nerd_dict = {
            'gen_time': calendar.timegm(time.gmtime()),
            'git_sha1': subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                universal_newlines=True
            ).strip()
        }

    def collect_authors(self):
        for authorfile in os.listdir(self.authors_files):
            if authorfile.endswith('.yaml'):
                with open(self.authors_files + authorfile) as f:
                    self.authors[authorfile.split('.')[0]] = yaml.load(f.read())

    def collect_items(self):
        for dir_ in self.items_dirs:
            for item_file in os.listdir(dir_):
                if item_file.endswith('.yaml'):
                    with open(dir_ + '/' + item_file) as f:
                        d = yaml.load(f.read())
                        self.items[slugify(item_file.split('.')[0])] = d

    def render_home(self):
        template = self.env.get_template('index.html')
        with open(self.output_dir + 'index.html', 'w') as f:
            f.write(template.render(title='Atilla Learn', **self.nerd_dict))

    def render_landpage(self, type_, filename, title):
        entries = {
            k: v for k, v in self.items.items()
            if v['type'] == type_
        }
        template = self.env.get_template(filename)
        with open(self.output_dir + filename, 'w') as f:
            f.write(template.render(landpage_title=title, title=title, entries=entries, **self.nerd_dict))

    def render_item(self, slug, entry):
        if entry['type'] not in self.templates_map:
            raise ValueError('{} is not a valid item type.'.format(entry['type']))
        tpl = self.templates_map[entry['type']]

        authors = {
            k: v for k, v in self.authors.items()
            if k in entry['authors']
        }

        template = self.env.get_template(tpl)
        with open(self.output_dir + slug + '.html', 'w') as f:
            f.write(template.render(entry=entry, authors=authors, **self.nerd_dict))

    def render(self):
        self.render_home()
        self.render_landpage('conference', 'conferences.html', 'Conférences')
        self.render_landpage('training', 'trainings.html', 'Formations')
        self.render_landpage('talk', 'talks.html', 'Talks')
        for slug, entry in self.items.items():
            self.render_item(slug, entry)
        

if __name__ == '__main__':
    a = AtillaLearn()
    a.render()
    


