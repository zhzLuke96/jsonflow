
def main(*args):
    import psutil
    return psutil.cpu_percent(interval=1)
