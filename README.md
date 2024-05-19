# Apartment And Chair Delivery Limited - Chair Counting Tool

This Python command line tool is designed to automate the process of counting different types of chairs from apartment floor plans for Apartment And Chair Delivery Limited.

## Background

Given the rise in business over the past years, the demand for automation of organizational tasks has increased. One of these tasks is the counting of different types of chairs indicated by home buyers in floor plans of their apartments.

Previously, this process was done manually, leading to various mistakes and dissatisfaction among customers. This tool enables users to avoid such mistakes by automating the counting process.

The tool reads an old format floor plan file and outputs the following crucial information:

- Number of different chair types for the apartment
- Number of different chair types per room

The different types of chairs are denoted as follows in the floor plan:

- `W`: Wooden Chair
- `P`: Plastic Chair
- `S`: Sofa Chair
- `C`: China Chair

## Setup

1. Ensure that Python 3.12.3 or a later version is installed on your system.
2. Clone this repository in your local system using following command:

`git clone git@github.com:iNinad/chair_counting_tool.git`

3. Navigate to the repository using command line terminal or shell and install the dependencies using following command:

`pip install -r requirements.txt
`

## Usage

In the console, navigate to the directory containing the script and execute the following command:

`python furniture_plan_analyzer.py -f /path/to/your/floor_plan_file.txt
`

Replace the /path/to/your/floor_plan_file.txt with the actual path to the floor plan file you want to analyze.
After running this command, the script will read the given floor plan file, analyze it, and output the count of different chair types for the entire apartment and for each room in a nicely formatted way.

## Note

This application assumes that the floor plan file format is consistent and adheres to the formatting rules. If the floor plan file format varies, the script may not work as expected.