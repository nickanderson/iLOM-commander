iLOM Commander

iLOM Commander is a simple python script to assist in pushing a configuration to
multiple servers.


Usage: ilom_cmd.py [options] <hostname> [<hostname> <hostname>]

Options:
  -h, --help            show this help message and exit
  -u USERNAME, --username=USERNAME
                        iLOM username (default: root)
  -p PASSWORD, --password=PASSWORD
                        iLOM password (default: changeme)
  -f COMMANDS_FILE, --file=COMMANDS_FILE
                        file with commands to run (default: stdin/pipe)
  -v, --verbose         be verbose in output (default: False)


Example Usage:


echo "set SP/alertmgmt/rules/1/ type=snmptrap" | ilom_cmd.py server-lom.lan


commands.txt:
    set SP/alertmgmt/rules/1/ type=snmptrap
    set SP/alertmgmt/rules/1/ level=minor

cat commands.txt | ilom_cmd.py server-lom.lan server1-lom.lan
ilom_cmd.py -f commands.txt server-lom.lan server1-lom.lan
ilom_cmd.py server-lom.lan server1-lom.lan < commands.txt


Known Limitations:
Interactive password promt is not supported. If you want to create a new user
be sure to set the password as you create the user.
    create /SP/users/me role=Administrator cli_mode=alom password=mypass

