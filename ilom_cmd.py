#!/usr/bin/env python

import pexpect
import sys


commands = [ 'set SP/alertmgmt/rules/1/ type=snmptrap',
             'set SP/alertmgmt/rules/1/ level=minor',
             'set SP/alertmgmt/rules/1/ destination=10.77.203.137',
             'set SP/alertmgmt/rules/1/ snmp_version=1',
             'set SP/alertmgmt/rules/1/ testrule=true',
           ]

sys.argv.reverse()
sys.argv.pop()
hosts = sys.argv

for host in hosts:
    print 'running commands on', host 
    child = pexpect.spawn('ssh %s' %sys.argv[1])
    child.expect('(?i)Password:')
    child.sendline('changeme')

    for command in commands:
        child.expect('(?i)-> ')
        child.sendline(command)
    child.expect('(?i)-> ')
    child.sendline('exit')

