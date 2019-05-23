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
        result.append(w2)
    return result


def time_it(func, *args, **kwargs):
    start = time()
    r = func(*args, **kwargs)
    end = time()
    duration = end - start
    return r, duration

def main():
    z = 10
    h = 50
    k = 5
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
    print(avg)


if __name__ == '__main__':
    main()
