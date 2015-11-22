# ATILLA's learning portal

Python-generated static website, with `materialize.css` design.

# How to get a working instance

* Clone the repo
* `pyvenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `python generate.py`
* `bower install` 

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
