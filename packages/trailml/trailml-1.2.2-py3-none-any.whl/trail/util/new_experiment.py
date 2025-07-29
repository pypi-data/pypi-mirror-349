import mlflow

from trail import Trail


def add_new_experiment():
    with mlflow.start_run():
        with Trail():
            pass
