#!/bin/bash

cat report.txt | sed -n "/^$1/,/^2/{p}" | sed '$d'

