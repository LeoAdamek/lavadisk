#!/usr/bin/env python

"""
Lavadisk: Keeps your systems running, and your backups HOT!
"""
import re
from logging import Logger , Formatter , StreamHandler , FileHandler , INFO , WARNING
from datetime import datetime, timedelta
from configuration import Configuration

try:
    from boto import ec2
except ImportError:
    raise ImportError("Failed to import 'boto' library, have you run 'pip install -r requirements.txt' ?")

class Lavadisk:

    tag_pattern = re.compile('^backups-(.*)$')
    
    time_interval_pattern = re.compile('^(?P<weeks>[0-9]+)w (?P<days>[0-9]+)d (?P<hours>[0-9]+)h$')

    def __init__(self):
        self.config = Configuration()

        self.logger = Logger( "Lavadisk" )

        stdout_handler = StreamHandler()
        logfile_handler = FileHandler(self.config.config['logfile'])

        if self.config.arguments.verbose:
            self.logger.setLevel(INFO)
            stdout_handler.setLevel(INFO)
            logfile_handler.setLevel(INFO)
        else:
            self.logger.setLevel(WARNING)
            stdout_handler.setLevel(WARNING)
            logfile_handler.setLevel(WARNING)
            

        formatter = Formatter("[%(asctime)s %(levelname)s] %(message)s")
        stdout_handler.setFormatter(formatter)
        logfile_handler.setFormatter(formatter)

        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(logfile_handler)

        self.run_backups()

    def run_backups(self):
        """ Run the backups! """
        if self.config.arguments.region:
            region = self.config.arguments.region
        else:
            region = self.config.config['region']

        self.logger.info("Connecting to AWS Region {}".format(region))

        self.connection = ec2.connect_to_region(
            region,
            aws_access_key_id = self.config.config['aws_key_id'],
            aws_secret_access_key = self.config.config['aws_key_secret']
        )

        self.logger.info("Checking volumes")
        
        ebs_volumes = self.connection.get_all_volumes()

        self.logger.info("Got {} volumes. Checking which ones need backing up".format(len(ebs_volumes)))

        volumes_to_backup = []
        for volume in ebs_volumes:
            if "backups-enabled" in volume.tags.keys():
                check_this_volume = True if volume.tags["backups-enabled"] == 'true' else False
            else:
                check_this_volume = self.config.config['defaults']['enabled']

            if check_this_volume:
                if self._check_backup_age(volume):
                    volumes_to_backup.append(volume)

        self.logger.info("Need to backup {} volumes".format( len(volumes_to_backup) ) )
        self.logger.info("Volume IDS: {}".format( ','.join(volumes_to_backup)) )

        created_snapshots = []
        for volume in volumes_to_backup:
            if "backups-format" in volume.tags.keys():
                snapshot_format = volume.tags["backups-format"]
            else:
                snapshot_format = self.config.config["defaults"]["backups_format"]
            
            if "Name" not in volume.tags.keys():
                volume_name = volume.id
            else:
                volume_name = volume.tags["Name"]

            snapshot_name = datetime.now().strftime(snapshot_format.replace("%V" , volume_name))

            ## DO the backup!
            if not self.config.arguments.dry_run:
                created_snapshots.append( volume.create_snapshot(snapshot_name) )
            else:
                self.logger.info("(DRY RUN) Would've created snapshot: {}".format(snapshot_name))
            

            ## Remove old snapshots
            self._purge_old_snapshots(volume)
        
                            
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
        
        newest_snapshot = datetime.min
        for snapshot in snapshots:
            snapshot_date = self._parse_date(snapshot.start_time)
            # Take the most recent snapshot.
            if snapshot_date > newest_snapshot:
                newest_snapshot = snapshot_date

        if "backups-interval" in volume.tags.keys():
            max_allowed_age = volume.tags["backups-interval"]
        else:
            max_allowed_age = self.config.config["defaults"]["backups_interval"]

        max_timedelta = self._parse_time_interval(max_allowed_age)

        if newest_snapshot < ( datetime.utcnow() - max_timedelta):
            return True

        return False


    def _parse_time_interval(self, time_interval):
        """ 
        Parse a time interval string in a human format:
        Only accepts weeks, days and hours as months and years vary in length.
        e.g. 1w 3d 18h
        """

        match = self.time_interval_pattern.match(time_interval)
        
        if match is None:
            raise ValueError("Invalid time_interval: %s" % time_interval)

        values = dict((elapsed , int(match.group(elapsed) ) ) for elapsed in ['weeks','days','hours'])

        delta = timedelta(days=values['weeks'] * 7 + values['days'] , hours=values['hours'])
        return delta

    def _purge_old_snapshots(self, volume):
        self.logger.info("Checking if any snapshots of {} are stale".format(volume.id))
        snapshots = volume.snapshots()
        
        if "backups-retain" in volume.tags.keys():
            snapshot_retention_period = volume.tags["backups-retain"]
        else:
            snapshot_retention_period = self.config.config["defaults"]["backups_retain"]


        snapshot_retention_period = self._parse_time_interval(snapshot_retention_period)
        
        for snapshot in snapshots:
            snapshot_age = datetime.now() - self._parse_date(snapshot.start_time)
            if snapshot_age > snapshot_retention_period:
                # Delete this old snapshot
                self.logger.info("Deleting Sanpshot: {}".format(shapshot))
                if not self.config.arguments.dry_run:
                    snapshot.delete()
    

    def _parse_date(self, date_string):
        return datetime.strptime(date_string , "%Y-%m-%dT%H:%M:%S.000Z")        

def run():
    lavadisk = Lavadisk()

if __name__ == '__main__':
    run()
