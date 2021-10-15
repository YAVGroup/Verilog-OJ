#!/bin/bash

BACKUP_SUFFIX="$1"

if [ -f "backup-files-volume-${BACKUP_SUFFIX}.tar" && -f "backup-db-volume-${BACKUP_SUFFIX}.tar" ]; then
    docker run -it --rm --name "VLab-Restore-Files" -v "$(pwd):/backup" -v verilog-oj_files-volume:/volume ubuntu:20.04 tar xvf "/backup/backup-files-volume-${BACKUP_SUFFIX}.tar" /volume

    docker run -it --rm --name "VLab-Restore-DB" -v "$(pwd):/backup" -v verilog-oj_db-volume:/volume ubuntu:20.04 tar xvf "/backup/backup-db-volume-${BACKUP_SUFFIX}.tar" /volume
else
    echo "Suffix ${BACKUP_SUFFIX} not present"
    exit 1
fi