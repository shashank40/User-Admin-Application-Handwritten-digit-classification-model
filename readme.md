TO CREATE REQUIREMENTS.TXT(Also read important.md)

Kinda mind-blowing how this simple task is so complicated in Python. Here is what I think is the best way to do it automatically.

You need two tools:

1.pipreqs

pip3 install pipreqs

pipreqs will go through your project and only install the packages that your project use. Instead of all the packages in your python environment as pip freeze would do.

But there's a problem with this approach. It does not install the sub-packages.

For example, your project uses pandas==1.3.2. pandas itself uses numpy==1.21.2 among other packages. But pipreqs itself does not write the sub-packages (i.e. numpy) in requirments.txt

This is where you need to combine pipreqs with the second tool.

pip-tools
pip3 install pip-tools

pip-tools will take the packages in requirements.in and generate the requirements.txt with all the sub-packages. For example, if you have pandas==1.3.2 in requirements.in, pip-tools would generate

numpy==1.21.2 # via pandas in requirements.txt.

But you need to manually add the package in requirements.in. Which is prone to mistake and you might forget to do this once in a while.

This is where you can use the first tool.

But both the tools write to requirements.txt. So how do you fix it?

Use the --savepath for pipreqs to write in requirements.in instead of the default requirements.txt.

To do it in one command; just do

 pipreqs --savepath=requirements.in && pip-compile

There you go. Now you don't need to worry about manually maintaining the packages and you're requirements.txt will have all the sub-packages so that your build is deterministic.

TL;DR

pip3 install pipreqs
pip3 install pip-tools
Use the following to build a deterministic requirements.txt

always add libraries/dependencoes with version in requirements.in

then

pip-compile 


 INSTALL DEPENDENCIES
 pip3 install -r requirements.txt


 RUN API SERVER: (stay in root directory)
 uvicorn main:app --reload