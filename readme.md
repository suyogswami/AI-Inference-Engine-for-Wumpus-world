Name: Suyog Siddheshwar Swami
Programming Langauge: Python 2.4
How to run the code: 	Copy all the unzipped folder to omega.
			On the comand line in omega type the following command:
			pyhton check_true_false_suyogs.py a.txt b.txt c.txt and hit enter
			
The file a.txt contain the KB for the wumpus rules.
The file b.txt contain the additional KB containing 48 additonal rules
the file c.txt contain the statement whose entailment against these two KBs needs to be determined

There are two python code files check_true_false_suyogs.py and logical_exp.py respectively.
The logical_exp contain code for reading the expressions and conncectives etc (this file is unchanged from the given sample code)
The check_true_false_suyogs.py contain main function. tt_entail function is included in main function. It also conatin tt_check_all, pl_true (for checking truth of the statments), extend (for adding symbols to the model) and get_symbols(for finding the truth table for symbols)
 
