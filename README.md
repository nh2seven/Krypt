# Krypt
- Krypt is an entirely local/offline password manager built using Python and SQLite, with encryption and decryption mechanisms in place for better security.
- With Krypt, you can store all your passwords and/or credentials safely, without the risk of ever exposing yourself to the internet.
> Strong disclaimer: At the moment, Krypt is still in active rapid development. Contributions are welcome.

# Features
- Multi-user system that stores credentials independent of user.
- Storage of user credentials along with associated websites, tags, descriptions and individual keys if enabled.
- Grouping of user credentials.
- In-built password generator.
- Logging of system activities to track user activity and potentially identify rare cases of unauthorized access.

# Installation
To install Krypt, clone the repository and install the required dependencies:
```sh
git clone https://github.com/nh2seven/Krypt.git
cd Krypt
pip install -r requirements.txt
```
Creating a new python environment via [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) is recommended, prior to installation.

# Usage
To run/use Krypt, run:
```sh
python main.py
```
in a terminal. A more streamlined usage method will be added sometime in the future.

# License
This project is licensed under the GNU General Public License (Version 3). Check out the [LICENSE](LICENSE) file for details.

# Attributions
- Significant parts of the frontend have been made using components from [PyQt6](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PyQt6), following its [documentation](https://qfluentwidgets.com/pages/about/).
- Icons used in the app are from the open-sourced [Iconify Material Symbols](https://icon-sets.iconify.design/material-symbols/) collection.
- This project is made as part of the requirements for the Database Management Systems course project at PES University, RR Campus, Bangalore.