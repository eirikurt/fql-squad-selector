# fpl-squad-selector

These are scripts for picking an optimal [Fantasy Premier League](https://fantasy.premierleague.com/) squad using [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming). This can come in handy when playing the wildcard token.

## Pre-requisites

 - Python 3.11 or later

## How to use

Start by installing the dependencies. If you're using pip then run
```bash
pip install -r requirements.txt
```

Alternatively, you can install the dependencies with [poetry](https://python-poetry.org/) 
```bash
poetry install
```

Then run the script that scrapes player data from the FPL web site

```bash
python a01_get_player_data.py   
```

At this point, you should open the second script named `a02_pick_squad.py` in a text editor. At the top you'll find a few variables that need to be set in a section titled "Things to tweak before running the script". Once you've entered your budget, how many positions to fill etc, save the file and run

```bash
python a02_pick_squad.py
```

Be prepared to wait a few seconds, as the solution space to explore is quite large. When the script finishes it will print out a report like this one

```
  id  name                            cost    points    form    score    team_nr  position
----  ----------------------------  ------  --------  ------  -------  ---------  ----------
 383  André Onana                      5          30     6        6           14  gk
 594  Noussair Mazraoui                4.6        25     4.2      5           14  def
 369  Diogo Dalot Teixeira             5          29     5.5      5.8         14  def
   3  Gabriel dos Santos Magalhães     6          36     7.5      7.2          1  def
 328  Mohamed Salah                   12.8        49     8.8      9.8         12  mid
 327  Luis Díaz                        7.9        51    12       10.2         12  mid
  19  Emile Smith Rowe                 5.7        30     6.8      6            9  mid
 177  Noni Madueke                     6.6        28     7        7            6  mid
 351  Erling Haaland                  15.3        63    14       12.6         13  fwd
 180  Nicolas Jackson                  7.7        35     8.2      7            6  fwd
 148  Danny Welbeck                    5.8        31     4.8      6.2          5  fwd
```
