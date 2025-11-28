import argparse


class CliHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Data Extractor CLI"
        )
        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-g",
            action="store_true",
            help="Extract data from Git"
        )
        group.add_argument(
            "-j",
            action="store_true",
            help="Extract data from Jira"
        )

    def parse(self, args=None):
        self.args = self.parser.parse_args(args)
        return self.args
