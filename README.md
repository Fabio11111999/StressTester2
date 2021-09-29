## StressTester2

StressTester is an handy tool for debugging and finding corner cases in a specific C++ program, the main idea behind it is that the results of a correct code are compared to the ones of the code that needs to be tested with goal of finding a specific test-case that doesn't work on the latter.
### List of files
StressTester is a python script that using multiprocessing allows the user to test his solutions on many testcases in a short period of time. The user must provide the following files:
- `correct.cpp`: a C++ program which is considered to produce only correct outputs, it reads the current input from `stdin` and writes the relative output on `stdout`.
- `wrong.cpp`: the C++ program that needs to be tested, like `correct.cpp` it reads from `stdin` and write on `stdout`.
- `generator.cpp` a C++ program which takes a seed as its only argument and writes on `stdout` a randomly generated testcase.
- `checker.cpp` a C++ program which compares the output produced by `wrong.cpp` and `correct.cpp` and determines whether or not the first one is correct. If the output produced by `wrong.cpp` appears to be correct then `checker.cpp` will return 0. This file will read from file the 2 outputs, the paths of the files will be passed as arguments. 

### Requirements
- Python.
- A Linux Operating System.
- [tqdm](https://github.com/tqdm/tqdm).

### Installation
Just clone the current repository, a premade list of the required files is already in it containing a simple example. 
### How to use it 
The script is really simple to use just run `python3 debugger.py` from terminal, the script will compile all the provided files and it will generate as many workers as the number of core in your CPU. The workers will share the workload splitting the total amount of testcases. Each worker will repeat this process many times:
- Execute the generator getting a new testcase.
- Run the "wrong" and the "correct" solution on that testcase.
- Call the checker to determine whether ot not the output of `wrong.cpp` is good. If it appears to be wrong than terminate the process keeping the current input and the outputs produced.

To determine if the wrong solution will end up in a loop a time limit for its execution is imposed.

### Flags
By default the number of testcases will be equal to `1000` and the time limit for the wrong code is set to `1s`, but it's possibile to change them by adding the flags `--testcases x --tl y` which will set the number of testcases equal to `x` and the time limit for the wrong solution equal to `y` (expressed in seconds).
By default `wrong.cpp` is compiled using different sanitizers which slow down the compilation and execution processes but will provide information about an eventual crash, to disable them and make the testing process faster add the flag `--fast` to the command.

<img width="1053" alt="Cattura" src="https://user-images.githubusercontent.com/39414882/135282228-bc4fbcb8-9f58-43b8-bacc-8a2e211dc0bb.PNG">

