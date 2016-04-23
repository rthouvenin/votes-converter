#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import json
import os.path
import sys

parser = argparse.ArgumentParser(
    description="Converts JSON votes report from parliament to CSV")
parser.add_argument('input_file')
parser.add_argument('output_file', nargs='?')
args = parser.parse_args()

VOTE_NAME = u'issue_type'
VOTE_DECISIONS = [u'Abstain', u'For', u'Against']
VOTES = u'votes'
GROUPS = u'groups'
GROUP_NAME  = u'group'
MEP_ID = u'id'
MEP_NAME = u'orig'

CSV_SEP = u','

if not os.path.exists(args.input_file) or not os.path.isfile(args.input_file):
	sys.exit("Wrong input file: " + args.input_file)

if args.output_file is None:
	input_basename = os.path.basename(args.input_file)
	output_basename, __ = os.path.splitext(input_basename)
	args.output_file = '%s.csv' % output_basename

with open(args.input_file, 'rb') as f:
	json_votes = json.loads(f.read())

meps = {}
vote_names = []
for json_vote in json_votes:
	vote_name = json_vote[VOTE_NAME]
	vote_names.append(vote_name)

	for decision in VOTE_DECISIONS:
		for group in json_vote[decision][GROUPS]:
			group_name = group[GROUP_NAME]
			for vote in group[VOTES]:
				mep_id = vote[MEP_ID]
				mep_name = vote[MEP_NAME]

				if mep_id not in meps:
					meps[mep_id] = {MEP_NAME: mep_name, GROUP_NAME: group_name, VOTES: {}}

				meps[mep_id][VOTES][vote_name] = decision

with open(args.output_file, 'wb') as f:
	f.write(u"mep_id,mep_name,group,")
	f.write(CSV_SEP.join(vote_names).encode('utf-8'))
	f.write(u'\n')

	for mep_id, mep in meps.iteritems():
		mep_votes = mep[VOTES]
		def get_vote(vote_name):
			return mep_votes[vote_name] if vote_name in mep_votes else ''

		f.write(CSV_SEP.join([mep_id, mep[MEP_NAME], mep[GROUP_NAME]]).encode('utf-8'))
		f.write(CSV_SEP)
		f.write(CSV_SEP.join(map(get_vote, vote_names)).encode('utf-8'))
		f.write(u'\n')



