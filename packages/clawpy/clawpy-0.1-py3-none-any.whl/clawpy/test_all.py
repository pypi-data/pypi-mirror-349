# MIT License  2025 Anish Chaudhuri
# See full license at the bottom of this file.

import time

print("\n**Running All ClawPy Tests** \n")

# List of test files to run
test_files = [
    "Random/basictest.py",
    "Random/scientifictest.py",
    "Random/advancedtest.py",
    "Random/calculustest.py",
    "Random/aitest.py",
    "Random/lefttest.py",
    "Random/othertest.py",
    "Random/appliedtest.py",
    "Random/moretest.py"
]


start_time = time.time()

for test_file in test_files:
    print(f"\n Running: {test_file}...\n")
    try:
        with open(test_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Execute the code in a fresh namespace (dictionary)
        namespace = {}
        exec(code, namespace)
    except Exception as e:
        print(f"Error running {test_file}: {e}")

end_time = time.time()
total_time = end_time - start_time

print(f"\n **All ClawPy Tests Completed in {total_time:.4f} seconds!** \n")

# MIT License
#
# Copyright (c) 2025 Anish Chaudhuri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
