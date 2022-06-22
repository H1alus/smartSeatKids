import json

CONFIG_FILE_PATH = "etc/config.json"

class Config():
    """Config file manager class made to easily manage configuration loading/update
            Args : None
    """
    def __init__(self) -> None:
# default values for the bot
        self.home_server = ""
        self.username = ""
        self.passwd = ""
        self.room_id = ""
# private dictionary holding the values stored in the json config file
        self._configDict = dict()
# load the configuration file and set the above file
        self._loadConfiguration()


# sets all the values
    def _loadConfiguration(self) -> None:
# load the configDict if not already loaded
        try:
            if self._configDict == dict():
                with open(CONFIG_FILE_PATH, 'r') as f:
                    raw_cfg_str = f.read()
                self._configDict = json.loads(raw_cfg_str)
        except FileNotFoundError as e: 
            print(e, 'creating new file with empty args')
            self.saveConfig()
# set the values like this to ensure robusteness of the configuration
        self.home_server = self._cfgEntry('home_server', default=self.home_server)
        self.username = self._cfgEntry('username', default=self.username)
        self.passwd = self._cfgEntry('passwd', default=self.passwd)
        self.room_id = self._cfgEntry('room_id', default=self.room_id)

# make code more readable by using a simple ternary function
    def _cfgEntry(self, field : str, default=None) -> None:
        if field in self._configDict.keys():
            return self._configDict[field]
        else:
            return default

    def saveConfig(self) -> None:
        """Save to config file everytime some of the config fields change
        """
# update dictionary in order to save in the json file
        self._configDict['home_server'] = self.home_server
        self._configDict['username'] = self.username 
        self._configDict['passwd'] = self.passwd
        self._configDict['room_id'] = self.room_id
    
        with open(CONFIG_FILE_PATH, 'w+') as f:
            f.write(json.dumps(self._configDict))

if __name__ == "__main__":
    pass