import argparse

from .meta import VERSION
from .commands.deploy import deploy
from .commands.init import init
from .commands.diff import diff
from .commands.info import info
from .commands.drift import drift
from .commands.destroy import destroy
from .utils.logging import logger
from .utils.context import Context

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", 
        choices=[
            'diff', 'info', 'deploy', 'package', 
            "version", "init", "destroy", "drift"
        ], 
        help='what action to preform'
    )


    parser.add_argument(
        "-s", "--service",
        default=".*",
        help="specify which stack"
    )

    parser.add_argument(
        "-path", "--path",
        default="services.yml",
        help='path to the file describing the services'
    )

    parser.add_argument('-y', '--yes', action='store_true')


    parser.add_argument(
        "-e", "--env",
        default="",
        help="which enviorment to use"
    )

    parser.add_argument("-v", '--version', action='version', help='path to the file describing the services', version='aws-cf: ' + VERSION)
    parser.add_argument("-r", "--root")
    parser.add_argument("-vb", "--verbose", type=bool)
    # parser.add_argument("-ldf", "--local-diff-cache", type=bool, help="")

    args = parser.parse_args()

    try:
        Context.set_root(args.root or ".")
        Context.set_args(args)
        Context.set_service_path(args.path)
        Context.set_auto_yes(args.yes)

        if args.action == "deploy":
            deploy(args.path, args.root or ".")

        if args.action == "destroy":
            destroy(args.path, args.root or ".")

        if args.action == "info":
            info()

        if args.action == "init":
            init()


        if args.action == "diff":
            diff(args.path, args.root or ".")


        if args.action == "drift":
            drift(args.path, args.root or ".")

    except Exception as e:
        if args.verbose:
            raise e
        logger.error(str(e))
        exit(1)


if __name__ == '__main__':
    main()