# PyVic2WarAnalyzer
_Python module to analyze Victoria 2 save files._\
See the documentation in https://pyvic2waranalyzer.readthedocs.io/en/stable
## Installing

````
pip install pyvic2waranalyzer 
````
This module is a little bit heavy because I included a localisation file from victoria 2 to translate the country tags.\
You can disable the localisation or change the localisation folder if you want to use your own files.
## Code examples

```python
import pyvic2waranalyzer as vic2

save = vic2.GameFile(lang="english") # 'lang' only available when you use localisation files
save = vic2.GameFile(localisation_folder=None) # If you want to disable it
save = vic2.GameFile(localisation_folder="relative/path/to/your/localisation_folder") # If you want to change the directory of the localisation folder


war = save.scan("save game.v2")
for w in war:
    print("War name", w.name)
    print("Wargoal", w.wargoal) 
    print("Battles", w.battles) # list of battles
    print("Started in", w.actor) 
    print("Attackers", w.attackers) # list of attackers
    print("Defenders", w.defenders) # list of defenders
    for b in w.battles:
            print("Battle name", b.name)
            print("result", b.result) # If attacker won it's true else false
            print("attacker army", b.attackerArmy)
            print("defender army", b.defenderArmy)
            print("attacker losses", b.attackerLosses)
            print("defender losses", b.defender.Losses)
            print("total losses", b.total_losses)


# You can also do 
for w in save.war:
    print("War name", w.name)
    print("Wargoal", w.wargoal) 
    print("Battles", w.battles) # list of battles
    print("Started in", w.actor) 
    print("Attackers", w.attackers) # list of attacker
    print("Defenders", w.defenders) # list of defenders
    for b in w.battles:
        print("Battle name", b.name)
        print("result", b.result) # If attacker won it's true else false
        print("attacker army", b.attackerArmy)
        print("defender army", b.defenderArmy)
        print("attacker losses", b.attackerLosses)
        print("defender losses", b.defender.Losses)
        print("total losses", b.total_losses)
```