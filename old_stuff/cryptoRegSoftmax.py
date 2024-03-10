from rHoodFuncs import * 
from cryptoData import *

login()
cur_data = load_data()

last_hour = []
for i in c.get_crypto_historicals("BTC", span="hour", interval="5minute"):
    last_hour.append(float(i["close_price"]))

print(last_hour)

if(last_hour[0] > last_hour[-1]):
    p = cur_data.extra_cash * 0.95
    if(p > cur_data.total * 0.01):
        cur_data.update_data(buy_price('BTC', p))
else:
    p = cur_data.current_inv * 0.95
    if(p > cur_data.total * 0.01):
        cur_data.update_data(sell_price('BTC', p))

"""db = build_labeled_db(get_all_cryptos_default_db())


features = np.array(db['BTC'][0], dtype=np.float32)
labels  = np.array(db['BTC'][1], dtype=np.float32)
print(features)
print(features.shape)
train_iter = load_array((features, labels), 100)
for X, y in train_iter:
    print(X.shape)
    break
#net = softmax_regression(train_iter, 100)
normalize_data(features, labels)
print(features)
print(labels)
y = []
for feature in features:
    y.append(feature[-1] > feature[0])
y_hat = []
for label in labels:   
    y_hat.append(label > 1)
print(y)
cnt_1 = 0
cnt_0 = 0
total = 0
for i in range(len(y)):
    total += 1
    if(y_hat[i] == 0 and y[i] == 0):
        cnt_0 += 1
    if(y_hat[i] == 1 and y[i] == 1):
        cnt_1 += 1
print(cnt_0/total)
print(cnt_1/total)

cur_p = 1.0
for i in range(len(y)):
    if(y[i]):
        cur_p *= labels[i]
        print(labels[i], " => ", cur_p)
print(cur_p)
#net = regress(2004, features, labels, 10)
#print(features[0].reshape((1,12)).shape)
#print(features[0].shape)
#print(softmax(net(features[0].reshape((1,12)))))
#print(net(features[0:10].reshape((10,12))), end=" | ")
#print(labels[0:10])"""
