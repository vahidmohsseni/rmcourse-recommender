from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pnd

def get_data(addr):
    with open(addr) as f:
        data = f.read().split('\n')
    x = eval(data[0])
    y = eval(data[1])
    return x, y


sns.set()
plt.xlabel('Problem set size')
plt.ylabel('seconds')
x, y = get_data('./algorithm1/algo1_diff_p.txt')
#data = pnd.DataFrame(data=[x, y],index=['x', 'y']).T
#vis = sns.relplot(x='x', y='y', data=data, kind='line')
plt.plot(x, y,label='algorithm1')
x, y = get_data('./algorithm2/algo2_diff_p.txt')
plt.plot(x, y, label='algorithm2')
plt.legend()
plt.show()

