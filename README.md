# Batch-Mode
Run programs in batch mode. This enables program to be aborted and resumed on the fly, as well as 
running them in multiple processes to speed up exectution.

Batch-mode keeps track of previously run sessions, with their configuration. This enables the output
to be saved and expanded over time as more jobs are added to a session.

In order for batch-mode to run programs they must conform with the following interface:
* The programs perform jobs
* Jobs are given to the program via STDIN
* One job is located on one line
* The reporting mechanism of the program reports to STDOUT
* Any flags or configuration details for the program are given as flags to the program itself.

## Examples

Below shows an example of starting a new session.


```
$ ./batch-mode.py new -c "path-brute -p 127.0.0.1:8000 -v" -r /fuzzdb/discovery/predictable-filepaths/filename-dirname-bruteforce/raft-small-files.txt -v -b 500 -f
[-] Session with that name already exists.
[-] Deleting old session and forcing a new session.
[+] 23/23 batches remaining.
[+] Batch '13.batch' complete.
[+] Batch '20.batch' complete.
[+] Batch '21.batch' complete.
^C[+] Batch '6.batch' complete.
[+] Quitting.
```

Below shows an example of show sessions and resuming.

```
$ ./batch-mode.py run
Existing sessions: 
ls.2017-04-23
path-brute.2017-04-23
$ ./batch-mode.py run -s path-brute.2017-04-23 -v
[+] 15/23 batches remaining.
[+] Batch '18.batch' complete.
[+] Batch '10.batch' complete.
[+] Batch '1.batch' complete.
[+] Batch '9.batch' complete.
[+] Batch '17.batch' complete.
^C[+] Batch '11.batch' complete.
[+] Quitting.
```

Belows examples using the session subcommand.

```
$ ./batch-mode.py session
Existing sessions: 
ls.2017-04-23
path-brute.2017-04-23
$ ./batch-mode.py session -s path-brute.2017-04-23 -o
[-] Miss: http://127.0.0.1:8000/2257.txt
[-] Miss: http://127.0.0.1:8000/227.html
[-] Miss: http://127.0.0.1:8000/229.html
[-] Miss: http://127.0.0.1:8000/23.htm
[-] Miss: http://127.0.0.1:8000/234.html
[-] Miss: http://127.0.0.1:8000/235.html
[-] Miss: http://127.0.0.1:8000/237.html
[-] Miss: http://127.0.0.1:8000/238.html
[-] Miss: http://127.0.0.1:8000/24.htm
[-] Miss: http://127.0.0.1:8000/241.html
[-] Miss: http://127.0.0.1:8000/242.html
[-] Miss: http://127.0.0.1:8000/244.html
[-] Miss: http://127.0.0.1:8000/251.html
[-] Miss: http://127.0.0.1:8000/28-3.html
[-] Miss: http://127.0.0.1:8000/295.html
[-] Miss: http://127.0.0.1:8000/306.html
[-] Miss: http://127.0.0.1:8000/310.html
[-] Miss: http://127.0.0.1:8000/318.html
[-] Miss: http://127.0.0.1:8000/343.html
```
