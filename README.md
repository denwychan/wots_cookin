# Wots Cookin

Wots Cookin is an ingredients-to-recipes recommender, which gives the user ideas for meals and drinks based on a list of input ingredients.

## User Journey

- The user lists the ingredients via speech into the web app
- Wots Cookin searches the recipe bank
- Wots Cookin returns an ordered list of best matching recipes with a match score

## High Level Architecture

1. Wots Cookin is built on a Streamlit web app
2. The user's voice is translated into text via the Google speech-to-text API
3. The ingredients are used as an input into the Wots Cookin search algorithms
4. The Streamlit web app displays the results back to the user

## Data Source
A small Kaggle [dataset](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images) with approximately 13.5k records is used for the Wots Cookin recipes bank. The source data has 6 features:

1. Row number
2. Title - for the food dish
3. Ingredients
4. Instructions
5. Image Name
6. Cleaned Ingredients - a comma separated version of the 'Ingredients' feature

The dataset is cleaned and enriched further for Wots Cookin. Please see more in the Workflow section.

## Workflow

## UI Elements




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
Additional installation steps:
- Install ffmpeg using preferred package manager of choice (e.g. brew)
- Enable Google Speech-to-Text API on GCP

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
wots_cookin-run
```
