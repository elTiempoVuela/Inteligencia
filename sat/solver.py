from commands import getoutput

def solver(problem_class, *args, **kwargs):
    """
    Solves a given `problem` with its given arguments.
    """
    problem = problem_class(*args, **kwargs)
    cnf_file = open('cnf_%s' % problem, 'w')
    cnf_file.write('p cnf %s %s\nc\nc Clauses:\nc\n' % (problem.num_variables,
                                                       problem.num_clauses))
    for clause in problem.clauses:
        cnf_file.write('%s 0\n' % ' '.join([str(s) for s in clause]))
    cnf_file.close()

    output = getoutput('./zchaff/zchaff %s' % cnf_file.name)
    print output
