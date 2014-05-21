#!/usr/bin/env python
# encoding: utf-8
"""
export_course_data.py

Created by Brady Law on 2011-01-16.
Copyright (c) 2011 Brady Law. All rights reserved.

Modified by Myeong Lee on 2013-06-06.
Since there were big changes in Testudo site, this work had to be revised. 
"""

import sys
import getopt
import json
import csv
import os 

import testudo


help_message = '''
Testudo Course Data Exporter:
Options:
    -h\tHelp
    -q\tQuiet
    -i [file]\tInput json file
    -o [file]\tOutput json file
    -d [dept]\tLimit to specific department
    -t [term]\t
    -l [level]\t
'''

# Specify all department codes that need to be crawled here 

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def count_fields(json_data):    
    attr_count = dict()
    cnt_term = 0
    cnt_code = 0
    cnt_desc = 0
    cnt_title = 0
    cnt_dept = 0
    cnt_level = 0
    cnt_grade = 0
    cnt_credits = 0
    cnt_details = 0
    
    for c in json_data:        
        for attribute, value in c.iteritems():            
            if attribute == 'term' and value :
                cnt_term += 1
            elif attribute == 'code' and value:
                cnt_code += 1
            elif attribute == 'description' and value:
                cnt_desc += 1
            elif attribute == 'title' and value:
                cnt_title += 1
            elif attribute == 'dept' and value:
                cnt_dept += 1
            elif attribute == 'level' and value:
                cnt_level += 1
            elif attribute == 'grade_method' and value:
                cnt_grade += 1
            elif attribute == 'credits' and value:
                cnt_credits += 1
#             elif attribute == 'details' and value:
#                 cnt_details += 1
    attr_count['term'] =cnt_term
    attr_count['code'] =cnt_code
    attr_count['description'] =cnt_desc
    attr_count['title'] =cnt_title
    attr_count['level'] =cnt_level
    attr_count['grade_method'] =cnt_grade
    attr_count['credits'] =cnt_credits
#     attr_count['details'] =cnt_details
    return attr_count

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hoid:q", ["help","output=","input_json_data=","dept=","term=","level="])
        except getopt.error, msg:
            raise Usage(msg)

        verbose= True
        output = os.path.dirname(os.path.realpath(__file__)) + '/../data/course_data.json'
        json_data = None
        dept = None
        level = None
        term = None

        # option processing
        for option, value in opts:
            if option == "-q":
                verbose = False
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-i", "--input_json_data"):
                json_data = value
            if option in ("-o", "--output"):
                output = value
            if option in ("-d", "--dept"):
                dept = value
            if option in ("-t", "--term"):
                term = value
            if option in ("-l", "--level"):
                level = value
                
        c = testudo.crawler(term=term, verbose=verbose)
        
        if json_data:
            # Load exising JSON data (faster)
            courses = json.load(open(json_data, 'rb'))
        else:
            # Fetch course data from server
            if dept:                
#                 courses = c.get_courses(dept=dept, level=level)      
                courses = []
                courses.extend(c.get_courses(dept=dept, level='UGRAD'))
                courses.extend(c.get_courses(dept=dept, level='GRAD'))          
            else:
                courses = []
                for d in dept_list:
                    courses.extend(c.get_courses(dept=d, level='UGRAD'))
                    courses.extend(c.get_courses(dept=d, level='GRAD'))                                       
            
            # Error checking, with counting the number of each field
            for attribute, value in count_fields(courses).iteritems():                
                if value<2:                                      
                    print "Field " + attribute + " has a small number of fields, " + str(value) + ". Report this problem directly to Administrators."
                    return 0
            
        json.dump(courses, open(output, 'wb'), indent=2)
        print "1"
        return "[Python] Crawling Successful.\n"
            
                        

#===============================================================================
#         if csv:
#             course_writer = csv.writer(open('data/courses.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             section_writer = csv.writer(open('data/sections.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             class_time_writer = csv.writer(open('data/class_times.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
# 
#             for c in courses:
#                 if c['sections']:
#                     for s in c['sections']:
#                         if s['class_times']:
#                             for ct in s['class_times']:
#                                 class_time_writer.writerow([c['code'], s['section']] + ct.values())
#                         del s['class_times']
#                         section_writer.writerow([c['code']] + s.values())
#                 del c['sections']
#                 course_writer.writerow(c.values())
#===============================================================================

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
