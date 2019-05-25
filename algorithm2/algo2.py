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


def argmax(lst, key=None):
    index = 0
    val = lst[0] if key is None else key(lst[0])
    for i, v in enumerate(lst):
        if key is not None:
            v = key(v)
        if v > val:
            index = i
            val = v
    return val, index


def create_bipartite_graph(w):
    graph = dict()
    for wi in w:
        for tag, val in wi.tags.items():
            workers = graph.setdefault(tag, list())
            workers.append((wi, val))
    return graph


def algorithm2(p, w, k):
    result = []
    specialty_graph = create_bipartite_graph(w)
    for pj in p:
        score_table = dict()
        for tl in pj.tags:
            if tl not in specialty_graph:
                continue
            for wi, s in specialty_graph[tl]:
                score_table[wi.id] = score_table.get(wi.id, 0) + s
        w2 = []
        items = list(score_table.items())
        for i in range(k):
            _, best_index = argmax(items, key=lambda x: x[1])
            w2.append(items[best_index][0])
            items.pop(best_index)
            if not items:
                break
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
        result, duration = time_it(algorithm2, p, w, k)
        avg += duration
    avg /= z
    return avg


def increase_k():
    from matplotlib import pyplot as plt
    y = []
    x = []
    for k in range(1, 50):
        print(k)
        avg_duration = 0
        r = 3
        for i in range(r):
            avg_duration += latency(k, 50)
        avg_duration /= r
        x.append(k)
        y.append(avg_duration)
    with open('./algo2_diff_k.txt', 'w') as out:
        out.write(f'{str(x)}\n{str(y)}')
    f = plt.figure()
    plt.plot(x, y)
    plt.show()


def different_p():
    from matplotlib import pyplot as plt
    k = 5
    r = 5
    x = []
    y = []
    for i in range(10, 50):
        print(i)
        avg  = 0
        for j in range(r):
            avg += latency(k, i)
        avg /= r
        x.append(i)
        y.append(avg)
    with open('./algo2_diff_p.txt', 'w') as out:
        out.write(f'{str(x)}\n{str(y)}')
    f = plt.figure()
    plt.xlabel('problem set size')
    plt.ylabel('seconds')
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    increase_k()
