## the `.process` method

The `.process` api is available to every krixik pipeline.  This api is invoked whenever you want to process files through your defined pipeline.

A table of contents for this section is shown below.

- [core inputs to the `.process` method](#core-inputs-to-the-process-method)
- [basic usage and output breakdown](#basic-usage-and-output-breakdown)
- [optional input arguments](#optional-input-arguments)
- [defaults when using `.process`](#defaults-when-using-process)
- [automatic data type transformations](#automatic-data-type-transformations)

### core inputs to the `.process` method

The api has five basic inputs, as well as a range of optional metdata.  These inputs are

- `local_file_path`:  (required) the path to the local file you wish to process
- `local_save_directory`: (optional) local location for saving process output (defaults to current working directory)
 - `expire_time`: (optional) length of time process output remains on krixik servers (default is 30 minutes / 1800 seconds)
- `wait_for_process`: (optional) whether or not to wait for your process to complete before regaining control of your IDE or notebook - `True` means wait until the process is complete, `False` means regain control immediately after your file has uploaded for processing (default `True`)  When set to `False` the status of processing can be retrieved via [the `.process_status` method](process_status.md)
- `verbose`: (optional) whether to show process update printouts at your terminal / notebook (default `True`)

Lets process a simple file using these core inputs.

### basic usage and output breakdown

We first define a path to a local input file.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
with open(test_file, "r") as file:
    print(file.read())
```

    It was a bright cold day in April, and the clocks were striking thirteen.
    Winston Smith, his chin nuzzled into his breast in an effort to escape the
    vile wind, slipped quickly through the glass doors of Victory Mansions,
    though not quickly enough to prevent a swirl of gritty dust from entering
    along with him.


A paragraph of text consisting of two sentences.

Now let's process it using our sentence parser and explore `.process` inputs.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for search
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False)            # set verbosity to False
```

The output of this process is printed below.  Because the output of this particular module-model pair is json, the process output is provided in the return response.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "parser-pipeline-1",
      "request_id": "e957e17f-ca3c-40bf-afd1-ebca1f27ba51",
      "file_id": "9d94d011-b445-41fa-ae9e-92322726be96",
      "message": "SUCCESS - output fetched for file_id 9d94d011-b445-41fa-ae9e-92322726be96.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
          "line_numbers": [
            1
          ]
        },
        {
          "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
          "line_numbers": [
            2,
            3,
            4,
            5
          ]
        }
      ],
      "process_output_files": [
        "./9d94d011-b445-41fa-ae9e-92322726be96.json"
      ]
    }


Lets break down the output:

- `status_code`: provides the success / failure signal for the api
- `pipeline`: the name of the pipeline we ran `.process` on
- `request_id`: unique id associated with this execution of `.process`
- `file_id`: unique id for the processed file and its associated output
- `message`: message detailing success or failure of call
- `warnings`: message list indicating any warnings related to our call
- `process_output`: returned output (available when module-model output is json only)
- `process_output_files`: list of process output, local file names 

We can see from `process_output` that our two-sentence paragraph input has been separated correctly.  Each sentence also has its corresponding line number(s).

This process output is also stored in the file contained in `process_output_files`.  Lets load it in and confirm we have the same process output we see above.


```python
# load in process output from file
import json
with open(process_output['process_output_files'][0], "r") as file:
    process_output = json.load(file)
    json_print(process_output)
```

    [
      {
        "snippet": "It was a bright cold day in April, and the clocks were striking thirteen.",
        "line_numbers": [
          1
        ]
      },
      {
        "snippet": "Winston Smith, his chin nuzzled into his breast in an effort to escape the\nvile wind, slipped quickly through the glass doors of Victory Mansions,\nthough not quickly enough to prevent a swirl of gritty dust from entering\nalong with him.",
        "line_numbers": [
          2,
          3,
          4,
          5
        ]
      }
    ]


### optional input arguments

 When using the api you may optionally include a variety of process metadata.  
 
These optional do not change how `.process` runs or treats input / output data - they make your process output easier to retrieve and organize.   

Optional inputs include

- `modules`: model and parameter selections for pipeline modules
- `symbolic_directory_path` - a unix formatted directory path (default is `/etc`)
- `file_name` - a custom file name (randomly assigned name by default)
- `file_tags` - a list of custom file tags (none by default)
- `file_description` - a custom file description (none by default)

These three arguments  - `symbolic_directory_path`, `file_name`, and `file_tags` - can be used to retrieve the record of your process at a later time using the [`.list` method](list.md).  They can also be used as filters for search if your pipeline ends with a `keyword-db` [LINK HERE] or `vector-db` [LINK HERE] module.

The `file_description` can be used to provide a description of the file.

Lets use the `.process` method with and without these arguments.


```python
# define path to an input file from examples directory
test_file = "../../examples/input_data/1984_very_short.txt"

# process for parser
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984")
```

The `modules` argument is optional since when not set default model options are made for each module in a pipeline.

To use any non-default model you must define the `modules` input argument when using `.process`.  

For example, the `parser` module has a secondary model called `fixed` which takes in two parameters.  You can employ it in an invocation of `.process` like this (see the [`parser` example](LINK HERE) for further information).

```python
# process using parser
process_output = pipeline.process(local_file_path = test_file,
                                  local_save_directory=".", # save output in current directory
                                  expire_time=60*5,         # set all process data to expire in 5 minutes
                                  wait_for_process=True,    # wait for process to complete before regaining ide
                                  verbose=False,            # set verbosity to False
                                  symbolic_directory_path = "/my/custom/filepath",
                                  file_name = "some_snippets.txt",
                                  file_tags = [{"author": "orwell"}, {"category": "fiction"}],
                                  file_description = "the first paragraph of 1984",
                                  modules={"parser":{"model":"fixed",
                                                     "params":{
                                                         "chunk_size": 10,
                                                         "overlap_size": 2
                                                     }}})
```

### defaults when using `.process`

- if no `file_name` is provided a random name is provided for the process input file of the form `krixik_generated_file_name_{10 random chars}.ext`
where here `ext` is the extension of your input provided by `local_file_path`

- if no value for `symbolic_directory_path` is provided it is set to the default value of `/etc`

- you cannot define `symbolic_directory_path`s that are children of `/etc` - e.g., `/etc/mypath` is not allowed

### automatic data type transformations

The `.process` method automatically transforms the following input data types from `local_file_path`

- `pdf` -> `txt`
- `docx` -> `txt`
- `pptx` -> `txt`
- `mp4` -> `mp3`
