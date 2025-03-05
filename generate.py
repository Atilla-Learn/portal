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
    items_dirs = map(lambda d: os.path.join('content', d), ['lives', 'conferences', 'talks', 'trainings'])
    templates_map = {
        'live': 'live.html',
        'conference': 'conference.html',
        'talk': 'talk.html',
        'training': 'training.html',
        'authors': 'authors.html'
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
            'gen_time': datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y à %H:%M"), # get local hour from system (for time zone)
            'git_sha1': subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                universal_newlines=True
            ).strip(),
            'num': {
                'lives': len([k for k, v in self.items.items() if v['type'] == 'live']),
                'trainings': len([k for k, v in self.items.items() if v['type'] == 'training']),
                'talks': len([k for k, v in self.items.items() if v['type'] == 'talk']),
                'conferences': len([k for k, v in self.items.items() if v['type'] == 'conference']),
                'authors' : len(self.authors)
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
                    self.authors[authorfile.split('.')[0]] = yaml.load(f.read(), Loader=yaml.FullLoader)

    def collect_items(self):
        for dir_ in self.items_dirs:
            for item_file in os.listdir(dir_):
                if item_file.endswith('.yaml'):
                    with open(os.path.join(dir_, item_file), encoding="utf-8") as f:
                        d = yaml.load(f.read(), Loader=yaml.FullLoader)
                        self.items[slugify(item_file.split('.')[0])] = d

    def render_home(self):
        template = self.env.get_template('index.html')
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding="utf-8") as f:
            f.write(template.render(
                title='ATILLA Learn',
                meta={'url': self.build_url(), 'image': self.default_image},
                **self.common_dict
            ))

    def render_landpage(self, type_, filename, title):
        if (type_ != "authors"):
            entries = [
                (k,v) for k, v in self.items.items()
                if v['type'] == type_
            ]
            entries = collections.OrderedDict(sorted(
                entries,
                key=lambda x: datetime.datetime.strptime(x[1]['date'], "%d/%m/%Y"),
                reverse=True
            ))
        else:
            entries = [
                (k,v) for k, v in self.authors.items()
            ]
            entries = collections.OrderedDict(sorted(
                entries,
                key=lambda x: x[1]['name']
            ))

        dict_ = self.common_dict.copy()

        if (type_ == 'live'):
            keywordsDict = {}
            for e in entries:
                keywordsList = entries[e]["keywords"]
                for object_ in keywordsList:
                    key = list(object_.keys())[0]
                    value = object_[key]
                    if key in keywordsDict:
                        if value not in keywordsDict[key]: keywordsDict[key].append(value)
                    else :
                        keywordsDict[key] = [value]
            dict_['keywordsDict'] = keywordsDict

        template = self.env.get_template(filename)
        with open(os.path.join(self.output_dir, filename), 'w', encoding="utf-8") as f:
            f.write(template.render(
                landpage_title=title,
                title=title,
                entries=entries,
                meta={'url': self.build_url(filename), 'image': self.default_image},
                **dict_
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

    def render_author(self, entry):
        template = self.env.get_template('author.html')
        lives, talks, conferences, trainings = {}, {}, {}, {}

        for k,v in self.items.items():
            if entry[0] in v['authors']:
                if v['type'] == 'talk':
                    talks[k] = v
                elif v['type'] == 'conference':
                    conferences[k] = v
                elif v['type'] == 'training':
                    trainings[k] = v
                elif v['type'] == 'live' :
                    lives[k] = v

        # TODO: Reverse sorting

        with open(os.path.join(self.output_dir, entry[0] + '.html'), 'w', encoding="utf-8") as f:
            f.write(template.render(
                author = entry[1],
                lives = lives,
                talks = talks,
                conferences = conferences,
                trainings = trainings,
                meta={
                    'url': self.build_url(entry[0] + '.html'),
                    'image': self.build_url('img', entry[1]['picture'])
                },
                **self.common_dict
            ))

    def render_sitemap(self):
        datestr = time.strftime('%Y-%m-%d', time.gmtime())
        endpoints = [
            '{}.html'.format(page)
            for page in ['live', 'conferences', 'trainings', 'talks'] + list(self.items.keys())
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
        self.render_landpage('live', 'lives.html', 'Lives')
        self.render_landpage('conference', 'conferences.html', 'Conférences')
        self.render_landpage('training', 'trainings.html', 'Formations')
        self.render_landpage('talk', 'talks.html', 'Talks')
        self.render_landpage('authors', 'authors.html', 'Auteurs')
        for slug, entry in self.items.items():
            self.render_item(slug, entry)
        for entry in self.authors.items():
            self.render_author(entry)
        self.render_sitemap()

if __name__ == '__main__':
    a = AtillaLearn()
    a.render()
