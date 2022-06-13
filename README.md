# Data analysis
- Document here the project: wots_cookin
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for wots_cookin in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/wots_cookin`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "wots_cookin"
git remote add origin git@github.com:{group}/wots_cookin.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
wots_cookin-run
```

# Install

Go to `https://github.com/denwychan/wots_cookin` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:denwychan/wots_cookin.git
cd wots_cookin
pip install -r requirements.txt
make clean install test                # install and test
```
Install ffmpeg using preferred package manager of choice (e.g. brew)
Enable Google Speech-to-Text API on GCP

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
wots_cookin-run
```
