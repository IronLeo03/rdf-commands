#!/usr/bin/python3

from optparse import OptionParser
import random
import os

def confirm(canSkip = True):
    mini = list('confirm')
    random.shuffle(mini)
    mini = ''.join(mini)
    typed = 'dummy'

    skipText = '\'skip\' to skip or '

    while not (typed == mini or (typed=='skip' and canSkip)):
        try:
            typed = input(f'To confirm type \'{mini}\' ({skipText if canSkip else ""}CTRL-C to stop/cancel): ')
        except KeyboardInterrupt:
            print('\nJob stopped!')
            exit(0)
    return typed == mini

def options():
    usage = 'Usage: %prog [options] [FILE]'
    description = 'Small utility to shred/execute commands on duplicate files. Duplicates MUST Be found beforehand using rdfind. It is REALLY IMPORTANT to either use absolute path-ing or make sure the relative paths are all correct. Although I made this script mainly to shred files, it may be used to perform any command that doesn\'t necessarely aim to securely delete.'
    
    parser = OptionParser(usage=usage, description=description)
    parser.add_option('-n', '--dryrun',
                    action='store_true', dest='dry',
                    help='Does not execute the actual command, it prints in console instead.')
    parser.add_option('-y', '--ask',
                    action='store_true', dest='askconfirm',
                    help='Asks to confirm the operation on every file. By enabling this, one may be able to skip specific files too.')
    parser.add_option('-s', '--sure',
                    action='store_true', dest='sure',
                    help='Asks to confirm before starting the process. Useful in case one is worried to press enter by mistake while typing.')
    parser.add_option('-c', '--cmd',
                    action='store', type='string', dest='cmd', default='cat {0}',
                    help='Command to use to on the files where {0} is the file (default: \'cat {0}\'). Example: \'shred -uf {0}\'')
    parser.add_option('-a', '--add-results',
                    action='store_true', dest='addresult',
                    help='Once all operation is done, also perform the same command the result file likewise duplicate files')
    parser.add_option('-r', '--reverse',
                    action='store_true', dest='reverse',
                    help='Executes operation on DUPTYPE_FIRST_OCCURRENCE instead of DUPTYPE_WITHIN_SAME_TREE.')
    
    return parser

def load_results(filename):
    filerow = list()
    with open(filename, 'r') as file:
        for i in file:
            if i.startswith('#'):
                continue
            duptype, path = i.split(' ')[0], (' '.join(i.split(' ')[7:]).replace('\n',''))
            #Path fix
            path = ''.join((e if (e.isalnum() or e in ['.', '/', '\\']) else '\\'+e) for e in path)
            
            filerow.append((duptype, path))
    return filerow
            
def is_duplicate(text):
    return text == 'DUPTYPE_WITHIN_SAME_TREE'

def perform_operation(path, cmd):
    os.system(cmd.format(path))

def perform_file(path, cmd):
    print(f'About to execute command on file: {path}')
    if confirm():
        perform_operation(path, cmd)
    else:
        print('Skipped.')



if __name__ == '__main__':
    parser = options()
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error('Result file not specified')
    if options.sure:
        print('Sure options specified: Are you sure you want to run the command as it was typed?')
        if not confirm(False):
            parser.error('Aborted.')
    if not options.askconfirm:
        confirm = lambda : True
    if options.dry:
        perform_operation = lambda path, cmd: print(f'COMMAND ISSUED: {cmd.format(path)}')
    if options.reverse:
        is_duplicate = lambda text: text == 'DUPTYPE_FIRST_OCCURRENCE'

    results = load_results(args[0])
    
    for duptype, path in results:
        if is_duplicate(duptype):
            perform_file(path, options.cmd)
    if options.addresult:
        perform_file(args[0], options.cmd)
    
    print('Finished.')