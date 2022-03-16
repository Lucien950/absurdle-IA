import multiprocessing

def run(a, b):
    return a, b

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    result = pool.starmap(run, [(i, i) for i in range(5)])
    print(result)