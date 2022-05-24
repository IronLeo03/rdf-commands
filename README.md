# RDF-COMMANDS
## _Utility to execute commands on rdfind's results_

Small utility to execute commands over rdfind's results.
Although I some tests were performed, it is nowhere near being completely safe and therefore it is highly recommended to perform a dry run before executing any change.
If you find any bug or issue, please fill free to report it on the github issue page.

This is not intended as a replacement for rdfind as, in fact, uses a result file that has already been generated using such tool.
Executing rdfind before this command is needed and for the sake of the examples, I will assume a result file already exists.

## Features

- Select duplicate files or reverse selection
- Select the command to be issued on every file in the selection
- Add the result file to the selection
- Option to avoid accidental command issue
- Option to ask confirmation before each command is executed.


## Requires
- Python3

## Installation

Download the python file and place it in a directory included within your PATH.

## Usage

```sh
<rdfcommands.py> [options] [FILE]
```
View options by using:
```sh
<rdfcommands.py> -h
```

### Examples

Shred all duplicate files found in results.txt
```sh
rdshredder.py -c 'shred -uf {0}' ./results.txt
```

Shred all duplicate files found in results.txt, then also shred the results.txt
```sh
rdshredder.py -ac 'shred -uf {0}' ./results.txt
```

**After making sure the command had not been issued accidently** shred all duplicate files found in results.txt, then also shred the results.txt
```sh
rdshredder.py -sac 'shred -uf {0}' ./results.txt
```

**Simulate** shredding all duplicate files found in results.txt, then also shred the results.txt
```sh
rdshredder.py -nac 'shred -uf {0}' ./results.txt
```

Shred all duplicate files found in results.txt, then also shred the results.txt **but asks for confirmation each time**
```sh
rdshredder.py -yac 'shred -uf {0}' ./results.txt
```
