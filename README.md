# ccks2018task2
# CCKS-2018-Task2 in python

The specific details of this task can be viewed at https://biendata.com/competition/CCKS2018_2/.

## 1. Prerequisites

* Python 3.6
* TensorFlow 1.5.0
* keras 2.1.6

## 2. Setup


### 2.1 Reproduce the submitted result
* if you want to use our trained model directly. The predictive label in which the intent is predicted is the best result of the submitted results.
> python mainFunc.py -o data/result/result_mlnlp-ymm.txt


### 2.2 Reproduce results from scratch
* if you want to retrain sequence labeling model by youself.
> python mainFunc.py --pycrf -o data/result/result_mlnlp-ymm.txt

* if you want to retrain classification model by youself.
> python mainFunc.py --classify -o data/result/result_mlnlp-ymm.txt

* if you want to retrain both of the models.
> python mainFunc.py --all -o data/result/result_mlnlp-ymm.txt

* The final result will be stored in "data/result/result_mlnlp-ymm.txt" You can open it as you like.
