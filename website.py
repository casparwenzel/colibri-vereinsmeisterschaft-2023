#!/usr/bin/env python3

# Generates the website

import json
import os
import jinja2
import math
import shutil
import datetime
import re
import numpy as np
import pandas as pd
import folium

import constants

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())


def task1(flight, lpradius=constants.lpradius, task_points=20):
    xc = round(float(flight["BestTaskPoints"]), 2)
    if xc <= task_points:
        deduction = 0
        xcvalid = round(xc, 2)
    else:
        deduction = round(xc - task_points, 2)
        xcvalid = round(task_points - deduction, 2)
    # if flight["stats"]["landepunktabstand"] <= lpradius:
    if flight["LandingLocation"] == "Horben, Breisgau-Hochschwarzwald, Baden-W\u00fcrttemberg":
        landing = 20
    else:
        landing = 0
    total = round(xcvalid + landing, 2)

    return {
        "name": flight["FirstName"] + " " + flight["LastName"],
        "xc": xc,
        "deduction": deduction,
        "xcvalid": xcvalid,
        "landing": landing,
        "total": total,
    }


def task2(flight, lpradius=constants.lpradius, task_points=75):
    xc = round(float(flight["BestTaskPoints"]), 2)
    if xc <= task_points:
        deduction = 0
        xcvalid = round(xc, 2)
    else:
        deduction = round(xc - task_points, 2)
        xcvalid = round(task_points - deduction, 2)
    # if flight["stats"]["landepunktabstand"] <= lpradius:
    if flight["LandingLocation"] == "Horben, Breisgau-Hochschwarzwald, Baden-W\u00fcrttemberg":
        landing = 20
    else:
        landing = 0
    total = round(xcvalid + landing, 2)

    return {
        "name": flight["FirstName"] + " " + flight["LastName"],
        "xc": xc,
        "deduction": deduction,
        "xcvalid": xcvalid,
        "landing": landing,
        "total": total,
    }


# prepare output directory

os.makedirs("_out", exist_ok=True)
shutil.copytree("templates/static", "_out/static", dirs_exist_ok=True)

flight_data = json.load(open("_tmp/flights.json"))

flights = {}

task1_results = {}
task2_results = {}


# Group flights by pilot, read stats
for flight in flight_data["data"]:
    id = flight["IDFlight"]
    pid = flight["FKPilot"]

    # flight["stats"] = json.load(open(f"_stats/{id}.stats.json"))

    if pid not in flights:
        flights[pid] = []
    flights[pid].append(flight)

    # Calculate task1 and task2 results for each flight
    task1_result = task1(flight)
    task2_result = task2(flight)

    # Store task1 and task2 results in dictionaries for each pilot
    if pid not in task1_results:
        task1_results[pid] = []
    if pid not in task2_results:
        task2_results[pid] = []

    task1_results[pid].append(task1_result)
    task2_results[pid].append(task2_result)


highest_task1 = {}
highest_task2 = {}

for pid, task1_list in task1_results.items():
    max_task1 = max(task1_list, key=lambda x: x["total"])

    highest_task1[pid] = max_task1

for pid, task2_list in task2_results.items():
    max_task2 = max(task2_list, key=lambda x: x["total"])

    highest_task2[pid] = max_task2

# Sort by total points
task1_sorted = dict(sorted(highest_task1.items(), key=lambda item: item[1]["total"], reverse=True))
task2_sorted = dict(sorted(highest_task2.items(), key=lambda item: item[1]["total"], reverse=True))


points_task1 = []

for i, flight in enumerate(task1_sorted.values()):
    flight["rank"] = i + 1
    points_task1.append(flight)

points_task2 = []

for i, flight in enumerate(task2_sorted.values()):
    flight["rank"] = i + 1
    points_task2.append(flight)


# Write main website
data = {}
data["points"] = {"task1": points_task1[:10], "task2": points_task2[:10]}
env.get_template("index.html").stream(data).dump(open(f"_out/index.html", "w"))
env.get_template("base.html").stream(data).dump(open(f"_out/base.html", "w"))
