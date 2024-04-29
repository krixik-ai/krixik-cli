# transcription with sentiment analysis pipeline

This document details a modular pipeline that takes in an audio/video file in the english language, transcribes it, and then performs sentiment analysis on each sentence of the transcript.

To follow along with this demonstration be sure to initialize your krixik session with your api key and url as shown below. 

We illustrate loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you inadvertantly push secrets to a repo).



```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os
load_dotenv("../../.env")
MY_API_KEY = os.getenv('MY_API_KEY')
MY_API_URL = os.getenv('MY_API_URL')

# import krixik and initialize it with your personal secrets
from krixik import krixik
krixik.init(api_key = MY_API_KEY, 
            api_url = MY_API_URL)
```

    SUCCESS: You are now authenticated.


This small function prints dictionaries very nicely in notebooks / markdown.


```python
# print dictionaries / json nicely in notebooks / markdown
import json
def json_print(data):
    print(json.dumps(data, indent=2))
```

A table of contents for the remainder of this document is shown below.


- [pipeline setup](#pipeline-setup)
- [processing a file](#processing-a-file)
- [saving the pipeline config for future use](#saving-the-pipeline-config-for-future-use)

## pipeline setup

Below we setup a multi module pipeline to serve our intended purpose, which is to build a pipeline that will transcribe any audio/video and make it semantically searchable in any language.

To do this we will use the following modules:

- [`transcribe`](modules/transcribe.md): takes in audio/video input, outputs json of content transcription
- [`json-to-txt`](modules/json-to-txt.md): takes in json of text snippets, merges into text file
- [`parser`](modules/parser.md): takes in text, slices into (possibly overlapping) strings
- [`sentiment`](modules/sentiment): takes in text snippets and returns scores for their sentiments


```python
from krixik.pipeline_builder.module import Module
from krixik.pipeline_builder.pipeline import CreatePipeline

# select modules
module_1 = Module(module_type="transcribe")
module_2 = Module(module_type="json-to-txt")
module_3 = Module(module_type="parser")
module_4 = Module(module_type="sentiment")

# create custom pipeline object
custom = CreatePipeline(name='transcribe-sentiment-pipeline', 
                        module_chain=[module_1, module_2, module_3, module_4])

# pass the custom object to the krixik operator (note you can also do this by passing its config)
pipeline = krixik.load_pipeline(pipeline=custom)
```

With our `custom` pipeline built we now pass it, along with a test file, to our operator to process the file.

## processing a file

We first define a path to a local input file.


```python
# define path to an input file
test_file = "../../input_data/Interesting Facts About Colombia.mp4"
```

Lets take a quick look at this file before processing.


```python
# examine contents of input file
from IPython.display import Video
Video(test_file)
```




<video src="../../input_data/Interesting Facts About Colombia.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



For this run we will use the default models for the entire chain of modules.


```python
# test file
test_file = "../../input_data/Interesting Facts About Colombia.mp4"

# process test input
process_output = pipeline.process(local_file_path = test_file,
                                  expire_time=60*5)
```

    INFO: Checking that file size falls within acceptable parameters...
    INFO:...success!
    converted ../../input_data/Interesting Facts About Colombia.mp4 to: /var/folders/k9/0vtmhf0s5h56gt15mkf07b1r0000gn/T/tmpas8o2_np/krixik_converted_version_Interesting Facts About Colombia.mp3
    INFO: hydrated input modules: {'transcribe': {'model': 'whisper-tiny', 'params': {}}, 'json-to-txt': {'model': 'base', 'params': {}}, 'parser': {'model': 'sentence', 'params': {}}, 'sentiment': {'model': 'distilbert-base-uncased-finetuned-sst-2-english', 'params': {}}}
    INFO: symbolic_directory_path was not set by user - setting to default of /etc
    INFO: file_name was not set by user - setting to random file name: krixik_generated_file_name_gndqwwmyqb.mp3
    INFO: wait_for_process is set to True.
    INFO: file will expire and be removed from you account in 300 seconds, at Mon Apr 29 15:42:13 2024 UTC
    INFO: transcribe-sentiment-pipeline file process and input processing started...
    INFO: metadata can be updated using the .update api.
    INFO: This process's request_id is: e3bdba39-9c7f-ea8d-05c8-2e83a524bbbe
    INFO: File process and processing status:
    SUCCESS: module 1 (of 4) - transcribe processing complete.
    SUCCESS: module 2 (of 4) - json-to-txt processing complete.
    SUCCESS: module 3 (of 4) - parser processing complete.
    SUCCESS: module 4 (of 4) - sentiment processing complete.
    SUCCESS: pipeline process complete.
    SUCCESS: process output downloaded


The output of this process is printed below.  Because the output of this particular pipeline is a json file, the process output is shown with output.  The local address of the output file itself has been returned to the address noted in the `process_output_files` key.


```python
# nicely print the output of this process
json_print(process_output)
```

    {
      "status_code": 200,
      "pipeline": "transcribe-sentiment-pipeline",
      "request_id": "bca798e6-85de-4f8a-9974-744108545dae",
      "file_id": "dfaced90-11ed-41c8-9bf0-8751656be563",
      "message": "SUCCESS - output fetched for file_id dfaced90-11ed-41c8-9bf0-8751656be563.Output saved to location(s) listed in process_output_files.",
      "warnings": [],
      "process_output": [
        {
          "snippet": " That's the episode looking at the great country of Columbia.",
          "positive": 0.993,
          "negative": 0.007,
          "neutral": 0.0
        },
        {
          "snippet": "We looked at some really basic facts.",
          "positive": 0.252,
          "negative": 0.748,
          "neutral": 0.0
        },
        {
          "snippet": "It's name, a bit of its history, the type of people that live there, land size, and all that jazz.",
          "positive": 0.998,
          "negative": 0.002,
          "neutral": 0.0
        },
        {
          "snippet": "But in this video, we're going to go into a little bit more of a detailed look.",
          "positive": 0.992,
          "negative": 0.008,
          "neutral": 0.0
        },
        {
          "snippet": "Yo, what is going on guys?",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "Welcome back to F2D facts.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "The channel where I look at people cultures and places.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "My name is Dave Wouple, and today we are going to be looking more at Columbia and our Columbia part two video.",
          "positive": 0.027,
          "negative": 0.973,
          "neutral": 0.0
        },
        {
          "snippet": "Which just reminds me guys, this is part of our Columbia playlist.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "So put it down in the description box below, and I'll talk about that more in the video.",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "But if you're new here, join me every single Monday to learn about new countries from around the world.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "You can do that by hitting that subscribe and that belt notification button.",
          "positive": 0.016,
          "negative": 0.984,
          "neutral": 0.0
        },
        {
          "snippet": "But let's get started.",
          "positive": 0.03,
          "negative": 0.97,
          "neutral": 0.0
        },
        {
          "snippet": "Learn about Columbia.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "So we all know Columbia is famous for its coffee, right?",
          "positive": 0.977,
          "negative": 0.023,
          "neutral": 0.0
        },
        {
          "snippet": "Yes, right.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "I know.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "You guys are sitting there going, five bucks says he's going to talk about coffee.",
          "positive": 0.974,
          "negative": 0.026,
          "neutral": 0.0
        },
        {
          "snippet": "Well, I am.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "That's right, because I got my van.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "You Columbia coffee right here.",
          "positive": 0.407,
          "negative": 0.593,
          "neutral": 0.0
        },
        {
          "snippet": "Boom advertisement.",
          "positive": 0.944,
          "negative": 0.056,
          "neutral": 0.0
        },
        {
          "snippet": "Yeah.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "Then I'm paying me for this.",
          "positive": 0.217,
          "negative": 0.783,
          "neutral": 0.0
        },
        {
          "snippet": "I'm care.",
          "positive": 1.0,
          "negative": 0.0,
          "neutral": 0.0
        },
        {
          "snippet": "So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up.",
          "positive": 0.039,
          "negative": 0.961,
          "neutral": 0.0
        },
        {
          "snippet": "Starbucks buys all had a coffee from Columbia.",
          "positive": 0.048,
          "negative": 0.952,
          "neutral": 0.0
        },
        {
          "snippet": "It's kind of like their favorite place to buy coffee.",
          "positive": 0.995,
          "negative": 0.005,
          "neutral": 0.0
        },
        {
          "snippet": "And kind of to pay tribute to that Starbucks when they're making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia.",
          "positive": 0.968,
          "negative": 0.032,
          "neutral": 0.0
        },
        {
          "snippet": "And this was in the town of Medellin, Columbia.",
          "positive": 0.13,
          "negative": 0.87,
          "neutral": 0.0
        },
        {
          "snippet": "Now here's the thing, when it comes to coffee in Columbia, they are the third largest producing and exporting coffee country in the world.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "The amount of coffee that is exported from Columbia equals about 810,000 metric tons or approximately 11.5 million bags.",
          "positive": 0.043,
          "negative": 0.957,
          "neutral": 0.0
        },
        {
          "snippet": "However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of bean known as the Arab Beka bean.",
          "positive": 0.999,
          "negative": 0.001,
          "neutral": 0.0
        },
        {
          "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture.",
          "positive": 0.005,
          "negative": 0.995,
          "neutral": 0.0
        },
        {
          "snippet": "Interesting fact that in 2007, major spots equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site.",
          "positive": 0.996,
          "negative": 0.004,
          "neutral": 0.0
        },
        {
          "snippet": "And also in 2007, the EU, the European Union, granted Colombian coffee a protected designation of origin status.",
          "positive": 0.995,
          "negative": 0.005,
          "neutral": 0.0
        },
        {
          "snippet": "Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
          "positive": 0.979,
          "negative": 0.021,
          "neutral": 0.0
        },
        {
          "snippet": "It's come from somewhere else, not really an invasive species because it's very much welcomed.",
          "positive": 0.997,
          "negative": 0.003,
          "neutral": 0.0
        },
        {
          "snippet": "Now you may have also seen this guy on many different Colombian coffee brands.",
          "positive": 0.978,
          "negative": 0.022,
          "neutral": 0.0
        },
        {
          "snippet": "Now his name is Juan Valdez.",
          "positive": 0.989,
          "negative": 0.011,
          "neutral": 0.0
        },
        {
          "snippet": "Now some people think that this guy is actually really a real coffee farmer, somebody just drew.",
          "positive": 0.011,
          "negative": 0.989,
          "neutral": 0.0
        }
      ],
      "process_output_files": [
        "/Users/jeremywatt/Desktop/krixik-cli/docs/examples/transcribe/dfaced90-11ed-41c8-9bf0-8751656be563.json"
      ]
    }


We can also load the output from file to see the pipeline output.


```python
# load in process output from file
with open(process_output['process_output_files'][0], "r") as file:
   json_print(json.load(file))
```

    [
      {
        "snippet": " That's the episode looking at the great country of Columbia.",
        "positive": 0.993,
        "negative": 0.007,
        "neutral": 0.0
      },
      {
        "snippet": "We looked at some really basic facts.",
        "positive": 0.252,
        "negative": 0.748,
        "neutral": 0.0
      },
      {
        "snippet": "It's name, a bit of its history, the type of people that live there, land size, and all that jazz.",
        "positive": 0.998,
        "negative": 0.002,
        "neutral": 0.0
      },
      {
        "snippet": "But in this video, we're going to go into a little bit more of a detailed look.",
        "positive": 0.992,
        "negative": 0.008,
        "neutral": 0.0
      },
      {
        "snippet": "Yo, what is going on guys?",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "Welcome back to F2D facts.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "The channel where I look at people cultures and places.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "My name is Dave Wouple, and today we are going to be looking more at Columbia and our Columbia part two video.",
        "positive": 0.027,
        "negative": 0.973,
        "neutral": 0.0
      },
      {
        "snippet": "Which just reminds me guys, this is part of our Columbia playlist.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "So put it down in the description box below, and I'll talk about that more in the video.",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "But if you're new here, join me every single Monday to learn about new countries from around the world.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "You can do that by hitting that subscribe and that belt notification button.",
        "positive": 0.016,
        "negative": 0.984,
        "neutral": 0.0
      },
      {
        "snippet": "But let's get started.",
        "positive": 0.03,
        "negative": 0.97,
        "neutral": 0.0
      },
      {
        "snippet": "Learn about Columbia.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "So we all know Columbia is famous for its coffee, right?",
        "positive": 0.977,
        "negative": 0.023,
        "neutral": 0.0
      },
      {
        "snippet": "Yes, right.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "I know.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "You guys are sitting there going, five bucks says he's going to talk about coffee.",
        "positive": 0.974,
        "negative": 0.026,
        "neutral": 0.0
      },
      {
        "snippet": "Well, I am.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "That's right, because I got my van.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "You Columbia coffee right here.",
        "positive": 0.407,
        "negative": 0.593,
        "neutral": 0.0
      },
      {
        "snippet": "Boom advertisement.",
        "positive": 0.944,
        "negative": 0.056,
        "neutral": 0.0
      },
      {
        "snippet": "Yeah.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "Then I'm paying me for this.",
        "positive": 0.217,
        "negative": 0.783,
        "neutral": 0.0
      },
      {
        "snippet": "I'm care.",
        "positive": 1.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      {
        "snippet": "So which might not know about coffee is yes, you probably already know that a lot of companies actually buy it up.",
        "positive": 0.039,
        "negative": 0.961,
        "neutral": 0.0
      },
      {
        "snippet": "Starbucks buys all had a coffee from Columbia.",
        "positive": 0.048,
        "negative": 0.952,
        "neutral": 0.0
      },
      {
        "snippet": "It's kind of like their favorite place to buy coffee.",
        "positive": 0.995,
        "negative": 0.005,
        "neutral": 0.0
      },
      {
        "snippet": "And kind of to pay tribute to that Starbucks when they're making their 1,000th store in 2016, they decided, yo, we're going to put it in Columbia.",
        "positive": 0.968,
        "negative": 0.032,
        "neutral": 0.0
      },
      {
        "snippet": "And this was in the town of Medellin, Columbia.",
        "positive": 0.13,
        "negative": 0.87,
        "neutral": 0.0
      },
      {
        "snippet": "Now here's the thing, when it comes to coffee in Columbia, they are the third largest producing and exporting coffee country in the world.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "The amount of coffee that is exported from Columbia equals about 810,000 metric tons or approximately 11.5 million bags.",
        "positive": 0.043,
        "negative": 0.957,
        "neutral": 0.0
      },
      {
        "snippet": "However, although it might be beaten by countries like Brazil, it is actually the number one or highest country for producing and growing a specific type of bean known as the Arab Beka bean.",
        "positive": 0.999,
        "negative": 0.001,
        "neutral": 0.0
      },
      {
        "snippet": "And I know coffee is really important when it comes to talking about Columbia, but you guys really don't know how important it is with its culture.",
        "positive": 0.005,
        "negative": 0.995,
        "neutral": 0.0
      },
      {
        "snippet": "Interesting fact that in 2007, major spots equaling a buffer zone of approximately 207,000 hectares, which are called the coffee cultural landscape, were considered a UNESCO World Heritage Site.",
        "positive": 0.996,
        "negative": 0.004,
        "neutral": 0.0
      },
      {
        "snippet": "And also in 2007, the EU, the European Union, granted Colombian coffee a protected designation of origin status.",
        "positive": 0.995,
        "negative": 0.005,
        "neutral": 0.0
      },
      {
        "snippet": "Now interesting enough when it comes to the coffee in Columbia, believe it or not, it is not actually native to the country.",
        "positive": 0.979,
        "negative": 0.021,
        "neutral": 0.0
      },
      {
        "snippet": "It's come from somewhere else, not really an invasive species because it's very much welcomed.",
        "positive": 0.997,
        "negative": 0.003,
        "neutral": 0.0
      },
      {
        "snippet": "Now you may have also seen this guy on many different Colombian coffee brands.",
        "positive": 0.978,
        "negative": 0.022,
        "neutral": 0.0
      },
      {
        "snippet": "Now his name is Juan Valdez.",
        "positive": 0.989,
        "negative": 0.011,
        "neutral": 0.0
      },
      {
        "snippet": "Now some people think that this guy is actually really a real coffee farmer, somebody just drew.",
        "positive": 0.011,
        "negative": 0.989,
        "neutral": 0.0
      }
    ]


## saving the pipeline config for future use

You can save the configuration of this pipeline using the `custom` object, and use it later direclty without building it again in python.


```python
# save your config for later use (that way you don't need to re-build in python)
custom.save(config_path='transcribe-sentiment-pipeline.yml')
```

See more about [saving and loading pipeline configuration files](LINNK GOES HERE).
