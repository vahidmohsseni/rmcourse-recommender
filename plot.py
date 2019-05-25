from matplotlib import pyplot as plt


def get_data(addr):
    with open(addr) as f:
        data = f.read().split('\n')
    x = eval(data[0])
    y = eval(data[1])
    return x, y


plt.xlabel('different k value')
plt.ylabel('seconds')
x, y = get_data('./algorithm1/algo1_diff_k.txt')
plt.plot(x, y,label='algorithm1')
x, y = get_data('./algorithm2/algo2_diff_k.txt')
plt.plot(x, y, label='algorithm2')
plt.legend()
plt.show()

