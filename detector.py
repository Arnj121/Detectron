import torch
from torch.autograd import Variable
import numpy as np
import cv2
import time
import warnings
warnings.filterwarnings("ignore")
if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
from ssd import build_ssd
labels = (  # always index 0
    'aeroplane', 'bicycle', 'bird', 'boat',
    'bottle', 'bus', 'car', 'cat', 'chair',
    'cow', 'diningtable', 'dog', 'horse',
    'motorbike', 'person', 'pottedplant',
    'sheep', 'sofa', 'train', 'tvmonitor')
net = build_ssd('test', 300, 21)    # initialize SSD
net.load_weights('./weights/ssd300_mAP_77.43_v2.pth')
def performImgDet(imagepath,filename=None,write=True):
    if filename:
        image=cv2.imread(imagepath)
    else:
        image =imagepath
    start=time.time()
    # rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rgb_image = image
    x = cv2.resize(image, (300, 300)).astype(np.float32)
    x -= (104.0, 117.0, 123.0)
    x = x.astype(np.float32)
    x = x[:, :, ::-1].copy()
    x = torch.from_numpy(x).permute(2, 0, 1)
    xx = Variable(x.unsqueeze(0))     # wrap tensor in Variable
    if torch.cuda.is_available():
        xx = xx.cuda()
    y = net(xx)
    coord = []
    label = []
    scores = []
    detections = y.data
    scale = torch.Tensor(rgb_image.shape[1::-1]).repeat(2)
    # scale each detection back up to the image
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            score = detections[0, i, j, 0]
            scores.append(str(score.item())[:4])
            label_name = labels[i - 1]
            pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
            coords = (pt[0], pt[1]), pt[2] - pt[0] + 1, pt[3] - pt[1] + 1
            coord.append(coords)
            label.append(label_name)
            j += 1
    end = time.time()-start
    for coords in coord:
        rgb_image = cv2.rectangle(rgb_image, (int(coords[0][0]), int(coords[0][1])),
                (int(coords[0][0] + coords[1]), int(coords[0][1] + coords[2])),
                                      color=(36,255,12),thickness=2)
    for i in range(len(label)):
        rgb_image = cv2.putText(rgb_image,"{}/{}".format(label[i],str(scores[i])),
            (int(coord[i][0][0]),int(coord[i][0][1])),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0), 2)
    if write:
        cv2.imwrite('./static/predictionFiles/{}_predicted.jpg'.
                        format(''.join(filename.split('.')[:-1])),rgb_image)
    else:
        return [rgb_image,label]
    return [str(end)[:4],label,scores]

def performVidDet(vidpath,filename):
    c=0
    total=0
    objs=[]
    videocap = cv2.VideoCapture(vidpath)
    try:
        #st=0
        while videocap.isOpened():
            flag,frame = videocap.read()
            if not c:
            #    total+=1
            #    s=time.time()
                frame = performImgDet(frame,False,write=False)
            #    st=st+time.time()-s
            #    cv2.imshow(filename,frame[0])
                objs.extend(frame[1])
            c += 1
            c = c % 30
            if cv2.waitKey(1) == 27:
                break
            #if st>1:
            #    print(total,' total ',st)
            #    st=0
    except cv2.error as e:
        return list(set(objs))

#performVidDet('./static/videos/sample1.mp4','sample1.mp4')

