
def main(*args):
    import psutil
    return psutil.virtual_memory().percent
