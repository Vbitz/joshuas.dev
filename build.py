#!/usr/bin/env python3

import os
from absl import app, logging, flags
from subprocess import check_call
import json
import yaml

PANDOC = "pandoc"

SITE_NAME = "joshuas.dev"


def resolve_path(*args):
    return os.path.abspath(os.path.join(*args))


TEMPLATES_PATH = resolve_path(os.path.dirname(__file__), "templates")

PUBLIC_PATH = resolve_path(os.path.dirname(__file__), "docs")

HTML_TEMPLATE_PATH = resolve_path(TEMPLATES_PATH, "post.html")


def pandoc_call(input_filename, output_filename, output_type, template_filename):
    pandoc_args = [PANDOC,
                   "--template", template_filename,
                   "-t", output_type,
                   "-o", output_filename,
                   input_filename]

    logging.info("PANDOC: %s", pandoc_args)

    check_call(pandoc_args)


def get_post_list():
    with open("posts.json", "r") as file_handle:
        return json.load(file_handle)


def extract_metadata(filename):
    with open(filename, "r") as file_handle:
        front_matter, content = list(yaml.load_all(
            file_handle, Loader=yaml.FullLoader))[:2]

        return front_matter


def main(args):
    logging.info("Starting Build for %s", SITE_NAME)

    post_list = get_post_list()

    for post in post_list:
        logging.info("Building Post %s", post)

        post_path = resolve_path(post)

        post_metadata = extract_metadata(post_path)

        output_filename = os.path.splitext(post)[0] + ".html"

        logging.info("Writing output to %s", output_filename)

        pandoc_call(post_path, resolve_path(
            PUBLIC_PATH, output_filename), "html", HTML_TEMPLATE_PATH)


if __name__ == "__main__":
    app.run(main)
