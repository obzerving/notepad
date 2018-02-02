Notepad

This is an Alexa skill written in Flask-Ask that appends lines of spoken text to a dropbox file and runs on a PythonAnywhere.com server. Though it does not use Amazon Web Services (AWS), you need a developer account to set up the skill.

A typical session:

User: Alexa, open notepad

Alexa: Welcome to notepad. Which notepad should I open?

User: John

Alexa: What should I enter in it?

User: Today was a nice day.

Alexa: I'm ready for the next entry. What is it?

User: Stop

Alexa: Okay

Minimum Requirements:

1. A free account on PythonAnywhere.com

2. A free account on Dropbox.com

3. Developer account on developer.amazon.com

Installation:

The first four steps come from Bjorn Vuylsteker's tutorial at https://blog.craftworkz.co/flask-ask-a-tutorial-on-a-simple-and-easy-way-to-build-complex-alexa-skills-426a6b3ff8bc#.srkoih7l8. I'm only covering the case of a single skill. The pertinent steps are:

1. Log onto https://pythonanywhere.com, select the Web tab, and create a new web app. Select Flask as the Python Web framework and Python 2.7 as the Python version. In his tutorial, Bjorn entered /home/*yourUserName*/mysite/alexa.py as the app's path, so I'll stick with that name.

2. Select the Consoles tab, start a new bash console, and enter the following commands

   a. pip install --user flask-ask
   
   b. pip install dropbox

3. Select the Files tab

   a. Replace the contents of the file /home/*yourUserName*/mysite/alexa.py with the version in this repository.

   b. Upload the file templates.yaml in this repository to the /home/*yourUserName*/mysite/ directory


5. Log onto https://www.dropbox.com/developers and create a new app

   a. Choose the Dropbox API (not Business API)

   b. Choose App folder access (There's no need for full dropbox access).

   c. Name your app (e.g. mynotepad).

   d. Create it

6. The app info page has a Settings tab, which should already be selected. Here, you have the opportunity to change attributes, such as the folder name used by the app. What needs to done is

   a. Scroll down to the Generated access token section and click the Generate button.

   b. In the alexa.py file, replace the string Your_Token_Here with the token.

7. Log onto https://developer.amazon.com and select the Alexa tab.

   a. Click the add a new skill button.

   b. The skill type is Custom Interaction Model

   c. The Name and Invocation Name are both Note Pad

   d. Switch to the Configuration Section

   e. Copy the contents of the intents.txt file in this repository to the "Intent Schema" field.

   f. Copy the contents of the utterances.txt file in this repository to the "Sample Utterances" field

   g. As part of the "Configure the Skill" step, you will need to add the custom slot "CATCHALL" in the configuration section [The list for this custom slot is in this repository under CustomSlot.txt].

8. Try it out!

