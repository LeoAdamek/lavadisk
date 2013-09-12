Configuration
=============

Lavadisk can be configured with a JSON file, with some options being overriden via the command line.
The default backup options are specified via the configuration file, but can be overriden on a per-volume basis using tags.


Command Line Flags
------------------

* `--help` , `-h` Show the help.

* `--region` Specify a region to connect to. Overrides config file.

Unimplimented Flags
^^^^^^^^^^^^^^^^^^

The following options will appear but do not currently function.

* `--aws-key-id` Specify the AWS access key.
* `--aws-key-secret` AWS Secret.


Configuration File
------------------

The configuration file is written in json and expects the following:

* `region` : AWS Region to connect to.
* `aws_key_id` : AWS Access key
* `aws_key_secret` : Aws Key Secret phrase

A `defaults` object should be present and accepts the following.

* `enabled` : A `true` / `false` for enabling backups by default
* `backups_interval` : (See: Time Interval) Regularity of backups
* `backups_format` : A standard `date` format, with the addition of `%V` for Volume Name
* `backups_retain` : (See: Time Interval) Retention period for backups

Volume Tags
-----------

AWS allows the tagging of resources with metadata.
The following tags will be used to override their config file counterparts:

* `backups-enabled`
* `backups-interval`
* `backups-format`
* `backups-retain`

The tag keys have the same function as in the configuration file.
