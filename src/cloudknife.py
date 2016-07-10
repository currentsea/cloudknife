#!/usr/bin/python
__author__ = "currentsea" 
__maintainer__ = "currentsea" 
__version__ = "0.0.1"
__license__ = "MIT" 

# The MIT License (MIT)

# Copyright (c) 2016 currentsea

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import boto3
from clint.textui import puts, indent
from clint import arguments

DEFAULT_REGION = "us-west-2" 

# Check arguments to determine program execution 
def getCreds(args, credentialsFileName="config/aws_credentials"): 
	creds = {}
	if (args == None): 
		with open(credentialsFileName, "r") as credentialsFile: 
			for line in credentialsFile: 
				lineSplit = line.split("=") 
				if len(lineSplit) == 2: 
					if lineSplit[0] == "AWS_ACCESS_KEY" or lineSplit[0] == "AWS_ACCESS_SECRET": 
						key = lineSplit[0] 
						value = lineSplit[1]
						creds[key] = value.strip()
						with indent(4, quote='  ====> '):
							puts(key + ": " + value.strip()) 

	else: 
		try: 
			creds["AWS_ACCESS_KEY"] = raw_input("AWS_ACCESS_KEY: ") 
			creds["AWS_ACCESS_secret"] = raw_input("AWS_ACCESS_KEY: ") 
		except: 
			raise
	return creds
			
def getS3BucketList(region=DEFAULT_REGION): 
	s3 = boto3.client("s3", region_name=region) 
	bucketNameList = []
	for bucket in s3.list_buckets()["Buckets"]: 
		bucketNameList.append(bucket["Name"])
	return bucketNameList

# Return all args passed after "cloudknife.py" - i.e. "$1, $2, $3", etc 
def getUserArgs(): 
	return arguments.Args()

def printS3BucketNames(region=DEFAULT_REGION): 
	print ("BELOW ARE THE AVAILABLE S3 BUCKETS IN THE REGION: " + region)
	bucketNameList = getS3BucketList(region)
	for name in bucketNameList: 
		with indent(4, quote='--> '):
			puts(name)


def processArgs(args): 
	firstArg = args.get(0) 
	if firstArg == None:
		raise IOError("No arguments passed to application.  Please use the \"--help\" flag for help")
	elif firstArg == "get-bucket-names": 
		printS3BucketNames()

if __name__ == "__main__": 
	puts ("Welcome to cloudknife!")
	args = getUserArgs()
	processArgs(args) 
	# bucketList = getS3BucketList()
