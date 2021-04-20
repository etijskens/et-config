# -*- coding: utf-8 -*-
"""
Package et_config
=======================================

A 'hello world' example.
"""
__version__ = "0.0.0"

from pathlib import Path
import json

class Config:
    """Class for configuration (or preferences) files.

    In fact little more than a persistent dict."""

    # this key controls the file location of the Config file
    file_key = 'file_loc'

    def __init__(self, **kwargs ):
        """"""
        self.data = {}

        if not kwargs:
            self.load(p_cfg=None)
        else:
            if Config.file_key in kwargs:
                # Read Config object data
                p_cfg = Path(kwargs[Config.file_key])
                self.load(p_cfg)

            # Add the other kwargs
            kwargs.pop(Config.file_key,None)
            self.add(**kwargs)

    def load(self, p_cfg=None):
        """

        :param Path p_cfg: path to cfg file
        """
        if p_cfg is None:
            # first look into

        self.p_cfg = p_cfg.resolve()
        with p_cfg.open() as fp_cfg:
            data = json.load(fp_cfg)
            self.data.update(data)

        self.update_location_(p_cfg)


    def save(self, file='', mkdir=False):
        """Save self.data to cfg file."""
        p_cfg = self.p_cfg if not file else Path(file)
        p_cfg = p_cfg.resolve()
        if not p_cfg.parent.exists():
            if mkdir:
                p_cfg.parent.mkdir()
            else:
                print(f'Inexisting Path: {p_cfg.parent}. Create it yourself, or use the "mkdir=True" parameter.')
                raise FileNotFoundError()
        self.update_location_(p_cfg)

        with p_cfg.open('w') as fp_cfg:
            json.dump(self.data, fp_cfg, indent=2)


    def add(self, **kwargs):
        self.data.update(kwargs)


    # "Private" methods: For internal use only.
    def update_location_(self, p_cfg):
        """Make sure self.data[Config.file_key] points to the correct location, i.e. where the Config object was
        Read from or written to.

        For internal use only.
        """
        self.data[Config.file_key] = str(p_cfg)


    def __str__(self):
        return json.dumps(self.data,indent=2)


    def __getitem__(self, item):
        return self.data[item]


    def __setitem__(self, key, value):
        self.data[key] = value

# eof
