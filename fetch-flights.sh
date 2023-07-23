#!/usr/bin/env bash

set -e

limit=2000
year=2023

mkdir -p _out
mkdir -p _tmp
mkdir -p _flights

echo "flights.json: fetching"
wget \
    --no-verbose \
	--load-cookies _tmp/cookies.txt \
    "https://de.dhv-xc.de/api/fli/flights?d0=1.7.$year&d1=31.7.$year&fkto%5B%5D=9306&fkto%5B%5D=11362&clubde%5B%5D=130&navpars=%7B%22start%22%3A0%2C%22limit%22%3A$limit%7D" \
	-O _tmp/flights.json
echo -n "Number of flights fetched: "
jq '.data | length' < _tmp/flights.json
