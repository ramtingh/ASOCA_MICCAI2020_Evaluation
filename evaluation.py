import SimpleITK
import nrrd
import numpy as np
import os
from scipy.spatial import cKDTree
from evalutils import ClassificationEvaluation
from evalutils.io import ImageLoader
from evalutils.validators import (
    NumberOfCasesValidator, UniquePathIndicesValidator, UniqueImagesValidator
)
def hausdorff_95(submission,groundtruth):
    # There are more efficient algorithms for hausdorff distance than brute force, however, brute force is sufficient for datasets of this size.
    submission_points = np.array(np.where(submission), dtype=np.uint16).T
    submission_kdtree = cKDTree(submission_points)
    
    groundtruth_points = np.array(np.where(groundtruth), dtype=np.uint16).T
    groundtruth_kdtree = cKDTree(groundtruth_points)
    
    distances1,_ = submission_kdtree.query(groundtruth_points)
    distances2,_ = groundtruth_kdtree.query(submission_points)
    return max(np.quantile(distances1,0.95), np.quantile(distances2,0.95))

class Loader(ImageLoader):
    @staticmethod
    def load_image(fname):
        filename, ext = os.path.splitext(fname)
        if ext=='.nrrd':
            submission, header = nrrd.read(fname)
        elif ext=='.npz':
            submission = np.load(fname)
            keys = list(submission.keys())
            if len(keys)!= 1:
                raise ValueError(f"Compressed numpy array in submission {fname} must contain exactly one array")
            submission = submission[keys[0]]
        else:
            raise ValueError(f" Unknown file extension  {ext}")
        return submission
    @staticmethod
    def hash_image(image):
        return hash(str(image))

def dice_score(a,b):
    return 2*np.sum(a*b)/(np.sum(a)+np.sum(b))


class Asoca(ClassificationEvaluation):
    def __init__(self):
        super().__init__(
            file_loader = Loader(),
            validators=(
                NumberOfCasesValidator(num_cases=20),
            ),
        )
    @property
    def _metrics(self):
        return {
            "aggregates": self._aggregate_results,
        }
    def score_case(self, *, idx, case):
        gt_path = case["path_ground_truth"]
        pred_path = case["path_prediction"]
        submission = Loader.load_image(pred_path)
        truth, truth_header = nrrd.read(gt_path)
        submission = submission>0.5
        if np.count_nonzero(submission)==0:
            raise ValueError(f" Submission {pred_path.name} is empty")
        
        if submission.shape != truth.shape:
            raise ValueError(f" Expected image with dimensions {truth.shape}, got {submission.shape} in {pred_path.name}")
        truth = truth>0.5
        dice=dice_score(submission, truth)
        hausdorff = hausdorff_95(submission=submission, groundtruth=truth)


        return {
            'DiceCoefficient': dice,
            'HD95':hausdorff,
            'pred_fname': pred_path.name,
            'gt_fname': gt_path.name,
        }


if __name__ == "__main__":
    Asoca().evaluate()
