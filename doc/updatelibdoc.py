#!/usr/bin/env python
# -*- coding: utf-8 -*-
# YAFF is yet another force-field code.
# Copyright (C) 2011 Toon Verstraelen <Toon.Verstraelen@UGent.be>,
# Louis Vanduyfhuys <Louis.Vanduyfhuys@UGent.be>, Center for Molecular Modeling
# (CMM), Ghent University, Ghent, Belgium; all rights reserved unless otherwise
# stated.
#
# This file is part of YAFF.
#
# YAFF is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# YAFF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


from __future__ import print_function

import os
import importlib
from glob import glob
from io import StringIO

from common import write_if_changed


def discover():
    # find packages
    packages = {'yaff': []}
    for fn in glob('../yaff/*/__init__.py'):
        subpackage = fn.split('/')[2]
        if subpackage == 'test':
            continue
        packages['yaff.%s' % subpackage] = []
    # find modules
    for package, modules in packages.items():
        stub = package.replace('.', '/')
        for fn in glob('../%s/*.py' % stub) + glob('../%s/*.so' % stub):
            module = fn.split('/')[-1][:-3]
            if module == '__init__':
                continue
            modules.append(module)

    return packages


def get_first_docline(module):
    m = importlib.import_module(module)
    if m.__doc__ is not None:
        lines = m.__doc__.split('\n')
        if len(lines) > 0:
            return lines[0]
    return 'FIXME! Write module docstring.'


def underline(line, char, f):
    f.write(line + u'\n')
    f.write(char*len(line) + u'\n')
    f.write(u'\n')


def main():
    packages = discover()

    # Write new/updated rst files if needed
    fns_rst = []
    for package, modules in sorted(packages.items()):
        # write the new file to a StringIO
        f = StringIO()
        f.write(u'..\n')
        f.write(u'    This file is automatically generated. Do not make\n')
        f.write(u'    changes as these will be overwritten. Rather edit\n')
        f.write(u'    the docstrings in the source code.\n')
        f.write(u'\n')
        underline('``%s`` -- %s' % (package, get_first_docline(package)), '#', f)
        f.write(u'\n')

        for module in sorted(modules):
            f.write(u'\n')
            f.write(u'\n')
            full = package + '.' + module
            underline(u'``%s`` -- %s' % (full, get_first_docline(full)), '=', f)
            f.write(u'.. automodule:: ' + full + '\n')
            f.write(u'    :members:\n')

        # write if the contents have changed
        fn_rst = 'rg_%s.rst' % package.replace('.', '_')
        fns_rst.append(fn_rst)
        write_if_changed(fn_rst, f.getvalue())


    # Remove other rst files
    for fn_rst in glob('rg_yaff*.rst'):
        if fn_rst not in fns_rst:
            print('Removing %s' % fn_rst)
            os.remove(fn_rst)


if __name__ == '__main__':
    main()
