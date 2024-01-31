import torch
from torch.autograd import Function
from ..box_utils import decode, nms
# from data import voc as cfg
from config import voc as cfg

class Detect(Function):
    """At test time, Detect is the final layer of SSD.  Decode location preds,
    apply non-maximum suppression to location predictions based on conf
    scores and threshold to a top_k number of output predictions for both
    confidence score and locations.
    """
    num_classes=0
    top_k=0
    background_label=0
    nms_thresh=0
    conf_thresh=0
    variance=0
    def __init__(self, num_class, bkg_label, top_k, conf_thresh, nms_thresh, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Detect.num_classes = num_class
        Detect.background_label = bkg_label
        Detect.top_k = top_k
        # Parameters used in nms.
        Detect.nms_thresh = nms_thresh
        if nms_thresh <= 0:
            raise ValueError('nms_threshold must be non negative.')
        Detect.conf_thresh = conf_thresh
        Detect.variance = cfg['variance']

    @staticmethod
    def forward(_,loc_data, conf_data, prior_data):
        """
        Args:
            loc_data: (tensor) Loc preds from loc layers
                Shape: [batch,num_priors*4]
            conf_data: (tensor) Shape: Conf preds from conf layers
                Shape: [batch*num_priors,num_classes]
            prior_data: (tensor) Prior boxes and variances from priorbox layers
                Shape: [1,num_priors,4]
        """
        num = loc_data.size(0)  # batch size
        num_priors = prior_data.size(0)
        output = torch.zeros(num, Detect.num_classes, Detect.top_k, 5)
        conf_preds = conf_data.view(num, num_priors,
                                    Detect.num_classes).transpose(2, 1)

        # Decode predictions into bboxes.
        for i in range(num):
            decoded_boxes = decode(loc_data[i], prior_data, Detect.variance)
            # For each class, perform nms
            conf_scores = conf_preds[i].clone()

            for cl in range(1, Detect.num_classes):
                c_mask = conf_scores[cl].gt(Detect.conf_thresh)
                scores = conf_scores[cl][c_mask]
                if scores.size(0) == 0:
                    continue
                l_mask = c_mask.unsqueeze(1).expand_as(decoded_boxes)
                boxes = decoded_boxes[l_mask].view(-1, 4)
                # idx of highest scoring and non-overlapping boxes per class
                ids, count = nms(boxes, scores, Detect.nms_thresh, Detect.top_k)
                output[i, cl, :count] = \
                    torch.cat((scores[ids[:count]].unsqueeze(1),
                               boxes[ids[:count]]), 1)
        flt = output.contiguous().view(num, -1, 5)
        _, idx = flt[:, :, 0].sort(1, descending=True)
        _, rank = idx.sort(1)
        flt[(rank < Detect.top_k).unsqueeze(-1).expand_as(flt)].fill_(0)
        return output
