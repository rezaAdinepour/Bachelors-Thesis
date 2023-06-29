import matplotlib.pyplot as plt
import torch
import torch.nn.functional as func
import numpy as np




def sigmoid(x, a, der=False):
    f = 1 / (1 + np.exp(-a*x))
    if (der == True):
        f = f * (1 -f)
    return f

x = torch.linspace(-5, 5, 500)
a = np.linspace(1, 3, 3)
legend = ['a=1', 'a=2', 'a=3']
for i in range(len(a)):
    ssig = sigmoid(x, a[i], der=False)
    plt.figure('Sigmoid')
    plt.title('Sigmoid')
    plt.plot(ssig, label=r'a={}' .format(str(int(a[i]))), linewidth=3)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.3)
    plt.legend()
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.xlabel('$v$')
    plt.ylabel('$\phi(v)$')

plt.savefig('Sigmoid.pdf')
plt.show()





# def unitStep(x):
#     outPut = 1 * (x >= 0)
#     return outPut


# x = torch.linspace(-5, 5, 200)

# yRelu = torch.relu(x)
# yTanh = torch.tanh(x)
# yThresh = unitStep(x)

# i = 1
# titles = ['ReLU', 'Tanh', 'Threshold']
# function = [yRelu, yTanh, yThresh]




# plt.figure(titles[i])
# plt.title('${}$' .format(titles[i]))
# plt.plot(function[i], linewidth=3)
# plt.xlabel('$v$')
# plt.ylabel('$\phi(v)$')
# plt.grid(color = 'gray', linestyle = '--', linewidth = 0.3)
# plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
# plt.savefig(titles[i]+'.pdf')


# plt.savefig(titles[i]+'.pdf')
# plt.show()