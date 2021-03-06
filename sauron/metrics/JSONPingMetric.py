#! /usr/bin/env python
# 
# Copyright (c) 2011 SEOmoz
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import urllib2
import datetime
import simplejson as json
from sauron import logger
from sauron.metrics import Metric, MetricException

class JSONPingMetric(Metric):
    def __init__(self, name, **kwargs):
        Metric.__init__(self, name, **kwargs)
        self.reconfig(name, **kwargs)
    
    def reconfig(self, name, url, post=None, timeout=30, **kwargs):
        Metric.reconfig(self, name, **kwargs)
        self.name = name
        self.url  = url
        self.post = post
        self.timeout = timeout
    
    def values(self):
        start = datetime.datetime.now()
        results = {}
        try:
            results = json.loads(urllib2.urlopen(self.url, self.post).read())
            results = dict((k,(v, 'Count')) for k,v in results.items())
        except json.decoder.JSONDecodeError as e:
            raise MetricException('Failed to fetch %s : %s' % (self.url, repr(e)))
        except urllib2.HTTPError as e:
            raise MetricException('Failed to fetch %s : %s' % (self.url, repr(e)))
        except IOError as e:
            raise MetricException('Failed to fetch %s : %s' % (self.url, repr(e)))
        # Some systems are stupid, and don't have total_seconds
        try:
            results['latency'] = ((datetime.datetime.now() - start).total_seconds(), 'Seconds')
        except AttributeError:
            results['latency'] = ((datetime.datetime.now() - start).seconds, 'Seconds')
        return {
            'results': results
        }