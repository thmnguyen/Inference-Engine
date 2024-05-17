from utils import (
    construct_expression_tree,
    infix_to_postfix,
    postfix_to_infix,
    prefix_to_infix,
)

def biconditional_eliminating(exp_tree):
    if isinstance(exp_tree, str):
        return exp_tree
    elif isinstance(exp_tree, list) and exp_tree[0] == "<=>":
        return ["&", ["=>", biconditional_eliminating(exp_tree[1]), biconditional_eliminating(exp_tree[2])],
                ["=>", biconditional_eliminating(exp_tree[2]), biconditional_eliminating(exp_tree[1])]]
    else:
        return [exp_tree[0]] + [biconditional_eliminating(sub_exp) for sub_exp in exp_tree[1:]]

def implies_eliminating(exp_tree):
    if isinstance(exp_tree, str):
        return exp_tree
    elif isinstance(exp_tree, list) and exp_tree[0] == "=>":
        return ["||", ["~", implies_eliminating(exp_tree[1])], implies_eliminating(exp_tree[2])]
    else:
        return [exp_tree[0]] + [implies_eliminating(sub_exp) for sub_exp in exp_tree[1:]]

def negation_eliminating(exp_tree):
    if isinstance(exp_tree, str):
        return exp_tree
    elif isinstance(exp_tree, list) and exp_tree[0] == "~":
        if isinstance(exp_tree[1], list):
            if exp_tree[1][0] == "&":
                return ["||"] + [negation_eliminating(["~", sub_exp]) for sub_exp in exp_tree[1][1:]]
            elif exp_tree[1][0] == "||":
                return ["&"] + [negation_eliminating(["~", sub_exp]) for sub_exp in exp_tree[1][1:]]
        return ["~", negation_eliminating(exp_tree[1])]
    else:
        return [exp_tree[0]] + [negation_eliminating(sub_exp) for sub_exp in exp_tree[1:]]

def doubleNegEliminating(exp_tree):
    if isinstance(exp_tree, str):
        return exp_tree
    elif isinstance(exp_tree, list) and exp_tree[0] == "~" and isinstance(exp_tree[1], list) and exp_tree[1][0] == "~":
        return doubleNegEliminating(exp_tree[1][1])
    else:
        return [exp_tree[0]] + [doubleNegEliminating(sub_exp) for sub_exp in exp_tree[1:]]

def distribution_perform(exp_tree):
    if isinstance(exp_tree, str):
        return exp_tree
    elif isinstance(exp_tree, list) and exp_tree[0] == "||":
        if isinstance(exp_tree[1], list) and exp_tree[1][0] == "&":
            return ["&"] + [distribution_perform(["||", sub_exp, exp_tree[2]]) for sub_exp in exp_tree[1][1:]]
        elif isinstance(exp_tree[2], list) and exp_tree[2][0] == "&":
            return ["&"] + [distribution_perform(["||", exp_tree[1], sub_exp]) for sub_exp in exp_tree[2][1:]]
    return [exp_tree[0]] + [distribution_perform(sub_exp) for sub_exp in exp_tree[1:]]

def cnf_converter(exp_tree):
    exp_tree = biconditional_eliminating(exp_tree)
    exp_tree = implies_eliminating(exp_tree)
    exp_tree = negation_eliminating(exp_tree)
    exp_tree = doubleNegEliminating(exp_tree)
    exp_tree = distribution_perform(exp_tree)
    return exp_tree

def to_cnf_form(sequence):
    sequence_x = infix_to_postfix(sequence)
    expression = postfix_to_infix(sequence_x).replace("|", "||")
    my_converter = prefix_to_infix(cnf_converter(construct_expression_tree(expression)))
    if my_converter[0] == "(" and my_converter[-1] == ")":
        my_converter = my_converter[1:-1]
    return my_converter

def to_cnf_form_prefix(sequence):
    sequence_x = infix_to_postfix(sequence)
    expression = postfix_to_infix(sequence_x).replace("|", "||")
    my_converter = cnf_converter(construct_expression_tree(expression))
    return my_converter
