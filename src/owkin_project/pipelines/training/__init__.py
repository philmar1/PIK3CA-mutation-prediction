"""
This is a boilerplate pipeline 'classification_pipeline'
generated using Kedro 0.18.4
"""

from .pipeline import create_pipeline, training_DualStream_pipeline, training_instance_classifier_pipeline

__all__ = ["create_pipeline","training_instance_classifier_pipeline", "training_DualStream_pipeline"]

__version__ = "0.1"
