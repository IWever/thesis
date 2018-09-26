from src.MTexperiment.general import addDynamicObject
from src.ship import Ship

def createShips():
    # Variables
    deadweight2displacement = 1.25

    # Define ships
    Tanker = Ship(name="Gulf Valour",
                  MMSI=311072100,
                  LBP=249,
                  width=48,
                  depth=13.2,
                  displacement=114900 * deadweight2displacement,
                  deadweight=114900,
                  nominalSpeed_kn=10.5,
                  maxSpeed_kn=20,
                  color='green')

    Tug = Ship(name="DAMEN ASD2411",
               MMSI=710030460,
               LBP=24.47,
               width=11.33,
               depth=5.61,
               displacement=492,
               deadweight=150,
               nominalSpeed_kn=13,
               maxSpeed_kn=14,
               color='black')

    EmmaMaersk = Ship(name="Emma Maersk",
                      MMSI=220417000,
                      LBP=397.71,
                      width=56.41,
                      depth=12.6,
                      displacement=156907 * deadweight2displacement,
                      deadweight=156907,
                      nominalSpeed_kn=18,
                      maxSpeed_kn=27,
                      color='dodgerblue')

    Astrorunner = Ship(name="Astrorunner",
                       MMSI=210248000,
                       LBP=141.58,
                       width=20.6,
                       depth=6.5,
                       displacement=9543 * deadweight2displacement,
                       deadweight=9543,
                       nominalSpeed_kn=15.5,
                       maxSpeed_kn=20,
                       color='orange')

    CF7200 = Ship(name="DAMEN Combi Freighter 7200",
                  MMSI=246232000,
                  LBP=118.14,
                  width=15.9,
                  depth=6.4,
                  displacement=7210 * deadweight2displacement,
                  deadweight=7210,
                  nominalSpeed_kn=10,
                  maxSpeed_kn=14,
                  color='peru')

    Anglia = Ship(name="Anglia Seaways",
                  MMSI=219292000,
                  LBP=142.4,
                  width=23,
                  depth=5,
                  displacement=4650 * deadweight2displacement,
                  deadweight=4650,
                  nominalSpeed_kn=16.8,
                  maxSpeed_kn=18,
                  color='deepskyblue')

    # Initialize ships
    addDynamicObject(Tanker, [0, 0], 0)
    addDynamicObject(Tug, [0, 0], 0)
    addDynamicObject(EmmaMaersk, [0, 0], 0)
    addDynamicObject(Astrorunner, [0, 0], 0)
    addDynamicObject(CF7200, [0, 0], 0)
    addDynamicObject(Anglia, [0, 0], 0)

    # Store ships in list
    shipList = [Tanker, Tug, EmmaMaersk, Astrorunner, CF7200, Anglia]

    return shipList, Tanker, Tug, EmmaMaersk, Astrorunner, CF7200, Anglia