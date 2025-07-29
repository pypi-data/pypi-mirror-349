# import kfp.dsl as dsl
# from kfp.dsl import OutputPath
# import os
# from typing import Callable, Optional



# def get_variables(arg: str):
#     if arg== "local_directory":
#         directory=os.environ.get("local_directory")
#         if directory is not None:
#             return directory
#         else:
#             return "."
#     if arg== "target_image":
#         print(os.environ.get("train_target_image"))
#         return os.environ.get("train_target_image")
#     if arg == "packages_to_install":
#         package_install= os.environ.get("train_packages_to_install")
#         if package_install is not None:
#             return package_install.split(",")
#         else:
#             pkg=[]
#             return pkg



from kfp.dsl import component
from typing import Callable

def my_dsl_component(base_image: str, target_image: str, packages_to_install: list):
    def decorator(func: Callable):
        return component(
            base_image=base_image,
            target_image=target_image,
            packages_to_install=packages_to_install
        )(func)
    return decorator