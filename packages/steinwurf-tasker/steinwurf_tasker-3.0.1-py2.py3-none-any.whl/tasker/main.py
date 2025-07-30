# ! /usr/bin/env python
# encoding: utf-8
from invoke import Collection, Program
from invoke import Config

from . import project_tasks
from . import vpn_tasks
from . import waf_tasks


class SteinwurfTaskerConfig(Config):
    prefix = "steinwurf-tasker"
    env_prefix = "SW"


VERSION = "3.0.1"

collection = Collection()

collection.add_collection(Collection.from_module(project_tasks, name="project"))
collection.add_collection(Collection.from_module(vpn_tasks, name="vpn"))
collection.add_collection(Collection.from_module(waf_tasks, name="waf"))

program = Program(
    config_class=SteinwurfTaskerConfig, namespace=collection, version=VERSION
)
