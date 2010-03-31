#!/usr/bin/env python
# Copyright (c) 2010, Nick Anderson <nick@cmdln.org>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pexpect
import sys
from getpass import getpass

def process_args():
    from optparse import OptionParser
    usage = "usage: %prog [options] <hostname> [<hostname> <hostname>]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--username", dest="username",
            help="iLOM username (default: %default)")
    parser.add_option("-p", "--password", dest="password", action="store_false",
            help="iLOM password (default: %default)")
    parser.add_option("-f", "--file", dest="commands_file",
            help="file with commands to run (default: stdin/pipe)")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
            help="be verbose in output (default: %default)")


    parser.set_defaults(username = 'root',
                        password = 'changeme',
                        commands_file = False,
                        verbose = False)
    return parser.parse_args()

def get_commands(commands_file):
    commands = []
    if commands_file:
        f = open(commands, "r"):
        commands = f.readlines()
        f.close()
    else:
        while True:
            line = sys.stdin.readline()
            if line:
                commands.append(line)
            else:
                break
    return commands
 
def exec_on_hosts(commands, hosts, options):

    if not options.password:
        options.password = getpass("Password: ")

    for host in hosts:
        try:
            if options.verbose:
                print 'ssh %s@%s' %(options.username,host)
            child = pexpect.spawn('ssh %s@%s' %(options.username,host))
            child.expect('(?i)Password:')
            if options.verbose:
                child.logfile = sys.stdout
            child.sendline(options.password)

            for command in commands:
                child.expect(['-> ', 
                              '\(y/n\)\?',])
                child.sendline(command)

            child.expect('(?i)-> ')
            child.sendline('exit')
            child.close()
        except:
            error='Error: at least one command failed to execute on %s\n' %host
            sys.stderr.write(error)
            child.close()


def main():
    (options, hosts) = process_args()
    commands = get_commands(options.commands_file)
    exec_on_hosts(commands, hosts, options)

if __name__ == '__main__':
    main()
