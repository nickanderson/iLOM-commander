#!/usr/bin/env python

import pexpect
import sys

def process_args():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username",
            help="iLOM username (default: %default)")
    parser.add_option("-p", "--password", dest="password",
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
        with open(commands_file) as f:
            commands = f.readlines()
        f.closed
    else:
        while True:
            line = sys.stdin.readline()
            if line:
                commands.append(line)
            else:
                break
    return commands
 
def exec_on_hosts(commands, hosts, options):

    for host in hosts:
        try:
            if options.verbose:
                print 'ssh %s@%s' %(options.username,host)
            child = pexpect.spawn('ssh %s@%s' %(options.username,host))
            child.expect('(?i)Password:')
            child.sendline(options.password)

            for command in commands:
                child.expect('(?i)-> ')
                if options.verbose:
                    print command
                child.sendline(command)

            child.expect('(?i)-> ')
            child.sendline('exit')
        except:
            error='Error: at least one command failed to execute on %s\n' %host
            sys.stderr.write(error)


def main():
    (options, hosts) = process_args()
    commands = get_commands(options.commands_file)
    exec_on_hosts(commands, hosts, options)

if __name__ == '__main__':
    main()
