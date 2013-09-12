"""
Lavadisk: Keeps your systems running, and your backups HOT!
"""
import re
from datetime import datetime, timedelta
from configuration import Configuration

try:
    from boto import ec2
except ImportError:
    raise ImportError("Failed to import 'boto' library, have you run 'pip install -r requirements.txt' ?")

class Lavadisk:

    tag_pattern = r'^backups-(.*)$'

    def __init__(self):
        self.config = Configuration()
        
        self.run_backups()

    def run_backups(self):
        """ Run the backups! """

        self.connection = ec2.connect_to_region(
            self.config.config['region'],
            aws_access_key_id = self.config.config['aws_key_id'],
            aws_secret_access_key = self.config.config['aws_key_secret']
        )
        
        ebs_volumes = self.connection.get_all_volumes()

        volumes_to_backup = []
        for volume in ebs_volumes:
            for tag in volume.tags:
                ## Check that the current tag is of use to use
                if re.match(self.tag_pattern , tag):

                    # Check if this volume even has backups
                    if tag == 'backups-enable':
                       if volume.tags[tag] == 'false':
                           break
                       if volume.tags[tag] == 'true':
                           check_this_volume = True
                    
            
            check_this_volume = (self.config.config['defaults']['enabled'])

            if check_this_volume:
                self._check_backup_age(volume)


        
                            
    def _check_backup_age(self, volume):
        """
         Check the age of the most recent snapshot for `volume`
         

         Returns:

         True:: volume requires snapshotting.
         False:: volume does not require snapshotting.
        """
        snapshots = volume.snapshots()

        if not snapshots:
            return True
        
        newest_snapshot = 0
        for snapshot in snapshots:
            snapshot_date = datetime.strptime(snapshot.start_time , "%Y-%m-%dT%H:%M:%S.%z")
            if "backups-interval" in volume.tags.keys():
                max_allowed_age = volume.tags["backups-interval"]
            else:
                max_allowed_age = self.config.config["defaults"]["backups_interval"]

            self._parse_time_interval(max_allowed_age)

    def _parse_time_interval(self, time_interval):
        """ 
        Parse a time interval string in a human format:
        e.g. 1y 2m 1w 3d 18h
        """
        
        # Regex for the interval
        pattern = r"((\d+){y,m,w,d,h})+"

        if not pattern.match(time_interval):
            raise ValueError("Got a bad time interval: %s" % time_interval)
        
        
                    
            

                        


        


def run():
    lavadisk = Lavadisk()

if __name__ == '__main__':
    run()
