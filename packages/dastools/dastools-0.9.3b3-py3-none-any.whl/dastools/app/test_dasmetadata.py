#!/usr/bin/env python3

###################################################################################################
# (C) 2021 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences, Potsdam, Germany  #
#                                                                                                 #
# This file is part of dastools.                                                                  #
#                                                                                                 #
# dastools is free software: you can redistribute it and/or modify it under the terms of the GNU  #
# General Public License as published by the Free Software Foundation, either version 3 of the    #
# License, or (at your option) any later version.                                                 #
#                                                                                                 #
# dastools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without   #
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU   #
# General Public License for more details.                                                        #
#                                                                                                 #
# You should have received a copy of the GNU General Public License along with this program. If   #
# not, see https://www.gnu.org/licenses/.                                                         #
###################################################################################################

"""Tests to check that dasmetadata.py is working

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

   :Copyright:
       2019-2021 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences, Potsdam, Germany
   :License:
       GPLv3
   :Platform:
       Linux

.. moduleauthor:: Javier Quinteros <javier@gfz-potsdam.de>, GEOFON, GFZ Potsdam
"""
import os

from click.testing import CliRunner
from dastools.app.dasmetadata import printmetadata
from dastools.app.dasmetadata import create
import json
import os
from io import StringIO

"""Test the functionality of dasmetadata.py

"""


def test_create_optodas():
    # runner = CliRunner()
    output = os.popen('dasmetadata create --directory . --experiment example --inputfmt optodas').read()
    # result = runner.invoke(create, ['--directory', '.', '--experiment', 'example', '--inputfmt', 'optodas'])
    # assert result.exit_code == 0
    print(len(output))
    print(output)
    data = json.loads(output)
    assert data['network_code'] == 'XX'
    assert data['start_date'] == "2022-04-22"
    assert data['end_date'] == "2022-04-22"
    assert data['interrogators'][0]['manufacturer'] == 'Alcatel'
    assert data['interrogators'][0]['acquisitions'][0]["acquisition_start_time"] == "2022-04-22T07:55:50"
    assert data['interrogators'][0]['acquisitions'][0]["acquisition_end_time"] == "2022-04-22T07:55:59.987500"


def test_create_tdms():
    # runner = CliRunner()
    output = os.popen('dasmetadata create --directory . --experiment PDN_1km --inputfmt tdms').read()
    print(len(output))
    print(output)
    data = json.loads(output)
    assert data['network_code'] == 'XX'
    assert data['start_date'] == "2018-09-05"
    assert data['end_date'] == "2018-09-05"
    assert data['interrogators'][0]['manufacturer'] == 'Silixa'
    assert data['interrogators'][0]['acquisitions'][0]["acquisition_start_time"] == "2018-09-05T09:55:03.298000"
    assert data['interrogators'][0]['acquisitions'][0]["acquisition_end_time"] == "2018-09-05T09:57:03.297000"


def test_create_empty():
    runner = CliRunner()
    result = runner.invoke(create, ['--empty'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert 'network_code' in data.keys()
    assert 'principal_investigator_name' in data.keys()
    assert 'interrogators' in data.keys()
    assert 'acquisitions' in data['interrogators'][0]
    assert 'cables' in data.keys()
    assert 'fibers' in data['cables'][0]


def test_printmetadata(capsys):
    out = StringIO()
    printmetadata(('Sampling Rate', '1000'), stream=out)
    assert out.getvalue() == "('Sampling Rate', '1000')\n"

    out = StringIO()
    printmetadata({'Sampling Rate': '1000'}, stream=out)
    assert out.getvalue() == "{'Sampling Rate': '1000'}\n"
