from d2l import mxnet as d2l
from mxnet import autograd, gluon, np, npx
from mxnet.gluon import nn
from mxnet import init
from IPython import display
npx.set_np()

def load_array(data_arrays, batch_size, is_train=True):
    dataset = gluon.data.ArrayDataset(*data_arrays)
    return gluon.data.DataLoader(dataset, batch_size, shuffle=is_train)


def regress(batch_size, features, labels, num_epochs):

    data_iter = load_array((features, labels), batch_size)

    net = nn.HybridSequential()
    net.add(nn.Dense(8, activation='relu'), nn.Dense(1))
    net.initialize(init.Normal(sigma=1))

    loss = gluon.loss.L2Loss()
    #loss = gluon.loss.SoftmaxCrossEntropyLoss()
    trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': .9})

    for epoch in range(num_epochs):
        for X, y in data_iter:
            with autograd.record():
                l = loss(net(X), y)
            l.backward()
            #print(net[1].weight.data())
            #print(net[1].weight.grad())
            w0 = net[0].weight.data()
            w1 = net[1].weight.data()
            b0 = net[0].bias.data()
            b1 = net[1].bias.data()
            trainer.step(batch_size)        
            print("w0 diff", net[0].weight.data() - w0)
            print("w1 diff", net[1].weight.data() - w1)
            print("b0 diff", net[0].bias.data() - b0)
            print("b1 diff", net[1].bias.data() - b1)
        l = loss(net(features), labels)
        print(f'epoch {epoch + 1}, loss {l.mean().asnumpy():f}')
    print("b0", net[0].bias.data())
    print("b1", net[1].bias.data())
    return(net)

def softmax(X):
    X_exp = np.exp(X)
    partition = X_exp.sum(1, keepdims=True)
    return X_exp / partition

class Accumulator:
    def __init__(self, n):
        self.data = [0.0] * n

    def add(self, *args):
        self.data = [a + float(b) for a, b in zip(self.data, args)]

    def reset(self):
        self.data = [0.0] * len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

def train_epoch(net, train_iter, loss, updater):
    metric =  Accumulator(3)
    #if isinstance(updater, gluon.Trainer):
    #    updater = updater.step
    for X, y in train_iter:
        with autograd.record():
            y_hat = net(X)
            l = loss(y_hat, y)
        l.backward()
        updater.step(X.shape[0])
        metric.add(float(l.sum()), accuracy(y_hat, y), y.size)
    print(f' loss {l.mean().asnumpy():f}')
    return metric[0] / metric[2], metric[1] / metric[2] 

def train(net, train_iter, loss, num_epochs, updater):
    for epoch in range(num_epochs):
        print(epoch + 1, ": ", end="")
        train_metrics = train_epoch(net, train_iter, loss, updater)
        #test_acc = evaluate_accuracy(net, test_iter)
    train_loss, train_acc = train_metrics
    return(net)

def evaluate_accuracy(net, data_iter):
    metric = Accumulator(2)
    for X, y in data_iter:
        metric.add(accuracy(net(X),y), y.size)
    return metric[0] / metric[1]

def accuracy(y_hat, y):
    if len(y_hat.shape)> 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp = y_hat.astype(y.dtype) == y
    return float(cmp.astype(y.dtype).sum())

def normalize_data(features, labels):
    one = features[:, 0]
    print("-=-=-=-=-=-one.shape, features.shape-=-=-=-=-=-")
    print(one.shape, features.shape,end='\n\n')
    for i in range(features.shape[0]):
        features[i] = features[i] / one[i]
        labels[i]   = labels[i]   / one[i]

def linReg(train_iter, batch_size, num_epochs):
    net = nn.Sequential()
    net.add(nn.Dense(1))
    net.initialize(init.Normal(sigma=0.01))

    loss = gluon.loss.L2Loss()
    trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': 0.03})
    train(net, train_iter, loss, num_epochs, trainer)
    return net

def get_synthetic_data():
    true_w = np.array([2, -3.4])
    true_b = 4.2
    features, labels = d2l.synthetic_data(true_w, true_b, 2000)

    train_iter = load_array((features[:1000], labels[:1000]), batch_size)
    test_iter  = load_array((features[1000:], labels[1000:]), batch_size)
    return(train_iter, test_iter)

def softmax_regression(train_iter, num_epochs):
    net = nn.Sequential()
    net.add(nn.Dense(32, activation='relu'), nn.Dense(2))
    net.initialize(init.Normal(sigma=1))
    #print(softmax(net(next(iter(train_iter))[0][0])))

    loss = gluon.loss.SoftmaxCrossEntropyLoss()

    trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': 0.1})
    train(net, train_iter, loss, num_epochs, trainer)
    return net

def get_fashion_data(batch_size):
    return d2l.load_data_fashion_mnist(batch_size)
    







