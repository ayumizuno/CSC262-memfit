Ayumi Mizuno <br>
CSC262 <br>
P2 memfit <br>


This program was written in Python. The code is inside the memfit-py folder. To run: <br>
python memfit-py/main.py input.txt


Sample input (input2.txt):
```
pool next 1000
alloc A 200
alloc B 400
alloc C 100
free B
alloc D 100
alloc E 200
free E
alloc F 300
```
The result of running this input should be:
```
Free_list
         offset: 500     size: 100
         offset: 800     size: 200

Used List
         offset: 0       size: 200       name: A
         offset: 200     size: 300       name: F
         offset: 600     size: 100       name: C
         offset: 700     size: 100       name: D
```
