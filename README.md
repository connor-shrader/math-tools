# math-tools

This project is based off of my [old-math-tools](https://github.com/connor-shrader/old-math-tools) repository, where I made calculators for linear regression and modular exponentiation. This project differs from [old-math-tools](https://github.com/connor-shrader/old-math-tools) because it uses the Flask microframework. This will allow me to make more sophisticated programs, because I will have easy access to Python.

## Accessing the Website

The website can be accessed at [http://shrader-math-tools.herokuapp.com/](http://shrader-math-tools.herokuapp.com/). I deployed the website using [Heroku](https://heroku.com/).

## Tools

Currently, the only tool I have up is a linear regression calculator (similar to the linear regression calculator on [old-math-tools](https://github.com/connor-shrader/old-math-tools)). This calculator differs from the one on [old-math-tools](https://github.com/connor-shrader/old-math-tools) because it uses a better UI and the linear regression line is visualized using Matplotlib.

If I have time this semester, I will try to add more tools.

## Configuration

Some app configurations will be shown in `config.py` in the main directory. However, some configurations (such as `SECRET_KEY`) must be kept hidden. Also, some configurations will differ between local and deployment versions (such as `DEBUG`). To resolve this issue, I have a two additional configuration files. The local version uses `local_config.py`, which I have in my `.gitignore` file. The deployment version uses `deploy_config.py`, which reads from environment variables.

## Runtime and Required Libraries

This project was made using Python 3.9.1 (this version can also be found in `runtime.txt`). The libraries that I used are available in `requirements.txt`.

## Installation

If you wish to reproduce this repository for any reason, follow these steps:

1. Clone this repository

```
git clone https://github.com/connor-shrader/math-tools
```

2. Change into the cloned directory

```
cd shrader-training-systems
```

3. Install the required libraries. Ideally, you should use a virtual environment. For example, using [anaconda](https://www.anaconda.com/), you would run:

```
conda create -n my-new-environment python=3.9.1
conda activate my-new-environment
pip install -r requirements.txt
```

4. Edit `deploy_config.py` to contain your own configuration values. Alternatively, you can create a `local_config.py` file in the same directory. In either case, you should set values for all configurations you see in `deploy_config.py`. For more information about a specific configuration, refer to the documentation for the library that uses the configuration.

5. Run the server

```
python app.py
```
