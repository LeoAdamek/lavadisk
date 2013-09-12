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
import json
from argparse import ArgumentParser

#
# Main Configuration Class
#


class Configuration(dict):
    """Configuration Object"""
    

    def __init__(self, *args, **kwargs):
        self.parse_command_line()
        self.load_config_file()

    def parse_command_line(self):
        parser = ArgumentParser(
            """
            Lavadisk: Keeps your systems running and your backups HOT!
            (Command line arguments will override values in config file.)
            """
        )

        parser.add_argument('--config-file',
                            type=unicode , nargs='?',
                            help="Path to configuration file (default: configuration.json)")


        parser.add_argument('--region',
                            type=unicode , nargs='?',
                            help="AWS Region to use.")

        parser.add_argument('--aws-key-id' ,
                            type=unicode , nargs='?',
                            help="AWS Access Key ID to use")
        
        parser.add_argument('--aws-secret-key',
                            type=unicode , nargs='?',
                            help="AWS Acsss Key Secret to use.")

        parser.add_argument('--dry-run' , dest='dry_run' , action='store_const' ,
                            const=True , default=False ,
                            help=""" Perform a dry run. Don't actually do operations. """)

        
        parser.add_argument('--verbose' , dest='verbose' , action='store_const' ,
                            const=True , default=False ,
                            help=""" Show verbose output to stdout """)


        arguments = parser.parse_args()

        if arguments.verbose:
            print "Running Verbosely."
            print "Using arguments: %s" % arguments
        

        if not arguments.config_file:
            arguments.config_file = 'configuration.json'

        self.arguments = arguments
        return arguments # Return it because why not?

    def load_config_file(self):
        """ Loads the configuration file """
        if not self.arguments.config_file:
            raise ValueError("There is no configuration file to load")

        try:
            config = json.loads(open(self.arguments.config_file).read())
        except ValueError:
            # Maybe this isn't such a good idea.
            raise SyntaxError("The configuration file contains a syntax error.")

        self.config = config

        if self.arguments.verbose:
            print "Got Following Config from %s : \n %s" % (self.arguments.config_file , config)
        
        return config
    



# Test code
if __name__ == '__main__':
    Configuration().parse_command_line()
