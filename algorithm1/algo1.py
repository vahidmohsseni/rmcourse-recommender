import sqlite3
from time import time


db_address = '../database/db'
db = sqlite3.connect(db_address)


class Problem:
    def __init__(self, data):
        self.id = int(data[0])
        self.stack_id = data[1]
        self.ans_id = data[2]
        self.tags = set(filter(lambda x: x != '', data[4].split(',')))
    
    def __repr__(self):
        return f'problem <{self.id}>'
    
    def __in__(self, tag):
        return tag in self.tags


def str_val(s):
    if 'k' in s:
        s = s.replace('k', '000')
    return int(s)


class Worker:
    def __init__(self, data):
        self.id = int(data[0])
        self.stack_id = data[1]
        tmp_tags = data[2].split(',')
        tmp_tags = filter(lambda x: x != '', tmp_tags)
        tmp_tags = map(lambda x: x.split(':'), tmp_tags)
        self.tags = {x[0]: str_val(x[1]) for x in tmp_tags} # tag with score
    
    def __repr__(self):
        return f'worker <{self.id}>'


def get_problems(start_id, end_id):
    query = f'SELECT * FROM questions WHERE id >= {start_id} AND id <= {end_id}'
    problems = db.execute(query).fetchall()
    problems = list(map(Problem, problems))
    return problems


def get_all_workers():
    query = 'SELECT * FROM worker'
    workers = db.execute(query).fetchall()
    workers = list(map(Worker, workers))
    return workers


def dist(wi, pj):
    pj_tags = len(pj.tags)
    worker_tags = set(wi.tags.keys())
    inter = worker_tags & pj.tags
    count = len(inter)
    d = 1 - count / pj_tags
    return d


def argmin(lst, key=None):
    index = 0
    val = lst[0] if key is None else key(lst[0])
    for i, v in enumerate(lst):
        if key is not None:
            v = key(v)
        if v < val:
            index = i
            val = v
    return val, index


def algorithm1(p, w, k):
    result = []
    for pj in p:
        d = []
        for wi in w:
            d.append((wi, dist(wi, pj)))
        w2 = []
        for i in range(k):
            _, best_index = argmin(d, key=lambda x: x[1])
            w2.append(d[best_index][0])
            d.pop(best_index)
        result.append(w2)
    return result


def time_it(func, *args, **kwargs):
    start = time()
    r = func(*args, **kwargs)
    end = time()
    duration = end - start
    return r, duration

def latency(k, h):
    z = 10
    w = get_all_workers()
    # size_w = len(w)
    avg = 0
    for i in range(z):
        start = z * i
        end = start + h
        p = get_problems(start, end)
        # size_p = len(p)
        result, duration = time_it(algorithm1, p, w, k)
        avg += duration
    avg /= z
    return avg


def increase_k():
    from matplotlib import pyplot as plt
    y = []
    x = []
    for k in range(1, 50):
        print(k)
        avg_duration = latency(k, 50)
        x.append(k)
        y.append(avg_duration)
    f = plt.figure()
    plt.plot(x, y)
    plt.show()


def different_p():
    from matplotlib import pyplot as plt
    k = 5
    r = 5
    x = []
    y = []
    for i in range(10, 60):
        print(i)
        avg  = 0
        for j in range(r):
            avg += latency(k, i)
        avg /= r
        x.append(i)
        y.append(avg)
    f = plt.figure()
    plt.xlabel('problem set size')
    plt.ylabel('seconds')
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    different_p()

