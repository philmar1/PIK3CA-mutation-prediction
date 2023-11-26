"""
This is a boilerplate pipeline 'classification_pipeline'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import *
from .utils.datamanager import *
from .models.DualStream import get_model
from .models.Classifier import get_instance_classifier

    
def training_instance_classifier_pipeline(**kwargs) -> Pipeline:
    return pipeline([ node(
        func=get_InstanceDataset,
        inputs=['X_train_shuffled',
                'y_clustered_train'], 
        outputs='train_instance_dataset',
        name='get_instance_dataset_train',
        tags='training_InstanceClassifier'
    ),
                     
                     node(
        func=get_InstanceDataset,
        inputs=['X_eval',
                'y_clustered_eval'],
        outputs='eval_instance_dataset',
        name='get_instance_dataset_eval',
        tags='training_InstanceClassifier'
    ),
                     
                     node(
        func=get_dataloader,
        inputs=['train_instance_dataset',
                'params:instance_classifier_train.train_batch_size'],
        outputs='train_instance_dataloader',
        name='get_instance_dataloader_train',
        tags='training_InstanceClassifier'
    ),
                     
                     node(
        func=get_dataloader,
        inputs=['eval_instance_dataset',
                'params:instance_classifier_train.eval_batch_size'],
        outputs='eval_instance_dataloader',
        name='get_instance_dataloader_eval',
        tags='training_InstanceClassifier'
    ),
                     node(
        func=get_instance_classifier,
        inputs=['params:instance_classifier.input_dim',
                'params:instance_classifier.cl_hidden_layers_size',
                'params:instance_classifier.dropout',
                'params:instance_classifier.end_activation'],
        outputs='raw_instance_classifier',
        name='get_instance_classifier',
        tags='training_InstanceClassifier'
    ),
                     node(
        func=train,
        inputs=['raw_instance_classifier',
                'train_instance_dataloader',
                'eval_instance_dataloader', 
                'params:train.hyperparameters'],
        outputs='instance_classifier',
        name='train_instance_classifier',
        tags='training_InstanceClassifier'
    )
                     ])

def training_DualStream_pipeline(**kwargs) -> Pipeline:
    return pipeline([ node(
        func=get_MILDataset,
        inputs=['X_train_shuffled',
                'y_train',
                'params:train.n_instances'],
        outputs='train_dataset',
        name='get_dataset_train',
        tags='training_DualStream'
    ),
                     
                     node(
        func=get_MILDataset,
        inputs=['X_eval_scaled',
                'y_eval',
                'params:eval.n_instances'],
        outputs='eval_dataset',
        name='get_dataset_eval',
        tags='training_DualStream'
    ),
                     
                     node(
        func=get_dataloader,
        inputs=['train_dataset',
                'params:train.train_batch_size'],
        outputs='train_dataloader',
        name='get_dataloader_train',
        tags='training_DualStream'
    ),
                     
                     node(
        func=get_dataloader,
        inputs=['eval_dataset',
                'params:train.eval_batch_size'],
        outputs='eval_dataloader',
        name='get_dataloader_eval',
        tags='training_DualStream'
    ),
                     node(
        func=get_model,
        inputs=['params:dual_stream_model.input_dim', 
                'params:dual_stream_model.embed_dim', 
                'params:dual_stream_model.dropout', 
                'params:dual_stream_model.passing_v',
                'params:dual_stream_model.transformers_first',
                'params:dual_stream_model.instance_classifier'],
        outputs='raw_model',
        name='get_model',
        tags='training_DualStream'
    ),
                     node(
        func=train,
        inputs=['raw_model',
                'train_dataloader',
                'eval_dataloader', 
                'params:train.hyperparameters'],
        outputs='model',
        name='train',
        tags='training_DualStream'
    )
    ])
    
def create_pipeline(**kwargs) -> Pipeline:
    basic_pipeline = pipeline([])
    return basic_pipeline