"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([])


def split_train_eval_pipeline(**kwargs) -> Pipeline:

    return pipeline([node(
        func=get_train_eval_IDs,
        inputs=['train_metadata'],
        outputs= ['eval_IDs', 'train_IDs'],
        name='split_train_eval_emb',
        tags='data_engineering'
    ),
                    node(
        func=split_train_eval,
        inputs=['concatenated_datasets', 'concatenated_indexs', 'eval_IDs', 'train_IDs'],
        outputs= ['X_train', 'X_eval'],
        name='split_train_eval_X',
        tags='data_engineering'
    ),
                    node(
        func=split_train_eval,
        inputs=['concatenated_targets', 'concatenated_indexs', 'eval_IDs', 'train_IDs'],
        outputs= ['y_train', 'y_eval'],
        name='split_train_eval_y',
        tags='data_engineering'
    ),
                    node(
        func=split_train_eval,
        inputs=['concatenated_indexs', 'concatenated_indexs', 'eval_IDs', 'train_IDs'],
        outputs= ['indexs_train', 'indexs_eval'],
        name='split_train_eval_indexs',
        tags='data_engineering'
    ),
                    node(
        func=split_train_eval,
        inputs=['y_clustered', 'concatenated_indexs', 'eval_IDs', 'train_IDs'],
        outputs= ['y_clustered_train', 'y_clustered_eval'],
        name='split_train_eval_yclustered',
        tags='data_engineering_InstantClassifier'
    )
                    ])
    
def prepare_data_pipeline(**kwargs) -> Pipeline:
    return pipeline([node(
        func=fit_scaler,
        inputs=['X_train', 'indexs_train'],
        outputs='scaler',
        name='fit_scaler',
        tags='data_engineering'
    ),
                     node(
        func=scale,
        inputs=['X_train', 'indexs_train', 'scaler'],
        outputs='X_train_scaled',
        name='scale_train',
        tags='data_engineering'
    ),
                     node(
        func=scale,
        inputs=['X_eval', 'indexs_eval', 'scaler'],
        outputs='X_eval_scaled',
        name='scale_eval',
        tags='data_engineering'
    ),
                     node(
        func=shuffleX,
        inputs='X_train_scaled',
        outputs='X_train_shuffled',
        name='shuffleX',
        tags='data_engineering'
    )
    ])
