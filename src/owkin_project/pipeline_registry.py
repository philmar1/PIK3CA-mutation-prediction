"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from owkin_project.pipelines import data_processing 
from owkin_project.pipelines import data_engineering
from owkin_project.pipelines import training 

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    
    # Processing pipeline
    data_processing_pipeline, data_processing_pipeline_test = data_processing.concatenate_pipeline()
    umap_embedding_pipeline = data_processing.embedding_pipeline()
    
    pipelines["data_processing_train"] = data_processing_pipeline
    pipelines["data_processing_test"] = data_processing_pipeline_test
    pipelines["data_processing_umap"] = umap_embedding_pipeline
    
    pipelines["data_processing"] = data_processing_pipeline + data_processing_pipeline_test + umap_embedding_pipeline
    
    # Data engineering pipeline
    split_train_eval_pipeline = data_engineering.split_train_eval_pipeline()
    data_engineering_pipeline = data_engineering.prepare_data_pipeline()
    
    pipelines['data_engineering'] = split_train_eval_pipeline + data_engineering_pipeline
    
    # Training pipeline
    training_instance_classifier_pipeline = training.training_instance_classifier_pipeline()
    training_pipeline = training.training_DualStream_pipeline()
    
    pipelines['training_InstanceClassifier_pipeline'] = training_instance_classifier_pipeline
    pipelines['training_DualStreamNet_pipeline'] = training_pipeline
    
    pipelines["__default__"] = pipelines["data_processing"] + pipelines["data_engineering"] + pipelines['training_InstanceClassifier_pipeline'] + pipelines['training_DualStreamNet_pipeline']
    return pipelines
