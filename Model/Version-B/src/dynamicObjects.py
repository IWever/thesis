from src.ship import Ship


""" Containing functions to create dynamic objects and ship definitions """


# Definition methods
def addShip(shipList, key, name, MMSI, LBP, width, depth, displacement, deadweight, nominalSpeed_kn):
    shipList[key] = Ship(name, MMSI, LBP, width, depth, displacement, deadweight, nominalSpeed_kn)


def removeShip(shipList, key):
    del shipList[key]


# initialize constants
shipList = {}

# Conversion constants
deadweight2displacement = 1.25

# Define and create ships
Tanker = Ship(name="Gulf Valour",
              MMSI=311072100,
              LBP=249,
              width=48,
              depth=13.2,
              displacement=114900 * deadweight2displacement,
              deadweight=114900,
              nominalSpeed_kn=10.5,
              color='green')

Bulk = Ship(name="Amelie",
            MMSI=636092737,
            LBP=180,
            width=30,
            depth=10.1,
            displacement=34650 * deadweight2displacement,
            deadweight=34650,
            nominalSpeed_kn=10.5,
            color='red')

Tug = Ship(name="DAMEN ASD2411",
           MMSI=710030460,
           LBP=24.47,
           width=11.33,
           depth=5.61,
           displacement=492,
           deadweight=150,
           nominalSpeed_kn=13,
           color='black')

Bibby = Ship(name="Bibby Wavemaster 1",
             MMSI=232008874,
             LBP=89.65,
             width=20,
             depth=6.1,
             displacement=5956,
             deadweight=2400,
             nominalSpeed_kn=12,
             color='blue')

EmmaMaersk = Ship(name="Emma Maersk",
                  MMSI=220417000,
                  LBP=397.71,
                  width=56.41,
                  depth=12.6,
                  displacement=156907 * deadweight2displacement,
                  deadweight=156907,
                  nominalSpeed_kn=18,
                  color='dodgerblue')

Astrorunner = Ship(name="Astrorunner",
                  MMSI=210248000,
                  LBP=141.58,
                  width=20.6,
                  depth=6.5,
                  displacement=9543 * deadweight2displacement,
                  deadweight=9543,
                  nominalSpeed_kn=15.5,
                  color='orange')

Anglia = Ship(name="Anglia Seaways",
                  MMSI=219292000,
                  LBP=142.4,
                  width=23,
                  depth=5,
                  displacement=4650 * deadweight2displacement,
                  deadweight=4650,
                  nominalSpeed_kn=16.8,
                  color='deepskyblue')

# Add ships to dictionary
shipList["Tanker"] = Tanker
shipList["Bulk"] = Bulk
shipList["Tug"] = Tug
shipList["Bibby"] = Bibby
shipList["EmmaMaersk"] = EmmaMaersk
shipList["Astrorunner"] = Astrorunner
shipList["Anglia"] = Anglia