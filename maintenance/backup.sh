#!/bin/bash

BACKUP_SUFFIX=`date -Iminutes`

docker run -it --rm --name "VLab-Backup-Files" -v "$(pwd):/backup" -v verilog-oj_files-volume:/volume:ro ubuntu:20.04 tar cvf "/backup/backup-files-volume-${BACKUP_SUFFIX}.tar" /volume

docker run -it --rm --name "VLab-Backup-DB" -v "$(pwd):/backup" -v verilog-oj_db-volume:/volume:ro ubuntu:20.04 tar cvf "/backup/backup-db-volume-${BACKUP_SUFFIX}.tar" /volume
