import logging
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

def calculate_metric(metric_fn, true_y, pred_y):
    logger.info(metric_fn(true_y, pred_y))
    return metric_fn(true_y, pred_y)
    
def print_scores(p, r, f1, a):
    # just an utility printing function
    for name, scores in zip(("precision", "recall", "F1", "accuracy"), (p, r, f1, a)):
        logger.info(f"\t{name.rjust(14, ' ')}: {scores:.4f}")        