# -*- coding: utf-8 -*-

"""Tests for et_config package."""

import logging
import os,sys
import shutil
from pathlib import Path

import pytest

sys.path.insert(0, '.')
from et_config import Config, get_param

__test_workspace__ = (Path(__file__) / '../../test_workspace').resolve()


def clear_test_workspace(folder=None):
    """If dir is None, clear the test workspace by removing it and recreating it.
    Otherwise, only remove directory folder
    """
    if 'VSC_HOME' in os.environ:
        # see https://stackoverflow.com/questions/58943374/shutil-rmtree-error-when-trying-to-remove-nfs-mounted-directory
        logging.shutdown()

    if not folder is None:
        p = __test_workspace__ / folder
        if p.exists():
            shutil.rmtree(p)
    else:
        if __test_workspace__.exists():
            shutil.rmtree(__test_workspace__)

    __test_workspace__.mkdir(exist_ok=True)


def test_Config_ctor():
    """Test Config ctor."""
    clear_test_workspace()

    cfg = Config(first_name='bert',name='tijskens')
    assert cfg.data['first_name'] == 'bert'
    assert cfg.data['name'] == 'tijskens'

    cfg.save(__test_workspace__ / '.cfg')

    cfg_copy = Config(file_loc=__test_workspace__ / '.cfg')
    cfg_copy.add(address='home')
    print(cfg_copy)
    with pytest.raises(FileNotFoundError):
        print('Exception expected:')
        cfg_copy.save(__test_workspace__ / 'address/.cfg')

    cfg_copy.save(__test_workspace__ / 'address/.cfg', mkdir=True)


def test_micc2_cfg():
    """"""
    clear_test_workspace()
    # first time setup

    initial_preferences = {
        "full_name": {
            "default": "Bert Tijskens",
            "text": "your full name"
        },
        "email": {
            "text": "your e-mail address"
        },
        # "github_username": {
        #     "default": "etijskens",
        #     "text": "your github username (leave empty if you do not have one,\n  or create one at https://github.com/join)"
        # },
        # "version": {
        #     "default": "0.0.0",
        #     "text": "the initial version number of a new project"
        # },
        # "github_repo": {
        #     "default": "{{ cookiecutter.project_name }}",
        #     "text": "github repo for this project"
        # },
        # "default_branch": {
        #     "default": "master",
        #     "text": "default git branch"
        # },
        # "python_version": {
        #     "default": "3.7",
        #     "text": "default minimal Python version"
        # },
        # "sphinx_html_theme": {
        #     "default": "sphinx_rtd_theme",
        #     "text": "Html theme for sphinx documentation"
        # },
        "software_license": {
            "choices": ['MIT license', 'BSD license', 'ISC license', 'Apache Software License 2.0', 'GNU General Public License v3', 'Not open source'],
            "text": "default software license"
        }
    }
    for name,v in initial_preferences.items():
        value = get_param(name, v)
        print(value)

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_micc2_cfg

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof