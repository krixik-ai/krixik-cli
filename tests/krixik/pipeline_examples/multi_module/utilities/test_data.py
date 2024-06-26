from tests.krixik import text_files_path, audio_files_path, json_files_path, image_files_path, npy_files_path

test_data = {
    "caption-keyword-db": [ 
        {"local_file_path": f"{image_files_path}restaurant.png"},
        ],
    "ocr-vector-db": [
        {"local_file_path": f"{image_files_path}seal.png"}
    ],
    "standard-vector-db": [
        {"local_file_path": f"{text_files_path}1984_short.txt"}
    ],
    "transcribe-vector-db": [
        {"local_file_path": f"{audio_files_path}valid_1.mp3"}
    ],
    "transcribe-translate-vector-db": [
        {"local_file_path": f"{audio_files_path}valid_1.mp3"}
    ],
    "summarize-keyword-db": [
        {"local_file_path": f"{text_files_path}1984_short.txt"}
    ],
}