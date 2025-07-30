import kfp.dsl as dsl
from kfp.dsl import OutputPath
import os
from model_train_component import model_train_component
from kfp.dsl import component, pipeline
from typing import Callable



def get_variables(arg: str):
    if arg== "local_directory":
        directory=os.environ.get("local_directory")
        if directory is not None:
            return directory
        else:
            return "."
    if arg== "target_image":
        print(os.environ.get("train_target_image"))
        return os.environ.get("train_target_image")
    if arg == "packages_to_install":
        package_install= os.environ.get("train_packages_to_install")
        if package_install is not None:
            return package_install.split(",")
        else:
            pkg=[]
            return pkg



# @dsl.component(
#     base_image="975050071275.dkr.ecr.us-west-2.amazonaws.com/docker:basepython8",
#     target_image=get_variables("target_image"),
#     packages_to_install=get_variables("packages_to_install")
# )

def model_train_dsl_component(
    model_artifact_path: OutputPath('Model'),
    epochs: int,
    imgsz: int,
    s3_bucket_name: str,
    s3_source_folder: str,
    #callback: Callable
):
#     if callback:
#         callback(model_artifact_path, epochs, imgsz, s3_bucket_name, s3_source_folder)
    print("---------------------inside dsl")
    return component(
            base_image="975050071275.dkr.ecr.us-west-2.amazonaws.com/docker:basepython8",
            target_image=get_variables("target_image"),
            packages_to_install=get_variables("packages_to_install")
        )

# 	from kfp.dsl import component
# from typing import Callable

# def my_dsl_component(base_image: str, target_image: str, packages_to_install: list):
#     def decorator(func: Callable):
#         return component(
#             base_image=base_image,
#             target_image=target_image,
#             packages_to_install=packages_to_install
#         )(func)
#     return decorator