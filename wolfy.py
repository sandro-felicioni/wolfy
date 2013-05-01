#!/usr/bin/env python
# Copyright 2013 Sandro Felicioni. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'sandro.felicioni@gmail.com'
__version__ = '1.0'

import sys
import alp
import wap
#import wolframBinding.wap as wap

# requires python 2.6+

def getInputArguments():
	inputArguments = ''
	for arg in sys.argv[1:]:
		inputArguments += arg + ' '
	
	# return sample input
	if not inputArguments:
		inputArguments = 'd/dx x^2 + 3'

	return inputArguments


# query wolfram alpha and return the result
def query(inputArguments):
	server = 'http://api.wolframalpha.com/v2/query'
	appid = '2VVQ63-7J3TLY79TQ'

	wolfram = wap.WolframAlphaEngine(appid, server)
	query = wolfram.CreateQuery(inputArguments)
	result = wolfram.PerformQuery(query)
	waeqr = wap.WolframAlphaQueryResult(result)
	#jsonresult = waeqr.JsonResult()
	return waeqr


def handleWolframResult(wolframQueryResult):
	items = []
	if wolframQueryResult.IsSuccess():
		for podData in wolframQueryResult.Pods():
			pod = wap.Pod(podData)
			subpod = wap.Subpod(pod.Subpods()[0]) # for now we just get the first subpod!
			
			item = {} # store all information for one item into a map
			item['title'] = pod.Title()[0] # pod title
			item['subtitle'] = subpod.Img()[0][0][1] # subpod image src
			item['uid'] = 'wolfy' # priorization of items makes not much sense, therefore we use always the same
			item['type'] = 'file'
			item['arg'] = item['title']
			items.append(alp.Item(**item))
	else:
		print "todo error"

	return items


try:
	inputArguments = getInputArguments()
	wolframQueryResult = query(inputArguments)
	items = handleWolframResult(wolframQueryResult)
	alp.feedback(items)
except:
	print '<items><item uid="error"><title>error</title><subtitle>~/error.log</subtitle></item></items>'


#alp.feedback(items)

# give feedback to alfred
#iDict = dict(title="Wolfy", subtitle="This is only a test.", uid="alp-test", valid=False)
#item = alp.Item(**iDict)
#alp.feedback(item)

#print jsonresult
