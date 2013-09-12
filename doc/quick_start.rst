Quick Start
-----------

Here's a quick run-down of how to get your systems backed up for point-in-time restore with Lavadisk.

1. Download Lavadisk
2. Install boto with ``user@host:$ pip install boto``
3. Create a configuration file.
4. Run it with ``./lavadisk --config-file $PATH_TO_CONFIG``
5. Schedule backups by creating a cron-job, set it to run at least as often as your most regular backup.

.. note:: The more volumes you want to back-up the longer it will take.

.. warning:: The backup operation is asynchronus.
             Once Lavadisk has finished running,
             all snapshots will have been started, but may not finish for some time.


See :doc:`Configuration </configuration>` for more detail.

