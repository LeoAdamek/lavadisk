"""
Configuration:

Handles all the configuration related stuff for Lavadisk.
Including command-line arguments.
Configuration File(s) and stuff...
"""

# Imports (all standard library)
import sys
import re
import os
from argparse import ArgumentParser

#
# Main Configuration Class
#


class Configuration(dict):
    """Configuration Object"""
    

    def __init__(self, *args, **kwargs):
        pass

    def parse_command_line(self):
        parser = ArgumentParser(
            """
            Lavadisk: Keeps your systems running and your backups HOT!
            (Command line arguments will override values in config file.)
            """
        )

        parser.add_argument('--config-file',
                            type=unicode , nargs='?',
                            help="Path to configuration file")


        parser.add_argument('--region',
                            type=unicode , nargs='?',
                            help="AWS Region to use.")

        parser.add_argument('--aws-key-id' ,
                            type=unicode , nargs='?',
                            help="AWS Access Key ID to use")
        
        parser.add_argument('--aws-secret-key',
                            type=unicode , nargs='?',
                            help="AWS Acsss Key Secret to use.")


        arguments = parser.parse_args()

        if not arguments.config_file:
            arguments.config_file = 'configuration.json'

        self.arguments = arguments
        return arguments # Return it because why not?

    def parse_config_file(self):
        pass


# Test code
if __name__ == '__main__':
    Configuration().parse_command_line()
