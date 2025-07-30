import click
import json
import argparse
import json
from pandas import DataFrame
import sys
import argparse
from whosclient.whosclient import OmOgcTimeseriesClient

def parse_first_arg():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "command",
        nargs="?",
        choices=["data", "metadata"],
        default="data",
        help="Command to run. Default is 'data'."
    )
    args, remaining_args = parser.parse_known_args()
    return args.command, remaining_args

@click.group()
def cli():
    pass

@cli.command()
@click.option('-t','--token', default=None, type=str, help='WHOS access token')
@click.option('-u','--url', default=None, type=str, help='WHOS OM OGC timeseries API url')
@click.option('-o','--output', default=None, type=str, help='Save result into this file (instead of print on stdout)')
@click.option('-c','--csv', is_flag=True, default=False, help='Use CSV format for output (instead of JSON)')
@click.option("-m","--monitoring_point",default=None,type=str,help="site identifier. It must be user together with --variable_name")
@click.option("-v","--variable_name",default=None,type=str,help="variable identifier. It must be used together with --monitoring_point")
@click.option("-s","--timeseries_identifier",default=None,type=str,help="timeseries identifier. If set, --monitoring_point and --variable_name are ignored")
@click.argument("begin_position")
@click.argument("end_position")
def data(token, url, output, csv, monitoring_point, variable_name, timeseries_identifier, begin_position, end_position):
    config = {}
    if token is not None:
        config["token"] = token
    if url is not None:
        config["token"] = token
    client = OmOgcTimeseriesClient(config)
    data = client.getData(
        begin_position, 
        end_position,
        feature = monitoring_point, 
        observedProperty = variable_name, 
        observationIdentifier = timeseries_identifier
    )
    if output is not None:
        if csv:
            df = DataFrame(data)
            df.to_csv(open(output, "w"), index=False)
        else:
            json.dump(data, open(output, "w"), ensure_ascii=False)
    else:
        if csv:
            df = DataFrame(data)
            df.to_csv(sys.stdout, index=False)
        else:
            click.echo(json.dumps(data))

@cli.command()
@click.option('-t','--token', default=None, type=str, help='WHOS access token')
@click.option('-u','--url', default=None, type=str, help='WHOS OM OGC timeseries API url')
@click.option('-o','--output', default=None, type=str, help='Save result into this file (instead of print on stdout)')
@click.option("-m","--monitoring_point",default=None,type=str,help="site (feature) identifier. It must be user together with --variable_name")
@click.option("-v","--variable_name",default=None,type=str,help="variable identifier (=observedProperty). It must be used together with --monitoring_point")
@click.option("-s","--timeseries_identifier",default=None,type=str,help="timeseries identifier. If set, --monitoring_point and --variable_name are ignored")
@click.option("-l","--limit",default=None,type=int,help="pagination page size")
@click.option('-h','--has_data', is_flag=True, default=False, help='return only observations with data')
@click.option("-W","--west",default=None,type=float,help="west longitude of bounding box")
@click.option("-S","--south",default=None,type=float,help="south latitude of bounding box")
@click.option("-E","--east",default=None,type=float,help="east longitude of bounding box")
@click.option("-N","--north",default=None,type=float,help="north latitude of bounding box")
@click.option("-O","--ontology",default=None,type=str,help="The ontology to be used to expand the observed property search term (or URI) with additional terms from the ontology that are synonyms and associated to narrower concepts. Two ontologies are available: whos or his-central")
@click.option("-V","--view",default=None,type=str,help="Identifier of the data subset interesting for the user")
@click.option("-T","--time_interpolation",default=None,type=str,help="The interpolation used on the time axis (for example, MAX, MIN, TOTAL, AVERAGE, MAX_PREC, MAX_SUCC, CONTINUOUS, ...)")
@click.option("-i","--intended_observation_spacing",default=None,type=str,help="The expected duration between individual observations, expressed as ISO8601 duration (e.g., P1D)")
@click.option("-a","--aggregation_duration",default=None,type=str,help="Time aggregation that has occurred to the value in the timeseries, expressed as ISO8601 duration (e.g., P1D)")
@click.option("-f","--format",default=None,type=str,help="Response format (e.g. JSON or CSV)")
def metadata(token, url, output, monitoring_point, variable_name, timeseries_identifier, limit, has_data, west, south, east, north, ontology, view, time_interpolation, intended_observation_spacing, aggregation_duration, format):
    config = {}
    if token is not None:
        config["token"] = token
    if url is not None:
        config["token"] = token
    client = OmOgcTimeseriesClient(config)
    data = client.getTimeseriesWithPagination(
        feature = monitoring_point, 
        observedProperty = variable_name, 
        observationIdentifier = timeseries_identifier,
        limit = limit,
        view = view,
        has_data = has_data, 
        west = west, 
        south = south, 
        east = east, 
        north = north, 
        ontology = ontology, 
        timeInterpolation = time_interpolation, 
        intendedObservationSpacing = intended_observation_spacing, 
        aggregationDuration = aggregation_duration, 
        format = format
    )
    if output is not None:
        json.dump(data, open(output, "w"), ensure_ascii=False)
    else:
        click.echo(json.dumps(data, ensure_ascii=False))

if __name__ == '__main__':
    command, remaining = parse_first_arg()
    sys.argv = [sys.argv[0], command] + remaining  # Reset sys.argv for click
    cli()
