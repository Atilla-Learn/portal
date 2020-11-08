# ATILLA's learning portal

Python-generated static website, with `materialize.css` design.

# How to get a working instance

* Clone the repo
```
$ virtualenv -p `which python3` venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python generate.py
$ bower install
```

# Structure of the repo

* `content/` author files and item files (each item is either a conf, a talk, or a training)
* `generate.py` main generation script
* `templates/` templates directory
* `web/` output directory, contains the static files (images, js and
  so on), and the `.html` files after generation.

# How to add an author file

* Add the right `.yaml` entry in `content/authors`
* The name of the file is understood as the author nick by the generator
* The file should respect the following schema:

    ```
    name: Complete Name
    email: some@email.com
    picture: mdr.png
    ```

* Please bear in mind that the author picture will be fetched in the
  `web/img/authors/` directory.

* Option : the author can add its formation and a description :

    ```
    name: Complete Name
    email: some@email.com
    picture: mdr.png
    more:
      formation: My awesome formation
      description: Description of my awesome self
    ```

# How to add a training/talk/conference

* Add the right `.yaml` entry in the concerned subfolder of `content/`
* The name of the file doesn't really matter
* The file should respect the following schema:

    ```
    type: either conference, training, or talk
    title: A title
    date: the date of the item
    image: lololol.png # will be printed out in the item list, and fetched in web/img/
    short: a short and catchy summary for the talk/conf/..
    replay_id: a Youtube ID for the replay (or nothing if there's none)
    authors:
      - author1
      - author2
    description: a full description
    links:
      - type: video, or http, or book
        text: link text
        link: proper link
        source: youtube, NASA, whatever
        author: you know the drill
    slides:
      link: http://link_to_online_version_of_slides.com
      git: http://link_to_source_of_slides.org
    ```
# How to add a live

* Add the right `.yaml` entry in the concerned subfolder of `content/`
* The name of the file doesn't really matter
* The file should respect the following schema:

    ```
    type: live
    title: A title
    date: the date of the item
    image: lololol.png # will be printed out in the item list, and fetched in web/img/
    short: a short and catchy summary for the live
    replay_id: ID of the Youtube video, if there is one
    peertube_id: 
      - the ID of the Peertube video
      - the ID of the second part of the live if needed
      - will you really need a third part ? If so, you can put its ID here
    authors:
      - author1
      - author2
    description: a full description
    keywords:
      - formation: ing1/ing2/ing3
      - cursus: genie-informatique/genie-mathematiques/you know what I'm talking about
      - category: informatique/mathematiques/other(you can be specific)
      - another type of keyword if you feel the need to add it
    links:
      - type: video, or http, or book
        text: link text
        link: proper link
        source: youtube, NASA, whatever
        author: you know the drill
    slides:
      link: http://link_to_online_version_of_slides.com
      git: http://link_to_source_of_slides.org
    ```

* Please keep in mind that you can add as many keywords as you want, but that
* keywords label must each have the structure of a css class as it will
* affect the filter (ex : Génie Informatique >> genie-informatique)