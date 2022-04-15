# ADB
Team : Ishta Gangal (ig1043) and Divya Juneja (dj1322)

This project was written in Python (Python 3.6) 

To execute source code without reprounzip navigate to source code that contains the code and run:

python StartRepCRec.py --filePath inputs/test1.txt 

If you want to put the contents to an output file you may use the following command and the console output will be written to file name specified in the args insteads:

python StartRepCRec.py --filePath inputs/test1.txt --outFile <filename>


Command line arguments: 
TO DO:

Transaction Manager:
if isCylic returns true added a check to see if transactions in cycleTransactions == 1. IF yes then it might be a self loop that shouldn't be killed. So it then tries to find a loop between transactions as stored in the blocked Queue, if there also there is a loop then it is killed otherwise not. IF len(cycleTransactions) > 1 then finds youngest transaction in the cycleTransactions and kills that (same as before)

1. kill the youngest transaction -> mark aborted -Done, needs to be tested

2. Execute the commands in wait for graph - in progress

3. Add in queue the commands which are executed after the site fails -> in case of odd variable execute all sequentially, if even then don't add read or write 

4. When no site is available then add both write and read transactions

5. decide whether to return and not allow current to running state
-> If current transaction is already in waiting queue to read then do multiple reads
line 192 in transaction manager

6. upgrade request - test case 21 - deadlock

7. display that it cant get read lock cause it is waiting for another transaction that has a write lock

8. check if waiting because of site unavailibility and add else statements and wait for graph

9. Add commands to queue if site fails and execute later in case of odd variables; ignore the even variable read and write requests

10. add read command after write is done on a variable

checkTransactionExists - not needed so far

map for which transaction waiting for which one - done

abort() - Done

check abort label before running any transaction -Done

dump on site - Done

reprozip - Done

flag all the replicated variables if a site is down and don't allow read until something is written to it - Done by using foundVariables list

Test Cases Tested:
Working: 1, 2, 3, 3.5, 3.7, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20(checked by adding end(T5) and then end(T1) to test, 21, 11

Not working: 11 -> detecting self loop as a cycle. Add condition to check if loop detected has only one transaction in graph.cycleTransactions, if yes then it should return false for cycle. -- FIXED. i think.

18,19 ->Even variable write lock not getting acquired. check why. they are present in the wait queue though, so maybe add a check for this. -- FIXED
