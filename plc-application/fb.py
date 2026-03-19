from wagoplc.fb import FB

class Torsteuerung(FB):

    def __init__(self):
        self.tor_auf = False
        self.tor_zu = True
        self.status = 0
    
    def __call__(self, xS1: bool, xS2: bool, xEndlageS1: bool, xEndlageS2: bool):
        match self.status:
            case 0: # Tor ist geschlossen
                if xS1:
                    self.tor_zu = False
                    self.status = 1
            case 1: # Tor oeffnet
                if not xEndlageS1:
                    print("Tor ist offen!")
                    self.tor_auf = True
                    self.status = 2
            case 2: # Tor ist offen
                if xS2:
                    self.tor_auf = False
                    self.status = 3
            case 3: # Tor schliesst
                if not xEndlageS2:
                    print("Tor ist geschloßen!")
                    self.tor_zu = True
                    self.status = 0