### WPBrute

Multi-threaded Wordpress password login brute forcer.

I read somewhere in passing that during a CTF, someone had written a multi-threaded python script for checking Wordpress login/passwords.. well, it just kinda stuck in my head. I was very interested in see how fast it would be, how many threads would be too much for the webserver/wordpress/wordfence.

Wordpress/mysql is running from a docker container.

```
docker-compose up -d
```

Should get it up and running on port 8000


### First test:
Took seven hours for the script to complete with a 1 million passwords, but since I didnt have global checks, I'm not sure when the password was found.
*d'oh*

```
0 :  49999
1 :  49999
2 :  49999
3 :  49999
4 :  49999
5 :  49999
6 :  49999
7 :  49999
8 :  49999
9 :  49999
10 :  49999
11 :  49999
12 :  49999
13 :  49999
14 :  49999
15 :  49999
16 :  49999
17 :  49999
18 :  49999
19 :  49999
20 :  19
[!] Starting Workers...
Worker #0 started.
Worker #1 started.
Worker #2 started.
 Worker #3 started.Worker #4 started.
 Worker #5 started.

Worker #6 started.
Worker #7 started.
Worker #8 started.
 Worker #9 started.
Worker #10 started.
Worker #11 started.
Worker #12 started.
Worker #13 started.
Worker #14 started.
Worker #15 started.
Worker #16 started.
Worker #17 started.
Worker #18 started.
Worker #19 started.
Worker #20 started.
Worker #20 finished.
MATCH FOUND: Password1234
Worker #6 finished.
Worker #3 finished.
Worker #4 finished.
Worker #0 finished.
 Worker #8 finished.
Worker #9 finished.
Worker #15 finished.
Worker #17 finished.
Worker #14 finished.
Worker #16 finished.
Worker #12 finished.
Worker #10 finished.
Worker #11 finished.
Worker #5 finished.
Worker #7 finished.
Worker #18 finished.
Worker #13 finished.
Worker #19 finished.
Worker #1 finished.
./wpbrute.py  4549.26s user 615.37s system 19% cpu 7:13:13.85 total
```


### Second Test:
Adding some cmd line arguments with argparse. Much better time here with a global var being checked on password found.
Next tests will be for login attempt throughtling by wordfence.
```
$ astonge@doom time ./wpbrute.py -f passwords.txt -t 30
Using password file passwords.txt
Setting up 30 workers
Using average size of 33333 lines/worker
Starting Workers...
Worker #30 finished.
Worker 4 found a password: Password1234
./wpbrute.py -f passwords.txt -t 30  384.12s user 52.04s system 18% cpu 39:02.64 total
```
