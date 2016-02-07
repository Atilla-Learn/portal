import os
import datetime
import collections
import subprocess
import time

from jinja2 import Environment, PackageLoader
from slugify import slugify
import yaml

# TODO(thooms): better template parameters (dict builder)

class AtillaLearn:
    output_dir = 'web'
    authors_dir = 'content/authors'
    items_dirs = map(lambda d: os.path.join('content', d), ['conferences', 'talks', 'trainings'])
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

        # Common stuff
        self.common_dict = {
            'gen_time': datetime.datetime.now(),
            'git_sha1': subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                universal_newlines=True
            ).strip(),
            'num': {
                'trainings': len([k for k, v in self.items.items() if v['type'] == 'training']),
                'talks': len([k for k, v in self.items.items() if v['type'] == 'talk']),
                'conferences': len([k for k, v in self.items.items() if v['type'] == 'conference'])
            }
        }

        self.domain = 'http://learn.atilla.org'
        self.default_image = self.build_url('img', 'prompt.png')

    def build_url(self, *components):
        return os.path.join(self.domain, *components)

    def collect_authors(self):
        for authorfile in os.listdir(self.authors_dir):
            if authorfile.endswith('.yaml'):
                with open(os.path.join(self.authors_dir, authorfile), encoding="utf-8") as f:
                    self.authors[authorfile.split('.')[0]] = yaml.load(f.read())

    def collect_items(self):
        for dir_ in self.items_dirs:
            for item_file in os.listdir(dir_):
                if item_file.endswith('.yaml'):
                    with open(os.path.join(dir_, item_file), encoding="utf-8") as f:
                        d = yaml.load(f.read())
                        self.items[slugify(item_file.split('.')[0])] = d

    def render_home(self):
        template = self.env.get_template('index.html')
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding="utf-8") as f:
            f.write(template.render(
                title='Atilla Learn',
                meta={'url': self.build_url(), 'image': self.default_image},
                **self.common_dict
            ))

    def render_landpage(self, type_, filename, title):
        entries = [
            (k,v) for k, v in self.items.items()
            if v['type'] == type_
        ]
        entries = collections.OrderedDict(sorted(
            entries,
            key=lambda x: datetime.datetime.strptime(x[1]['date'], "%d/%m/%Y"),
            reverse=True
        ))
        template = self.env.get_template(filename)
        with open(os.path.join(self.output_dir, filename), 'w', encoding="utf-8") as f:
            f.write(template.render(
                landpage_title=title,
                title=title,
                entries=entries,
                meta={'url': self.build_url(filename), 'image': self.default_image},
                **self.common_dict
            ))

    def render_item(self, slug, entry):
        if entry['type'] not in self.templates_map:
            raise ValueError('{} is not a valid item type.'.format(entry['type']))
        tpl = self.templates_map[entry['type']]

        authors = {
            k: v for k, v in self.authors.items()
            if k in entry['authors']
        }

        title = entry['title']
        template = self.env.get_template(tpl)
        with open(os.path.join(self.output_dir, slug + '.html'), 'w', encoding="utf-8") as f:
            f.write(template.render(
                title=title,
                entry=entry,
                authors=authors,
                meta={
                    'url': self.build_url(slug + '.html'),
                    'image': self.build_url('img', entry['image'])
                },
                **self.common_dict
            ))

    def render_sitemap(self):
        datestr = time.strftime('%Y-%m-%d', time.gmtime())
        endpoints = [
            '{}.html'.format(page)
            for page in ['conferences', 'trainings', 'talks'] + list(self.items.keys())
        ]
        pages = [
            {'url': self.build_url(endpoint), 'lastmod': datestr}
            for endpoint in endpoints
        ]
        template = self.env.get_template('sitemap.xml')
        with open(os.path.join(self.output_dir, 'sitemap.xml'), 'w', encoding="utf-8") as f:
            f.write(template.render(pages=pages))


    def render(self):
        self.render_home()
        self.render_landpage('conference', 'conferences.html', 'Conférences')
        self.render_landpage('training', 'trainings.html', 'Formations')
        self.render_landpage('talk', 'talks.html', 'Talks')
        for slug, entry in self.items.items():
            self.render_item(slug, entry)
        self.render_sitemap()

if __name__ == '__main__':
    a = AtillaLearn()
    a.render()
