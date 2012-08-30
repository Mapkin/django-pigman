#!/usr/bin/env python
#
# Created by John Watson on 2012-08-29.
# Copyright (c) 2012 Eightyone Labs, Inc. All rights reserved.
#


from django.conf import settings
from pigman import job, PigMan

instance = PigMan(settings.PIGMAN_SERVERS)
