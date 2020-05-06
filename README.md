# ulisp-python
A simple list compiler inspired by Eaton Phil, see the blog post https://notes.eatonphil.com/compiler-basics-lisp-to-assembly.html for details.

Running the program:
```bash
python part1.py '(+ 3 (+ 1 (+ 4 2)))' > program.S
gcc -mstackrealign -masm=intel -o program program.S
./program
echo $?
```

## Useful links
* Memory layout of a C program https://www.cs.bgu.ac.il/~caspl122/wiki.files/lab2/ch07lev1sec6/ch07lev1sec6.html
