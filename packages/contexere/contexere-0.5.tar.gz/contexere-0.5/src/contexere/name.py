import argparse
import logging
from pathlib import Path
import sys

from contexere import __version__
from contexere.discover import summary
from contexere.scheme import abbreviate_date, abbreviate_time, suggest_next

__author__ = "Andreas W. Kempa-Liehr"
__copyright__ = "Andreas W. Kempa-Liehr"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Suggest name for research artefact")
    parser.add_argument(
        "--version",
        action="version",
        version=f"contexere {__version__}",
    )
    parser.add_argument(dest="path",
                        help="Path to folder with research artefacts (default: current working dir)",
                        nargs='?',
                        type=Path,
                        default=Path.cwd())
    parser.add_argument(
        "-n",
        "--next",
        dest="next",
        help="Suggest next artefact name",
        action="store_true"
    )
    parser.add_argument(
        "-p",
        "--project",
        dest="project",
        type=str,
        default=None,
        help="Specify project abbreviation",
        action="store"
    )
    parser.add_argument(
        "-s",
        "--summary",
        dest="summary",
        help="Sumarize files following the naming convention",
        action="store_true"
    )
    parser.add_argument(
        "-t",
        "--time",
        dest="time",
        help="add time abbreviation",
        action="store_true"
    )  
    parser.add_argument(
        "-u",
        "--utc",
        dest="utc",
        help="Generate timestamp with respect to UTC (default is local timezone)",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Start building context...")
    if args.summary:
        summary(args.path)
    elif args.next:
        print(suggest_next(args.path, project=args.project, local=~args.utc))
    else:
        output = abbreviate_date(local=~args.utc)
        if args.time:
            output += abbreviate_time(local=~args.utc)
        print(output)

    # print(args.project + abbreviate_date() + ending)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m contexere.name
    #
    run()
