import csv
import os
import glob

from typing import List

from .utils.types import *
import pkg_resources

COLUMNS = ("Key", "English", "French", "German", "Polish", "Spanish", "Italian",
            "Swedish", "Czech", "Hungarian", "Dutch", "Portuguese", "Russian", "Finnish")


class GameFile:
    """Initializes the parser

    Parameters
    ----------
    localisation_folder: :class:`str` or :class:`list` or :class:`None`
        Indicates a localisation folder with .csv files.
    lang: :class:`str`
        Indicates the language to translate.
    """
    def __init__(self, localisation_folder=pkg_resources.resource_listdir("pyvic2waranalyzer", "localisation"), lang="English"):
        self.__localisations = {}
        self.file = None
        self.__reader = None
        self.__lang_index = 1
        for pos, language in enumerate(COLUMNS, 0):
            if language == "Key":
                continue
            if lang.lower() == language.lower():
                self.__lang_index = pos
        # print(localisation_folder)
        if localisation_folder:
            if isinstance(localisation_folder, list):
                for a in localisation_folder:
                    filename = pkg_resources.resource_filename("pyvic2waranalyzer", os.path.join("localisation", a))
                    # print(filename)
                    # self.file = pkg_resources.resource_string("pyvic2waranalyzer", os.path.join("localisation", a)).decode("latin-1")
                    if filename.endswith(".csv"):
                        with open(filename, "r", newline="", encoding="latin-1", errors="ignore") as self.file:
                            self.file.seek(0)
                            self.__reader = csv.reader(self.file, delimiter=";")
                            next(self.__reader)
                            for _ in self.__reader:
                                try:
                                    # print(_)
                                    self.__localisations.update({_[0]: _[self.__lang_index] if _[self.__lang_index] != "" else _[1]})
                                except IndexError:
                                    pass
            else:
                for filename in glob.glob(os.path.join(localisation_folder, "*.csv")):
                    with open(filename, "r", newline="", encoding="latin-1", errors="ignore") as self.file:
                        self.file.seek(0)
                        self.__reader = csv.reader(self.file, delimiter=";")
                        next(self.__reader)
                        for _ in self.__reader:
                            try:
                                self.__localisations.update({_[0]: _[self.__lang_index] if _[self.__lang_index] != "" else _[1]})
                            except IndexError:
                                pass
        self.__sl = None
        self.__attackerDefender = None
        self.__battleProcessing = False
        self.__warGoalProcessing = False
        self.__OriginalwarGoalProcessing = False
        self.__warProcessing = False
        self.__war = []
        self.__iter_ = 0
        self.__wargoalcounter = 0
        self.__warcounter = 0
        self.__bracketCounter = 0
        self.__wargoal_disabled = False

    @property
    def war(self):
        return self.__war

    def scan(self, filename):
        """Scan the save file, returns a list of :class:`War`

        Parameters
        ----------
        filename: :class:`str` or :class:`bytes`

        Returns
        -------
        List[:class:`War`]
        """
        self.__sl = None
        self.__attackerDefender = None
        self.__battleProcessing = False
        self.__warGoalProcessing = False
        self.__OriginalwarGoalProcessing = False
        self.__warProcessing = False
        self.__war = []
        self.__iter_ = 0
        self.__wargoalcounter = 0
        self.__warcounter = 0
        self.__bracketCounter = 0
        self.__wargoal_disabled = False
        if isinstance(filename, bytes):
            doc = filename.decode("latin-1", errors="ignore")
        elif isinstance(filename, str):
            with open(filename, "r", errors="ignore", encoding="latin-1") as f:
                doc = f.read()
        self.__sl = doc.split("\n")
        for i in range(len(self.__sl) - 3):
            if self.__is_previous_war(i):
                self.__warProcessing = True
                # print("activado")

            if self.__warProcessing:
                # print(self.__sl[i])
                self.__bracketCounterChange(self.__sl[i])

                if "battle=" in self.__sl[i] or self.__battleProcessing:
                    # print(self.__sl[i], "battle")
                    # print("BATALLA", self.__sl[i])
                    if self.__iter_ == 0 or "battle=" in self.__sl[i] and not self.__battleProcessing:
                        # print("created battle", self.__sl[i])
                        if not self.__battleProcessing:
                            self.__war[self.__warcounter].battles.append(Battle())

                    self.__battleProcessing = True
                    self.__BattleReader(self.__sl[i])
                elif "war_goal=" in self.__sl[i] or self.__warGoalProcessing and not self.__wargoal_disabled:
                    if self.__wargoalcounter == 0 or "war_goal=" in self.__sl[i]:
                        if not self.__warGoalProcessing:
                            self.__war[self.__warcounter].wargoals.append(Wargoal())
                    self.__warGoalProcessing = True
                    self.__wargoalreader(self.__sl[i])
                elif "original_wargoal=" in self.__sl[i] or self.__OriginalwarGoalProcessing and not self.__wargoal_disabled:
                    if self.__wargoalcounter == 0 or "original_wargoal=" in self.__sl[i]:
                        if not self.__OriginalwarGoalProcessing:
                            self.__war[self.__warcounter].wargoals.append(OriginalWargoal())
                    self.__OriginalwarGoalProcessing = True
                    self.__wargoalreader(self.__sl[i])
                else:
                    # print("guerra", self.__sl[i])
                    # print(self.__sl[i], "war_parse")
                    self.__war_parse(self.__sl[i])
            try:
                if self.__bracketCounter == 0 and self.__warProcessing and not self.__war[self.__warcounter].name == "":
                    # print(self.__sl[i], "next_war")
                    self.__warGoalProcessing = False
                    self.__wargoalcounter = 0
                    self.__iter_ = 0
                    self.__warcounter += 1
                    self.__warProcessing = False
            except:
                pass
        if self.file:
            self.file.close()
        return self.__war

    def __localize(self, key):
        return self.__localisations.get(key) or key

    def __bracketCounterChange(self, line):
        if "{" in line:
            self.__bracketCounter += 1
        elif "}" in line:
            self.__bracketCounter -= 1

    def __nameextractor(self, line):
        line = line.strip()
        line = line.split("=")[1].replace("'", "")
        return line.replace('"', '')

    def __wargoalreader(self, line):
        # wargoal
        if "state_province_id=" in line:
            # print(line)
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].state = line
        elif "casus_belli=" in line:
            # print(line)
            # print(line)
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].casus_belli = self.__localize(line)
        elif "country=" in line:
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].country = self.__localize(line)
        elif "actor=" in line:
            line = self.__nameextractor(line)
            # print(self.__wargoalcounter, self.__war[self.__warcounter].wargoals[self.__wargoalcounter])
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].actor = self.__localize(line)
        elif "receiver=" in line:
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].receiver = self.__localize(line)
        elif "score=" in line:
            # print(line)
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].score = float(line)
        elif "change=" in line:
            # print(line)
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].change = float(line)
        elif "date=" in line:
            # print(line)
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].date = line
        elif "is_fulfilled=" in line:
            # print(line)
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].wargoals[self.__wargoalcounter].is_fulfilled = True if line == "yes" else False
        elif "}" in line:
            # print(line)
            if not self.__war[self.__warcounter].wargoals[self.__wargoalcounter]:
                del self.__war[self.__warcounter].wargoals[self.__wargoalcounter]
                self.__wargoalcounter -= 1
            self.__warGoalProcessing = False
            self.__OriginalwarGoalProcessing = False
            self.__wargoalcounter += 1

    def __BattleReader(self, line):
        if "name=" in line:
            name = self.__nameextractor(line)
            self.__war[self.__warcounter].battles[self.__iter_].name = name
            self.__attackerDefender = True
        elif "location=" in line:
            location = int(self.__nameextractor(line))
            self.__war[self.__warcounter].battles[self.__iter_].location = location
        elif "result=" in line:
            result_ = True if "yes" in self.__nameextractor(line) else False
            self.__war[self.__warcounter].battles[self.__iter_].result = result_
        elif "country=" in line:
            # print(line)
            line = self.__nameextractor(line)
            if self.__attackerDefender:
                country_atck = line
                self.__war[self.__warcounter].battles[self.__iter_].attacker = self.__localize(country_atck)
            else:
                country_def = line
                self.__war[self.__warcounter].battles[self.__iter_].defender = self.__localize(country_def)
        elif "leader=" in line:
            line = self.__nameextractor(line)
            if self.__attackerDefender:
                leader_atck = line
                self.__war[self.__warcounter].battles[self.__iter_].attackerLeader = leader_atck
            else:
                leader_def = line
                self.__war[self.__warcounter].battles[self.__iter_].defenderLeader = leader_def
        elif "losses=" in line:
            line = int(self.__nameextractor(line))
            if self.__attackerDefender:
                self.__attackerDefender = False
                losses_atck = line
                self.__war[self.__warcounter].battles[self.__iter_].attackerLosses = losses_atck
            else:
                losses_def = line
                self.__war[self.__warcounter].battles[self.__iter_].defenderLosses = losses_def
                if not self.__war[self.__warcounter].battles[self.__iter_]:
                    del self.__war[self.__warcounter].battles[self.__iter_]
                    self.__iter_ -= 1
                self.__iter_ += 1
                self.__battleProcessing = False

        elif "attacker=" not in line and "defender=" not in line and "{" not in line and "}" not in line and "battle=" not in line:
            if self.__attackerDefender:
                line = line.strip()
                first, second = line.split("=")
                second = int(second.replace('"', ''))
                first = self.__localize(first)
                self.__war[self.__warcounter].battles[self.__iter_].attackerArmy.append(Unit(first, second))
            else:
                line = line.strip()
                first, second = line.split("=")
                second = int(second.replace('"', ''))
                first = self.__localize(first)
                self.__war[self.__warcounter].battles[self.__iter_].defenderArmy.append(Unit(first, second))

    def __war_parse(self, line):
        if "name=" in line:
            line = self.__nameextractor(line)
            self.__war.append(War(name=line))
        elif "1=" in line:
            pass
        # elif "add_attacker=" in line:
        #     line = self.__localize(self.__nameextractor(line).strip())
        #     self.__war[self.__warcounter].attackers.append(line)
        # elif "add_defender=" in line:
        #     line = self.__localize(self.__nameextractor(line).strip())
        #     self.__war[self.__warcounter].defenders.append(line)
        elif "attacker=" in line:
            line = self.__localize(self.__nameextractor(line).strip())
            if line != "---":
                if line not in self.__war[self.__warcounter].attackers:
                    self.__war[self.__warcounter].attackers.insert(0, line)
            else:
                pass
        elif "defender=" in line:
            line = self.__localize(self.__nameextractor(line).strip())
            if line != "---":
                if line not in self.__war[self.__warcounter].defenders:
                    self.__war[self.__warcounter].defenders.insert(0, line)
            else:
                pass
        elif "action=" in line:
            line = self.__nameextractor(line)
            self.__war[self.__warcounter].action = line

    def __is_previous_war(self, index):
        return "previous_war=" in self.__sl[index] or "active_war=" in self.__sl[index] and "{" in self.__sl[index + 1] \
            and "name=" in self.__sl[index + 2] \
            and 'American War of Independence' not in self.__sl[index + 2] \
            and 'Texan War of Independence' not in self.__sl[index + 2] \
            and 'Ottoman Restoration of Tripoli' not in self.__sl[index + 2]