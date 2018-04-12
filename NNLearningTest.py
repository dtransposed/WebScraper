import ImageRankerNN as ir
from PIL import Image
import glob
import numpy as np
import pickle as p

folder_clean = 'clean_pics'
folder_garbage = 'garbage_pics'

image_ranker = ir.Ranker_NN(1, 1000, 500)

files_clean = glob.glob('clean_pics/*.jpg')
files_garbage = glob.glob('garbage_pics/*.jpg')

img_clean = np.zeros([len(files_clean), 224, 224, 3])
for i in range(len(img_clean)):
    img_clean[i] = Image.open(files_clean[i])

img_garbage = np.zeros([len(files_clean), 224, 224, 3])
for i in range(len(img_clean)):
    img_garbage[i] = Image.open(files_garbage[i])

targets = np.concatenate((np.ones(len(files_clean)), np.zeros(len(files_clean))), axis=0)
data = np.concatenate((img_clean, img_garbage), axis=0)

rnd_index = np.random.permutation(np.arange(len(targets)))
data = data[rnd_index]
targets = targets[rnd_index]

print('Training on ' + str(targets.shape[0]) + ' samples...')

history = []
last_index = 0
N = len(targets)
for i in range(N):
    if (i % 100 == 0 and i != 0) or i == N - 1:
        pred_score = image_ranker.make_prediction(data[last_index:i])
        preds = np.reshape(pred_score > 0.5, (len(targets[last_index:i])))
        acc = np.sum(preds == targets[last_index:i]) / len(targets[last_index:i])
        print('Sample ' + str(last_index) + '-' + str(i-1) + ' | Accuracy: ' + str(acc))
        # print('Sample ' + str(i) +  ': Target: ' + str(targets[i]) + '  Prediction: ' + str(pred))
        history.append([acc, targets[last_index:i], preds, pred_score])
        image_ranker.train_model(data[last_index:i], targets[last_index:i],
                                 batch_size=len(targets[last_index:i]), no_epochs=1)
        last_index = i

p.dump(history,open('history_equalPosNegBatchsizeCa100.p','wb'))