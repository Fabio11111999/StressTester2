import multiprocessing as mp
from multiprocessing import Pool
from itertools import repeat
from tqdm import *
import time
import subprocess
import random
import os
import argparse

class bcolors:
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

def clear_files(files):
    for file in files:
        os.system('rm -f ' + file)
        
def compile_cpp(cpp, binary, safe=False, print_process=True):
    compilation_process = 1
    sym = bcolors.OKGREEN + u'\u2713' + bcolors.ENDC if safe is True else bcolors.FAIL + 'X' + bcolors.ENDC
    if print_process is True:
        print('\tCompiling '  + cpp + ' ' * (20 - len(cpp)) + 'safe = ' + sym + ':', end=' ', flush = True)
    if safe:
        compilation_process = subprocess.run(
            ['g++', '-std=c++17', '-Wshadow', '-Wall', '-o', binary, cpp, '-g', '-fsanitize=address','-fsanitize=undefined', '-D_GLIBCXX_DEBUG'],
            capture_output=True,
            text=True)
    else:
        compilation_process = subprocess.run(['g++', '-o', binary, cpp],
            capture_output=True,
            text=True)
    if compilation_process.returncode != 0:
        if print_process is True:
            print(bcolors.FAIL + '\tCompilation failed. \n' + bcolors.ENDC)
            print(compilation_process.stderr)
        exit(1)
    if print_process is True:
        print(' ' * (15 - len(cpp)), bcolors.OKGREEN + '\tCompilation completed. \n' + bcolors.ENDC, flush=True)


bars = []
"""
    Return Values:
            0 Generator Execution Failed
            1 Correct Solution Execution Failed
            2 Wrong Solution Execution Failed
            3 Wrong Solution Time Limit Exceeded
            4 Wrong Outpout
            5 All test passed
            6 Another Worker Already finished
"""
def worker(name, test_cases, time_limit, done):
    current_folder = 'files/worker' + str(name) + '/'
    os.system('mkdir -p ' + current_folder)
    os.system('cp -t ' + current_folder + ' gen checker wrong correct')
    for _ in range(test_cases):
        global bars
        bars[name].update(1)
        # If a counter example has already been founded stop here
        if done.is_set():
            return 6
        # Run generator
        seed = random.randint(1, 1000000000)
        gen_execution = subprocess.run([current_folder + 'gen', str(seed)], 
                stdout=open(current_folder + 'input.txt', 'w+'),
                stderr=open('log.txt', 'w+'))
        if gen_execution.returncode != 0:
            done.set()
            return 0
        # Run correct solution
        start_clock = time.time()
        correct_execution = subprocess.run(current_folder + 'correct',
                stdin=open(current_folder + 'input.txt', 'r'),
                stdout=open(current_folder + 'correct_output.txt', 'w+'),
                stderr=open('log.txt', 'w+'),
                text=True)
        time_correct_solution = time.time() - start_clock
        if correct_execution.returncode != 0:
            done.set()
            return 1 
        # Run wrong solution
        start_clock = time.time()
        try:
            wrong_solution = subprocess.run(current_folder + 'wrong',
                    stdin=open(current_folder + 'input.txt', 'r'),
                    stdout=open(current_folder + 'wrong_output.txt', 'w+'),
                    stderr=open('log.txt', 'w+'),
                    text=True,
                    timeout=time_limit)
            time_wrong_solution = time.time() - start_clock
            bars[name].postfix = 'Execution Time:  Correct Solution: ' + str(round(time_correct_solution, 3)) + 's, Wrong Solution: ' + str(round(time_wrong_solution, 3)) + 's'
            if wrong_solution.returncode != 0:
                done.set()
                return 2
        except subprocess.TimeoutExpired:
            done.set()
            os.system('mkdir -p results')
            os.system('cp ' + current_folder + 'input.txt results/')
            os.system('cp ' + current_folder + 'correct_output.txt results/')
            return 3
        # Run checker
        check_execution = subprocess.run([current_folder + 'checker', current_folder + 'correct_output.txt', current_folder + 'wrong_output.txt'])
        if check_execution.returncode != 0:
            if done.is_set():
                return 6
            done.set()
            os.system('mkdir -p results')
            os.system('cp ' + current_folder + 'input.txt results/')
            os.system('cp ' + current_folder + 'correct_output.txt results/')
            os.system('cp ' + current_folder + 'wrong_output.txt results/')
            return 4
    return 5

def execute(test_cases, time_limit):
    print(bcolors.OKGREEN + ' Execution Process: \n' + bcolors.ENDC)
    workers = mp.cpu_count() 
    tcs = [test_cases // workers + (1 if i < test_cases % workers else 0) for i in range(workers)]
    for i in range(workers):
        bars.append(tqdm(total=tcs[i], position=i, desc = ' Worker ' + str(i) + ': ', unit=' testcases', ncols=150, leave=True))
    with Pool(processes=workers) as pool:
        names = range(workers)
        manager = mp.Manager()
        event = manager.Event()
        results = pool.starmap(worker, zip(names, tcs, repeat(time_limit), repeat(event)))
    clear_files(['wrong', 'gen', 'checker', 'correct', '-r files/'])
    bars.clear()
    print('\n')
    print(' Results:')
    if results == [5 for i in range(workers)]:
        print(bcolors.OKGREEN + '\tAll tests passed' + bcolors.ENDC)
    else:
        for i in range(workers):
            if results[i] == 0:
                print(bcolors.FAIL + '\tGenerator Execution Failed \n ERROR:' + bcolors.ENDC)
                os.system('cat log.txt')
                return
            if results[i] == 1:
                print(bcolors.FAIL + '\tCorrect Solution Execution Failed \n ERROR' + bcolors.ENDC)
                os.system('cat log.txt')
                return
            if results[i] == 2:
                print(bcolors.FAIL + '\tWrong Solution Execution Failed \n ERROR' + bcolors.ENDC)
                os.system('cat log.txt')
                return
            if results[i] == 3:
                print(bcolors.FAIL + '\tWrong Solution Time Limit Exceeded' + bcolors.ENDC)
                print('\tCheck results/ to see the input that caused TLE')
                return
            if results[i] == 4:
                print(bcolors.FAIL + '\tA Counter-Example Has Been Found' + bcolors.ENDC)
                print('\tCheck results/ to see input/outputs')
                return

if __name__ == '__main__':
    try:
        clear_files(['-r results/'])
        parser = argparse.ArgumentParser()
        parser.add_argument('--fast', help="does't use sanitiizers to compile the wrong solution", action='store_true')
        parser.add_argument('--testcases', help='number of tested cases')
        parser.add_argument('--tl', help='time limit for the execution of the wrong solution')
        args = parser.parse_args()
        testcases = (int(args.testcases) if args.testcases else 1000)
        timelimit = (float(args.tl) if args.tl else 1)
        os.system('clear')
        print(bcolors.OKGREEN + bcolors.BOLD + ' Debugger Started\n' + bcolors.ENDC)
        print(bcolors.OKBLUE + ' Number of testcases: ' + bcolors.ENDC + str(testcases) + '\t' + bcolors.OKBLUE + 'Time Limit: ' + bcolors.ENDC + str(timelimit) + 's\n') 
        os.system('mkdir -p files')
        print(bcolors.OKGREEN + ' Compilation Process: \n' + bcolors.ENDC)
        compile_cpp('generator.cpp', 'gen', False)
        compile_cpp('checker.cpp', 'checker', False)
        compile_cpp('wrong.cpp', 'wrong', False if args.fast else True)
        compile_cpp('correct.cpp', 'correct', False)
        execute(testcases, timelimit)
        clear_files(['log.txt'])
    except KeyboardInterrupt:
        print(bcolors.FAIL + 'Execution Stopped' + bcolors.ENDC)
        clear_files(['log.txt', '-r results', 'wrong', 'gen', 'checker', 'correct', '-r files/'])
