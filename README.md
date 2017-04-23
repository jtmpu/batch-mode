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
