#! /usr/bin/env python

import os
import Metric
import logging
import datetime
from boto.s3.connection import S3Connection
from boto.exception import BotoClientError

logger = logging.getLogger('sauron')

class S3BucketMetric(Metric.Metric):
	def __init__(self, name, bucket, keys=None, **kwargs):
		super(S3BucketMetric,self).__init__(name, keys)
		self.bucketName = bucket
		self.prefix = kwargs.get('prefix', '')
		try:
			self.conn = S3Connection(kwargs.get('aws_id', None), kwargs.get('aws_secret', None))
			self.bucket = self.conn.get_bucket(bucket)
		except BotoClientError as e:
			raise Metric.MetricException(repr(e))
		
	def values(self):
		try:
			self.bucket = self.conn.get_bucket(self.bucketName)
			now = datetime.datetime.now()
			youngest = 100
			oldest = 0
			count = 0
			for k in self.bucket.list(self.prefix):
				mod = datetime.datetime.strptime(k.last_modified, '%Y-%m-%dT%H:%M:%S.000Z')
				age = (now - mod).seconds
				if youngest > age:
					youngest = age
				if oldest < age:
					oldest = age
				count += 1
			return {
				'results' : {
					'count' : (count, 'Count'),
					'oldest' : (oldest, 'Seconds'),
					'youngest': (youngest, 'Seconds')
				}
			}
			
			results = []
			len()
		except BotoClientError as e:
			raise Metric.MetricException(repr(e))
		except ValueError as e:
			# Time misparsing can cause this
			raise Metric.MetricException(repr(e))