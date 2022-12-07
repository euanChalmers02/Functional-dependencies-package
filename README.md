# FDS Package Readme

<aside>
⛔ Currently in progress (please report any bugs or errors)

</aside>

---

This package is free to use for any use and was design to help those learning DBMS and functional dependencies /normal forms. Source code is available on Github [^^^]. Additionally for background to each question/method i have highlight good reading at the end of the question.

### Install

Install the package in the standard pip format.

```python
 pip install FDS
```

### Help

```python
import FDS

FDS.ReadMe()
#or
FDS.Help()
```

### Simple Example:

```python
import FDS 

#MUST BE IN STANDARD FORMAT:

#Attributes = ["A"]  - list of string letters
#Functional dependencies = ["B->C"] - list of functional.. 
#..dependency string with -> as the implied symbol and..  
# ..a comma between each attribute if more than one 

#Find the closure of A
FDS.closureALG(["A"],["B->C","A,B->C","A->B"])
```

### Generate Questions:

```python
import FDS

# 3 is the number of attributes in your question
# 5 is the number of functional dependencies in question
# "C" - String is the seed letter for the question 
	#(e.g. C-> attributes = C,D,E ...)

FDS.generateQuestion(3,5,"C")
```

### Candidate Key Finder:

If there is a complete closure of the LHS of the attribute. 

```python
import FDS

#These are standard formats for attributes & FDs throughout
functional_dependecies = ["B->C","A,B->C"]
attributes = ["A","B","C","D"]

print(FDS.ck(attributes,functional_dependecies))
```

### 3NF:

Attributes:

- Trival FD
- Candidate Key
- Prime Attribute (the RHS of a CK)

If it is a BCNF then it is a 3NF

```python
import FDS

#These are standard formats for attributes & FDs throughout
functional_dependecies = ["B->C","A,B->C"]
attributes = ["A","B","C","D"]

print(FDS.threeNF(attributes,functional_dependecies))
```

### BCNF:

Attributes:

- Trival FD
- Candidate Key

```python
import FDS

#These are standard formats for attributes & FDs throughout
functional_dependecies = ["B->C","A,B->C"]
attributes = ["A","B","C","D"]

print(FDS.BCNF(attributes,functional_dependecies))
```

### Minimal Covers:

Steps:

1. Simplify LHS using the Armstrongs decomposition axiom
2.  Check each item with RHS if > 1 ( X→A if closure(partofRHS) contains A then replace X with partofRHS)
3. Remove redundant FD’s (check if can infer X→A from FD’s - X→A)

```python

import FDS

fds_input = ["C,F->A,D","C,A->B","F,D->D,E","C->A","E->C","D,B->F","E->A"]
attributes = ["A","B","C","D","E","F"]

FDS.minimalFDS(attributes,fds_input)
```

### 3NF systhis algorithm:

### IsCompleteClosure:

### Decomposition and Union to essentail axioms:

### Check Answers:

```python
import FDS

attributes = ["A"]
fds = ["B->C","A,B->C","A->B"]

#What you have calculated as the answer
answer_closure = ["A","B","C"]

FDS.checkClosureAnswer(attributes,fds,answer_closure)

#What you have calculated as the answer
answer_BCNF = False

FDS.checkBCNFAnswer(attributes,fds,answer_BCNF)

#What you have calculated as the answer
answer_CK= []
FDS.checkCK(attributes,fds,answer_CK)
```

### Further Readings:

^^^^^^^^^
