# from krixik.modules.utilities.io_validator import is_valid
# from tests.krixik import json_files_path
# import pytest

# test_success_data = [
#      ("vector-db", f"{json_files_path}/valid.npy"),
#  ]

# @pytest.mark.parametrize("module_name, file_path", test_success_data)
# def test_is_valid_success(module_name, file_path):
#     is_valid(module_name, file_path)


# test_failure_data = [
#     ("vector-db", f"{json_files_path}/invalid_1.npy"),
# ]

# @pytest.mark.parametrize("module_name, file_path", test_failure_data)
# def test_is_valid_failure(module_name, file_path):
#     with pytest.raises(ValueError):
#         is_valid(module_name, file_path)
