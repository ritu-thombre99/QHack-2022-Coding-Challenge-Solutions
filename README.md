# QHack Coding Challenge

The [QHack Coding Challenge](https://challenge.qhack.ai) is a set of 25 quantum coding challenges. [Challenge Repository link](https://github.com/XanaduAI/QHack/tree/master/Coding_Challenges) 



## Setting Up Environment<a name="setup" />


```console
pip install -r requirements.txt
```  

## Running Solutions<a name="testing" />

Run the `#.py` by supplying one of the `#.in` files for that problem to the solution script via `stdin`. 

For example, to run the file `my_solution.py` and for the first set of inputs, do the following:
 * Open a terminal console (`CMD`, `Terminal`, etc.) and navigate to the folder containing the solution
 * Run the file and pass in the inputs:  
`python ./my_solution.py < 1.in`
 * Output to the console should match answer in `1.ans` file (within some tolerance specified in the `problem.pdf` file)

To run on Windows Powershell: `Get-Content 1.in | python .code.py`

