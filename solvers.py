from pysat.formula import CNF
from pysat.solvers import Solver

# parse attributes file
def parse_attr(text):
    lines = text.strip().split('\n')
    parsed = {}
    for (i, line) in enumerate(lines, start=1):
        category, items_str = line.split(':')
        items = items_str.split(',')
        parsed[category.strip()] = {items[0].strip(): i, items[1].strip(): -i} # the name of the attribute value and its numeric representation
    return parsed

def parse_constraints_into_cnf(text, attrs: dict) -> CNF:
    lines = text.strip().split('\n')
    
    cnf = CNF()
    for (lineNum, line) in enumerate(lines):
        cnf_constraint = []
        clauses: list[str] = line.strip().split('AND') # A list of disjunctive clauses, e.g. A OR B AND C OR D would produce ['A OR B', 'C OR D']
        for clause in clauses:
            cnf_clause = []
            literals: list[str] = clause.strip().split('OR') # A list of literals in a clause, e.g. ['A', 'NOT B']
            for literal in literals:
                
                literal_name = literal.strip().removeprefix('NOT').strip()
                literal_numeric = None
                for attribute in attrs.values():
                    if literal_name.strip() in attribute:
                        literal_numeric = attribute[literal_name]
                if (literal_numeric is None): 
                    print("Error parsing '" + literal + "' on line " + str(lineNum) )
                    return []
                if (literal_numeric is not None and literal.strip().startswith('NOT')):
                    literal_numeric = -literal_numeric

                cnf_clause.append(literal_numeric)

            cnf_constraint.append(cnf_clause)

        cnf.extend(cnf_constraint)
    return cnf


def generate_possible_objects(constr: CNF, attrs: dict):
        possible_objects = []
        with Solver(bootstrap_with=constr) as solver:
             for m in solver.enum_models():
                possible_objects.append([get_attr_name_from_numeric(x, attrs) for x in m])

# Get the name of an attribute value from its numeric representation, e.g. -1 gets turned into 'ice-cream'
def get_attr_name_from_numeric(numeric: int, attrs: dict):
    for attribute in attrs.values():
        for key in attribute:
            if (attribute[key] == numeric): 
                return key
    
    return None
