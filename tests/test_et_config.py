# -*- coding: utf-8 -*-

"""Tests for et_config package."""

import logging
import os
import shutil
from pathlib import Path

import pytest

from et_config import Config


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



# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_Config_ctor

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof