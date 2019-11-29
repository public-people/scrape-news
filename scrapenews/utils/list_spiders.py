#!/usr/bin/env python
"""
List available spiders as names and classes.
"""
from __future__ import print_function
from scrapy import spiderloader
from scrapy.utils import project


def get_spiders():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    names = spider_loader.list()

    return {name: spider_loader.load(name) for name in sorted(names)}


def test():
    spiders = get_spiders()

    print("Name                 |  Class")
    print("---------------------+-------")
    for k, v in spiders.items():
        print("{:20} | {}".format(k, v.__name__))


if __name__ == '__main__':
    test()
