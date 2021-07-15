import csv
import os
import glob
from utils.types import *

# COLUMNS = ("Key", "English", "French", "German", "Polish", "Spanish", "Italian",
#            "Swedish", "Czech", "Hungarian", "Dutch", "Portuguese", "Russian", "Finnish")


class GameFile:
    def __init__(self, localisation_folder=os.path.join("localisation")):
        self.localisations = {}
        self.file = None
        self.reader = None
        if localisation_folder:
            for a in glob.glob(os.path.join(localisation_folder, "*.csv")):
                with open(a, "r", newline="", encoding="latin-1", errors="ignore") as self.file:
                    self.file.seek(0)
                    self.reader = csv.reader(self.file, delimiter=";")
                    next(self.reader)
                    for _ in self.reader:
                        try:
                            self.localisations.update({_[0]: _[1]})
                        except IndexError:
                            pass
        self.sl = None
        self.attackerDefender = None
        self.battleProcessing = False
        self.warGoalProcessing = False
        self.warProcessing = False
        self.war = []
        self.iter_ = 0
        self.wargoalcounter = 0
        self.warcounter = 0
        self.bracketCounter = 0
        self.wargoal_disabled = False

    def scan(self, filename):
        self.sl = None
        self.attackerDefender = None
        self.battleProcessing = False
        self.warGoalProcessing = False
        self.warProcessing = False
        self.war = []
        self.iter_ = 0
        self.wargoalcounter = 0
        self.warcounter = 0
        self.bracketCounter = 0
        self.wargoal_disabled = False
        if isinstance(filename, bytes):
            doc = filename.decode("latin-1", errors="ignore")
        elif isinstance(filename, str):
            with open(filename, "r", errors="ignore", encoding="latin-1") as f:
                doc = f.read()
        self.sl = doc.split("\n")
        for i in range(len(self.sl) - 3):
            if self.is_previous_war(i):
                self.warProcessing = True
                # print("activado")

            if self.warProcessing:
                # print(self.sl[i])
                self.bracketCounterChange(self.sl[i])

                if "battle=" in self.sl[i] or self.battleProcessing:
                    # print("BATALLA", self.sl[i])
                    self.battleProcessing = True
                    self.BattleReader(self.sl[i])
                elif "war_goal=" in self.sl[i] or "original_wargoal=" in self.sl[i] or self.warGoalProcessing and not self.wargoal_disabled:
                    self.warGoalProcessing = True
                    self.wargoalreader(self.sl[i])
                else:
                    # print("guerra", self.sl[i])
                    self.war_parse(self.sl[i])
            try:
                if self.bracketCounter == 0 and self.warProcessing and not self.war[self.warcounter].name == "":
                    self.warGoalProcessing = False
                    self.wargoalcounter = 0
                    self.iter_ = 0
                    self.warcounter += 1
                    self.warProcessing = False
            except:
                pass
        if self.file:
            self.file.close()
        return self.war

    def localize(self, key):
        return self.localisations.get(key) or key

    def bracketCounterChange(self, line):
        if "{" in line:
            self.bracketCounter += 1
        elif "}" in line:
            self.bracketCounter -= 1

    def nameextractor(self, line):
        line = line.strip()
        line = line.split("=")[1].replace("'", "")
        return line.replace('"', '')

    def wargoalreader(self, line):
        # wargoal[self.wargoalcounter]
        if "state_province_id=" in line:
            # print(line)
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal = Wargoal(state=int(line))
        elif "casus_belli" in line:
            # print(line)
            # print(line)
            line = self.nameextractor(line)
            try:
                self.war[self.warcounter].wargoal.casus_belli = self.localize(line)
            except:
                self.war[self.warcounter].wargoal = Wargoal(casus_belli=self.localize(line))
        elif "country=" in line:
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal.country = self.localize(line)
        elif "actor=" in line:
            line = self.nameextractor(line)
            # print(self.wargoalcounter, self.war[self.warcounter].wargoal)
            self.war[self.warcounter].wargoal.actor = self.localize(line)
        elif "receiver=" in line:
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal.receiver = self.localize(line)
        elif "score=" in line:
            # print(line)
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal.score = float(line)
        elif "change=" in line:
            # print(line)
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal.change = float(line)
        elif "date=" in line:
            # print(line)
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal.date = line
        elif "is_fulfilled=" in line:
            # print(line)
            line = self.nameextractor(line)
            self.war[self.warcounter].wargoal.is_fulfilled = True if line == "yes" else False
        elif "}" in line:
            # print(line)
            self.warGoalProcessing = False
            self.wargoalcounter += 1

    def BattleReader(self, line):
        if "name=" in line:
            name = self.nameextractor(line)
            self.war[self.warcounter].battles.append(Battle(name=name))
            self.attackerDefender = True
        elif "location=" in line:
            location = int(self.nameextractor(line))
            self.war[self.warcounter].battles[self.iter_].location = location
        elif "result=" in line:
            result_ = True if "yes" in self.nameextractor(line) else False
            self.war[self.warcounter].battles[self.iter_].result = result_
        elif "country=" in line:
            # print(line)
            line = self.nameextractor(line)
            if self.attackerDefender:
                country_atck = line
                self.war[self.warcounter].battles[self.iter_].attacker = self.localize(country_atck)
            else:
                country_def = line
                self.war[self.warcounter].battles[self.iter_].defender = self.localize(country_def)
        elif "leader=" in line:
            line = self.nameextractor(line)
            if self.attackerDefender:
                leader_atck = line
                self.war[self.warcounter].battles[self.iter_].attackerLeader = leader_atck
            else:
                leader_def = line
                self.war[self.warcounter].battles[self.iter_].defenderLeader = leader_def
        elif "losses=" in line:
            line = int(self.nameextractor(line))
            if self.attackerDefender:
                self.attackerDefender = False
                losses_atck = line
                self.war[self.warcounter].battles[self.iter_].attackerLosses = losses_atck
            else:
                losses_def = line
                self.war[self.warcounter].battles[self.iter_].defenderLosses = losses_def
                self.iter_ += 1
                self.battleProcessing = False

        elif "attacker=" not in line and "defender=" not in line and "{" not in line and "}" not in line and "battle=" not in line:
            if self.attackerDefender:
                line = line.strip()
                first, second = line.split("=")
                second = int(second.replace('"', ''))
                first = self.localize(first)
                self.war[self.warcounter].battles[self.iter_].attackerArmy.update({first: second})
            else:
                line = line.strip()
                first, second = line.split("=")
                second = int(second.replace('"', ''))
                first = self.localize(first)
                self.war[self.warcounter].battles[self.iter_].defenderArmy.update({first: second})

    def war_parse(self, line):
        if "name=" in line:
            line = self.nameextractor(line)
            self.war.append(War(name=line))
        elif "1=" in line:
            pass
        elif "add_attacker=" in line:
            line = self.localize(self.nameextractor(line).strip())
            self.war[self.warcounter].attackers.append(line)
        elif "add_defender=" in line:
            line = self.localize(self.nameextractor(line).strip())
            self.war[self.warcounter].defenders.append(line)
        elif "attacker=" in line:
            line = self.localize(self.nameextractor(line).strip())
            if line not in self.war[self.warcounter].attackers:
                self.war[self.warcounter].attackers.insert(0, line)
        elif "defender=" in line:
            line = self.localize(self.nameextractor(line).strip())
            if line not in self.war[self.warcounter].defenders:
                self.war[self.warcounter].defenders.insert(0, line)
        elif "action=" in line:
            line = self.nameextractor(line)
            self.war[self.warcounter].action = line

    def is_previous_war(self, index):
        return "previous_war=" in self.sl[index] or "active_war=" in self.sl[index] and "{" in self.sl[
            index + 1] and "name=" in self.sl[
                   index + 2] and not 'name="American War of Independence"' in self.sl[index + 2]