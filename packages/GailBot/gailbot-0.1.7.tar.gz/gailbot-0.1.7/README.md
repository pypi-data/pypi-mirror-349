# GailBot

## About

Researchers studying human interaction, such as conversation analysts, psychologists, and linguists all rely on detailed transcriptions of language use. Ideally, these should include so-called paralinguistic features of talk, such as overlaps, prosody, and intonation, as they convey important information. However, transcribing these features by hand requires substantial amounts of time by trained transcribers. There are currently no Speech to Text (STT) systems that are able to annotate these features. To reduce the resources needed to create transcripts that include paralinguistic features, we developed a program called GailBot. GailBot combines STT services with plugins to automatically generate first drafts of conversation analytic transcripts. It also enables researchers to add new plugins to transcribe additional features, or to improve the plugins it currently uses. We argue that despite its limitations, GailBot represents a substantial improvement over existing dialogue transcription software.

Find the full paper published by Dialogue and Discourse [here](https://journals.uic.edu/ojs/index.php/dad/article/view/11392).


## Status

GailBot version: 0.2a5
Release type: API


## Installation

You will need run Gailbot with Python Version 3.10. GailBot and the necessary dependencies can be installed using pip with the following commands:
```
pip install --upgrade pip
pip install gailbot
pip install git+https://github.com/m-bain/whisperx.git
```
To use an virtual environment, you can use the following command:
```
conda create --name gailbot-api python==3.10.6
conda activate gailbot-api
pip install --upgrade pip
pip install gailbot
pip install git+https://github.com/m-bain/whisperx.git

```

## Usage - GailBot API

This release features a convenient API to use GailBot and create custom plugin suites. To use the API and its features, import the GailBot package like the following:

```
from gailbot import GailBot
```

Once you have imported the GailBot package, initialize an instance of GailBot called "gb" (or a name of your choosing) by doing the following ("ws_root" is takes a path to your workspace directory):

```
gb = GailBot()
```
The GailBot API's methods are now available through your GailBot instance. Check out GailBot's backend documentation for a full list of method and their uses [here](https://gailbot-release-document.s3.us-east-2.amazonaws.com/Documentation/Backend_Technical_Documentation.pdf).


### Example Usage 1 - Default Settings
Now, we will try to use the GailBot on an input audio file.
To do so, we will need initiate a GailBot instance, add input audio file as source, and transcribe. 
This example uses GailBot's default settings with default engine (Whisper) and pre-installed plugin suite. Therefore, there is no need to create and apply profile settings.
See the example below:
```
from gailbot import GailBot

gb = GailBot()
gb.add_source(
    source_path="your_source_file_path"
    output_dir="your_output_directory_path"
)
gb.transcribe()
```

### Example Usage 2 - Custom Profile
Here is an example of using GailBot with your customized transcription profile.
To do so, you'll need to create a profile and apply it to input source files before transcribing with GailBot.
See example on how to create a profile:

```
gb = GailBot()
google_api = "path/to/google-api.json"
input = "path/to/source"
output = "path/to/source"

google_engine_setting = {"engine": "google", "google_api_key": google_api}
google_engine_name = "google engine"
gb.add_engine(name=google_engine_name, setting=google_engine_setting)

google_profile_setting = ProfileSetting(
    engine_setting_name=google_engine_name,
    plugin_suite_setting={
        "HiLabSuite": ["XmlPlugin", "ChatPlugin", "TextPlugin", "CSVPlugin"]
    },
)
google_profile_name = "google profile"
gb.create_profile(name=google_profile_name, setting=google_profile_setting)

source_id = gb.add_source(input, output)
gb.apply_profile_to_source(source_id=source_id, profile_name=google_profile_name)
google_transcription_result = gb.transcribe()
```
In the example above, we added Google Cloud STT engine called "google engine" using your Google engine API key.
Then, we used the Google engine to create a new profile called "google profile" . Here we also use GailBot's default plugin suite called HiLabSuite.
Finally, we apply our custom profile to our input source and transcribe.


## Supported Plugin Suites

A core GailBot feature is its ability to apply plugin suites during the transcription process. While different use cases may require custom plugins, the Human Interaction Lab maintains and distributes a pre-developed plugin suite -- HiLabSuite. For more information about the default plugin suite, click [here](https://sites.tufts.edu/hilab/gailbot-an-automatic-transcription-system-for-conversation-analysis/).

### Custom Plugins

A core GailBot feature is its ability to allow researchers to develop and add custom plugins that may be applied during the transcription process, in addition to the provided built-in HiLabSuite. To create a compatible plugin suite for the Gailbot app, follow these steps:

1. Prepare the Folder Structure and Files:
Ensure your plugin suite directory contains the following files with specific names: "init.py," "CHANGELOG.md," "DOCUMENT.md," "TECH_DOCUMENT.md," "README.md," "format.md," and "config.toml." Include a subfolder named "src" within the main directory.

    File Descriptions:

    init.py: Used for package initialization and can be left empty.
    format.md: Provides users information about generated output files.
    CHANGELOG.md: Documents version-to-version changes.
    README.md: Offers a high-level explanation and purpose of the plugin suite.
    DOCUMENT.md: Contains specifics about algorithms, plugins, and developers.
    TECH_DOCUMENT.md: Explains technical aspects like logging implementation.
    config.toml: Vital file that outlines plugin execution order and settings.

2. Configure config.toml:
Begin with setting suite_name = "<mySuite>", matching the directory name. Define metadata in the [metadata] section, including Author, Email, and Version.

3. Define Plugins:
For each plugin, create a section in config.toml under plugins section. Specify plugin_name, dependencies, rel_path, and module_name.

    plugin_name: The name of your plugin.
    dependencies: A list of plugins needed before this one.
    rel_path: Path to the file with the plugin's apply function.
    module_name: The name of the file without the .py suffix.

4. Plugin Coding:
Define each plugin as a class with the exact name from plugin_name.
Inside the class, include an apply function with the signature def apply(self, dependency_outputs: Dict[str, Any], methods: <your methods>).
At the end of the apply function, set self.is_successful = True.

5. Dependencies and Output Flow:
Use the dependency_outputs dictionary to pass outputs between plugins.
When a plugin depends on another, it receives previous plugin outputs through this dictionary, with plugin class name as the key.
Ensure plugin classes are properly formatted in config.toml for the apply function to run.

With correctly structured files, codes, and dependencies, your plugins will run as intended when uploaded to Gailbot. 
Congratulations on creating your plugin suite for Gailbot, and thank you for following our tutorial! Happy transcribing!


## Contribute

Users are encouraged to direct installation and usage questions, provide feedback, details regarding bugs, and development ideas by [email](mailto:hilab-dev@elist.tufts.edu).


## Acknowledgements

Special thanks to members of the [Human Interaction Lab](https://sites.tufts.edu/hilab/) at Tufts University and interns that have worked on this project.


## Cite

Users are encouraged to cite GailBot using the following BibTex:
```
@article{umair2022gailbot,
  title={GailBot: An automatic transcription system for Conversation Analysis},
  author={Umair, Muhammad and Mertens, Julia Beret and Albert, Saul and de Ruiter, Jan P},
  journal={Dialogue \& Discourse},
  volume={13},
  number={1},
  pages={63--95},
  year={2022}
}
```

## Liability Notice

Gailbot is a tool to be used to generate specialized transcripts. However, it
is not responsible for output quality. Generated transcripts are meant to
be first drafts that can be manually improved. They are not meant to replace
manual transcription.

GailBot may use external Speech-to-Text systems or third-party services. The
development team is not responsible for any transactions between users and these
services. Additionally, the development team does not guarantee the accuracy or 
correctness of any plugin. Plugins have been developed in good faith and we hope 
that they are accurate. However, users should always verify results.

By using GailBot, users agree to cite Gailbot and the Tufts Human Interaction Lab
in any publications or results as a direct or indirect result of using Gailbot.