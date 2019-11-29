#!/usr/bin/env python
"""
List available spiders as names and classes.

Based on:
    https://stackoverflow.com/questions/46871133/get-all-spiders-class-name-in-scrapy/46871206
"""
from __future__ import print_function
from scrapy import spiderloader
from scrapy.utils import project


def get_spiders():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    names = spider_loader.list()

    return {name: spider_loader.load(name) for name in sorted(names)}


def print_table():
    spiders = get_spiders()

    print("Name                 |  Class")
    print("---------------------+-------")
    for k, v in spiders.items():
        print("{:20} | {}".format(k, v.__name__))


def print_list():
    spiders = get_spiders()

    for k in sorted(spiders.keys()):
        print(k)


if __name__ == '__main__':
    print_list()
