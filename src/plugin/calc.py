

def main(query, expression):
    """
    expression => a + b
    query => {a:1,b:2}
    return 3
    """
    return eval(expression, query)
