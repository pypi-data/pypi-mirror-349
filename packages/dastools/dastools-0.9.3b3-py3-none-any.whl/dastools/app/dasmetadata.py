#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""dasmetadata tool

This file is part of dastools.

dastools is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

dastools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If
not, see https://www.gnu.org/licenses/.

   :Copyright:
       2021-2023 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences, Potsdam, Germany
   :License:
       GPLv3
   :Platform:
       Linux

.. moduleauthor:: Javier Quinteros <javier@gfz-potsdam.de>, GEOFON, GFZ Potsdam
"""

import click
import sys
import json
from pprint import pprint
from typing import Literal
from pydantic import ValidationError
from dastools.input import str2class
from dastools.input import checkDASdata
from dastools import __version__
from dastools.utils import str2date
from dastools.utils import printmetadata
from dastools.utils import dasrcn2stationxml
from dastools.utils import dasrcn2datacite
from dastools.utils import kml2channels
from dastools.basemodels import DASMetadata
from dastools.basemodels import ChannelGroupModel


dasclasses = ['OptoDAS', 'TDMS']


@click.group()
def cli():
    pass


@click.command()
@click.option('--infile', type=click.File('rt'), default=sys.stdout,
              help='Input file in JSON format as proposed by the DAS-RCN group.')
@click.option('--coords', type=str, default=None,
              help='KML file with coordinates for each channel')
@click.option('--gain', type=float, default=1.0,
              help='Gain to be included in the response of the StationXML file')
@click.option('--outfile', type=click.File('wt'), default=sys.stdout,
              help='File where the stationXML data should be saved')
@click.option('--outputfmt', type=click.Choice(['StationXML', 'Datacite'], case_sensitive=False),
              help='Format of the file to generate', default='Datacite')
def convert(infile: click.File('rt') = sys.stdin, coords: str = None, gain: float = 1.0,
            outfile: click.File('wt') = sys.stdout, outputfmt: Literal['StationXML', 'Datacite'] = 'Datacite'):
    """Convert JSON metadata to StationXML"""
    indict = json.load(infile)
    o = DASMetadata(**indict)

    if outputfmt == 'StationXML':
        # numchans = o.interrogators[0].acquisitions[0].number_of_channels
        # Integrate channels if it was requested
        if coords is not None:
            # Read and create a Channel Group instance
            try:
                # Create a list of channels from a KML file
                chgrp = ChannelGroupModel(cable_id=o.cables[0].cable_id,
                                          fiber_id=o.cables[0].fibers[0].fiber_id,
                                          channels=kml2channels(coords))
                o.interrogators[0].acquisitions[0].channel_groups.append(chgrp)
            except ValidationError as e:
                click.echo('Error while creating a ChannelGroup!')
                click.echo(e.errors())
                sys.exit(-2)
        # Generate a StationXML file as output
        dasrcn2stationxml(o, gain=gain).write(outfile, encoding='unicode')

    elif outputfmt == 'Datacite':
        outfile.write(dasrcn2datacite(o))
    return


@click.command()
@click.option('--experiment', type=str,
              help='Experiment to read and process. It is usually the first part of the filenames.')
@click.option('--directory', type=str, default='.',
              help='Directory where files are located (default: ".")')
@click.option('--start', type=str, default=None,
              help='Start of the selected time window.\nFormat: 2019-02-01T00:01:02.123456Z')
@click.option('--end', type=str, default=None,
              help='End of the selected time window.\nFormat: 2019-02-01T00:01:02.123456Z')
@click.option('--inputfmt', type=click.Choice(dasclasses, case_sensitive=False), default=None,
              help='Format of the data files')
@click.option('--output', type=click.File('wt'), default=sys.stdout,
              help='Filename to save the output')
@click.option('--outputfmt', type=click.Choice(['raw', 'json', 'stationxml'], case_sensitive=True),
              default=None, help='Format of the output')
@click.option('--coords', type=str, default=None,
              help='KML file with coordinates for each channel')
@click.option('--empty', default=False, is_flag=True,
              help='Create an empty instance of metadata in standard format. If this parameter is present, all other parameters will be ignored.')
@click.option('--quick', default=True, is_flag=True,
              help='Check metadata only from the first file')
def create(experiment: str = None, directory: str = '.', start: str = None, end: str = None,
           chstart: int = None, chstop: int = None, chstep: int = 1,
           inputfmt: Literal['OptoDAS', 'TDMS'] = None, output: click.File = sys.stdout, outputfmt: str = 'json',
           coords: str = None, empty: bool = False, quick: bool = True):
    if empty:
        if isinstance(output, str):
            stream = open(output, 'wt')
            json.dump(DASMetadata().model_dump(mode='json'), stream, indent=2)
        else:
            jsonstr = json.dumps(DASMetadata().model_dump(mode='json'), indent=2)
            click.echo(jsonstr)
        # stream.write(json.dumps(DASMetadata().model_dump(mode='json')))
        return

    start = str2date(start)
    end = str2date(end)

    if end is not None and start is not None and start >= end:
        click.echo('End time is smaller than start time.')
        sys.exit(-2)

    # If there are no input format try to guess it from the file extension filtering them with the parameters provided
    if inputfmt is None:
        # Check data format from the dataset (if any)
        try:
            clsdas = checkDASdata(experiment, directory)
        except Exception:
            click.echo('Data format could not be detected!')
            sys.exit(-2)
    else:
        clsdas = str2class(inputfmt)

    if isinstance(chstart, int) and isinstance(chstop, int):
        chlist = list(range(chstart, chstop, chstep))
    else:
        chlist = None
    dasobj = clsdas(experiment, directory=directory, starttime=start, endtime=end,
                    channels=chlist, loglevel='WARNING')
    # progress = tqdm(dasobj)

    if isinstance(output, str):
        stream = open(output, 'wt')
    else:
        stream = output

    # Output format is raw
    if outputfmt == 'raw':
        for data in dasobj:  # progress:
            printmetadata(data, stream)
        return

    o = dasobj.dasrcn
    # Integrate channels if it was requested
    if coords is not None:
        # Read and create a Channel Group instance
        try:
            # Create a list of channels from a KML file
            chgrp = ChannelGroupModel(cable_id=o.cables[0].cable_id,
                                      fiber_id=o.cables[0].fibers[0].fiber_id,
                                      channels=kml2channels(coords))
            # pprint(chgrp.model_dump(mode='json'))
            o.interrogators[0].acquisitions[0].channel_groups.append(chgrp)
        except ValidationError as e:
            click.echo('Error while creating a ChannelGroup')
            pprint(e.errors())
            sys.exit(-2)

    # Output format is stationxml
    if outputfmt == 'stationxml':
        # Generate a StationXML file as output
        dasrcn2stationxml(o).write(stream, encoding='unicode')
        stream.close()
        return

    # Output format is json
    try:
        json.dump(o.model_dump(mode='json'), stream, indent=2)
        # pprint(json.dumps(o.model_dump(mode='json')), stream=stream)
        stream.close()
    except ValidationError as e:
        click.echo('Error while creating main metadata')
        pprint(e.errors())
        sys.exit(-2)


@click.command()
@click.option('--infile', type=click.File('rt'), default=sys.stdout,
              help='Input file in JSON format as proposed by the DAS-RCN group.')
@click.option('--coords', type=str, default=None,
              help='KML file with coordinates for each channel')
@click.option('--outfile', type=click.File('wt'), default=sys.stdout,
              help='File where the modified JSON metadata should be saved')
def addcoords(infile: click.File('rt') = sys.stdin, coords: str = None,
              outfile: click.File('wt') = sys.stdout):
    indict = json.load(infile)
    o = DASMetadata(**indict)
    # numchans = o.interrogators[0].acquisitions[0].number_of_channels
    # Integrate channels if it was requested
    if coords is None:
        click.echo("Error: No coordinates have been provided!")
        sys.exit(-2)
    # Read and create a Channel Group instance
    try:
        # Create a list of channels from a KML file
        chgrp = ChannelGroupModel(cable_id=o.cables[0].cable_id,
                                  fiber_id=o.cables[0].fibers[0].fiber_id,
                                  channels=kml2channels(coords))
        o.interrogators[0].acquisitions[0].channel_groups = [chgrp]
    except ValidationError as e:
        click.echo('Error while creating a ChannelGroup!')
        click.echo(e.errors())
        sys.exit(-2)
    json.dump(o.model_dump(mode='json'), outfile, indent=2)


cli.add_command(create)
cli.add_command(convert)
cli.add_command(addcoords)

# msg = 'Read and convert metadata from different DAS formats to standard representations.'
# parser = argparse.ArgumentParser(description=msg)
# parser.add_argument('-V', '--version', action='version', version='dasmetadata v%s' % __version__)
# parser.add_argument('-l', '--loglevel', help='Verbosity in the output.', default='INFO',
#                     choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'])

if __name__ == '__main__':
    cli()
