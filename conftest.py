import os
import sys


#Get the absolute path of the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')) #getting absolute path of project root directory

print("PROJECT ROOT: ",project_root)

sys.path.insert(0, project_root) # It adds os path to sys.path, so Python can locate your main program files.

# 1.what is config test file: it is special file in pytest used to share setup and configuration
#across multiple test files.it helps avoid code repetition by defining common fixtures
#or configuration
#2.conftest.py file ensures that our test script can access the main program, even when it's in a different directory.
#3.Since our test file is in another directory, Python might not automatically find your main program. The sys.path.insert(0, project_root) line ensures that the Python interpreter can find and import your main code.
#4.Without modifying sys.path, pytest might not find our main program files.
#5. Instead of manually adding paths in each test file, conftest.py does it once for all tests.