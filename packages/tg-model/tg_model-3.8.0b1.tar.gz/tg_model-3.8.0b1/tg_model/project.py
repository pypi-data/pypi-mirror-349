# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging

from .collection import CollectionModeler
from .util import RenderBase
from .yaml import CollectionConfigTemplate, ProjectConfig


log = logging.getLogger(__name__)


class Project(RenderBase):

    def __init__(self, projectpath, templates=None, *args, **kw):
        super().__init__(projectpath, templates=templates)
        self.templates = templates
        self.collectors = []
        self._project_config = None
        self._avatar = None
        self._xslt = None
        self._requirements = None

    @property
    def requirements(self):
        if self._requirements is None:
            self._requirements = CollectionConfigTemplate(
                projectpath=self.projectpath
            ).extracted_requirements
        return self._requirements

    @property
    def project_config(self):
        if self._project_config is None:
            self._project_config = ProjectConfig(self.projectpath)
        return self._project_config

    def render_project(self, validate=True, export=True):

        for subproject in self.project_config.content["subprojects"]:
            collection = CollectionModeler(
                subproject, self.projectpath, templates=self.templates
            )
            if validate:
                collection.validate(self.requirements)
            collection.render_collection()
            self.project_config.other_files.add_facets(collection.facets)
            if export:
                collection.export()
        self.project_config.other_files.render_all()

    def validate(self):

        for subproject in self.project_config.content["subprojects"]:
            collection = CollectionModeler(
                subproject, self.projectpath, templates=self.templates
            )
            collection.validate(self.requirements)

    def export(self):

        for subproject in self.project_config.content["subprojects"]:
            collection = CollectionModeler(
                subproject, self.projectpath, templates=self.templates
            )
            collection.export()
