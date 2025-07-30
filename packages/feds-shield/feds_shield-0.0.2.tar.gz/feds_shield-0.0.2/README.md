**DISCLAIMER

Program has a zero-division bug that does not allow division if denominator is 0 at any point in a character's
encoding by the bi-key, thereby causing a crash.

**END_DISCLAIMER

Automaton that can encrypt messages using a structure comprised of layers
centered around a point (centerion).

*explanation*

FEDS shield is a cipher that stands for Friend/Enemy/Difference/Similarity shield.

FEDS shield consists of n arbitary layers and 
each of those layers consists of an arbitrary 
number of integers. Each of those integers is 
called a "cell". The "flattened" version of
the shield (in one dimenion) is an encoding for a
particular character. 

Behind the FEDS shield structure, found in the file `structure.py` with 
accompanying comments, is a structure called a `Centerion` in the file 
`centerion.py` that determines if each of the cells is a `friend` or an 
`enemy`.

FEDS shield can only perform encodings on string messages. Given a string message `m`, each character `a` in `m` will go through a cipher that produces the flattened version of the FEDS shield and a padding consisting of the `Centurion`'s enemies.

Run tests by going into this directory. Then 
`python -m unittest discover tests`

*emphasis*

Not to be thought of as a secure cryptographic
protocol due to two reasons: 

1) *.py implementation.
2) program is a draft;has not demonstrated to 
   work: 
    - no proof-of-concept paper
    - no statistical test results included

*examples*

See the following screenshots for examples: 

![Encryption example](data/encryption_example.png "Encryption example")

![Decryption example](data/decryption_example.png "Decryption example")

*questions?*

For any questions and/or concerns, contact me @ 
phamrichard45@gmail.com

