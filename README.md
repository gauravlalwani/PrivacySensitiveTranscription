# csh-crowdsourcing

### Setting up the development environment:
Use virtual environments to create project-specific development environments and thereby use project-specific dependencies.

Example setup for Ubuntu:
```
# install pip and virtualenv
sudo apt-get install python-pip
sudo pip install virtualenv

# clone and cd into the directory
git clone https://github.com/ColoredInsaneAsylums/PrivacySensitiveTranscription.git
cd PrivacySensitiveTranscription

# create and start new virtualenv
virtualenv -p python3 venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Adding new dependencies:
```
pip install <some-package>
pip freeze > requirements.txt
```

Deactivating the virtual environment:
```
deactivate
```
