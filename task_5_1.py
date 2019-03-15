
import argparse
from copy import deepcopy


def read_grammar(file_name):
    grammar = dict()
    with open(args.file, "r") as file:
        for line in file.readlines():
            rule_id, operands = line.split(':')
            operands = [operand.strip().split()
                        for operand in operands.strip().split("|")]
            grammar[rule_id.strip()] = operands

    return grammar


def output_grammar(file_name, first, follow):
    output_file = open(file_name, 'w+')

    counter = len(first.keys())

    for rule_name in first.keys():
        counter -= 1
        line = rule_name + ' : ' + \
            ' '.join(first[rule_name]) + ' : ' + ' '.join(follow[rule_name])

        if counter != 0:
            line += '\n'
        output_file.write(line)
        print(line)


def get_first_of_grammar(grammar):
    first = dict()
    for rule_id in grammar.keys():
        first[rule_id] = get_first(rule_id, grammar)

    return first


def get_first(terminal, grammar):
    first_array = list()

    for literal in grammar[terminal]:
        for term in literal:
            if term in grammar:
                new_first = get_first(term, grammar)
                found_eps = 'epsilon' in new_first
                if found_eps:
                    new_first.remove('epsilon')
                first_array += new_first
                if not found_eps:
                    break
            else:
                first_array.append(term)
                break

    return list(sorted(set(first_array)))


def is_start_variable(var):
    return var == 'S'


def get_follow_of_grammar(grammar, first):
    follow = dict()

    for rule_id in grammar.keys():
        follow[rule_id] = get_follow(rule_id.strip(), first, grammar)

    return follow


def get_follow(terminal, first, grammar):
    follow_array = list()

    if is_start_variable(terminal):
        follow_array.append('$')

    for rule_id, productions in grammar.items():
        for production in productions:
            if terminal not in production:
                continue

            index_of_terminal = production.index(terminal)

            # If A -> pBq is a production, where p, B and q are any grammar symbols
            # then everything in FIRST(q)  except Є is in FOLLOW(B).
            if index_of_terminal + 1 < len(production):
                if production[index_of_terminal + 1] != terminal:
                    first_of = deepcopy(first[production[index_of_terminal + 1]])
                    found_eps = 'epsilon' in first_of

                    if found_eps:
                        first_of.remove('epsilon')
                        follow_array += get_follow(
                            production[index_of_terminal + 1], first, grammar)
                        if index_of_terminal + 2 == len(production) and rule_id != terminal:
                            new_follow = get_follow(rule_id, first, grammar)
                            follow_array += new_follow

                    follow_array += first_of

            # 3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).
            elif index_of_terminal + 1 == len(production):
                if rule_id != terminal:
                    follow_array += get_follow(rule_id, first, grammar)

    return list(sorted(set(follow_array)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    input_grammar = read_grammar(args.file)

    first = get_first_of_grammar(input_grammar)
    follow = get_follow_of_grammar(input_grammar, first)

    output_grammar('task_5_1_result.txt', first, follow)
