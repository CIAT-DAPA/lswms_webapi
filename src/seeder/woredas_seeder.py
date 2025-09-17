import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

#test
from mongoengine import connect
from conf import config
from ormWP import Woreda

# Connect to the database
connect(host=config['CONNECTION_DB'])

# Function to seed Woreda data
def seed_woredas():
    """Seeds the Woreda collection."""
    data = [
  {
    "name": "Dubti",
    "ext_id": "ET020101"
  },
  {
    "name": "Elidar",
    "ext_id": "ET020102"
  },
  {
    "name": "Asayita",
    "ext_id": "ET020103"
  },
  {
    "name": "Afambo",
    "ext_id": "ET020104"
  },
  {
    "name": "Mile",
    "ext_id": "ET020105"
  },
  {
    "name": "Chifra",
    "ext_id": "ET020106"
  },
  {
    "name": "Dubti town",
    "ext_id": "ET020107"
  },
  {
    "name": "Kori",
    "ext_id": "ET020108"
  },
  {
    "name": "Adar",
    "ext_id": "ET020109"
  },
  {
    "name": "Gerani",
    "ext_id": "ET020110"
  },
  {
    "name": "Asayita town",
    "ext_id": "ET020111"
  },
  {
    "name": "Samera Logiya town",
    "ext_id": "ET020198"
  },
  {
    "name": "Erebti",
    "ext_id": "ET020201"
  },
  {
    "name": "Kunneba",
    "ext_id": "ET020202"
  },
  {
    "name": "Abaala",
    "ext_id": "ET020203"
  },
  {
    "name": "Megale",
    "ext_id": "ET020204"
  },
  {
    "name": "Berahile",
    "ext_id": "ET020205"
  },
  {
    "name": "Dalol",
    "ext_id": "ET020206"
  },
  {
    "name": "Afdera",
    "ext_id": "ET020207"
  },
  {
    "name": "Bidu",
    "ext_id": "ET020208"
  },
  {
    "name": "Abaala town",
    "ext_id": "ET020209"
  },
  {
    "name": "Amibara",
    "ext_id": "ET020301"
  },
  {
    "name": "Awash",
    "ext_id": "ET020302"
  },
  {
    "name": "Gewane",
    "ext_id": "ET020303"
  },
  {
    "name": "Dulecha",
    "ext_id": "ET020304"
  },
  {
    "name": "Gelalu",
    "ext_id": "ET020305"
  },
  {
    "name": "Arguba",
    "ext_id": "ET020306"
  },
  {
    "name": "Hanruka",
    "ext_id": "ET020307"
  },
  {
    "name": "Awash town",
    "ext_id": "ET020396"
  },
  {
    "name": "Awra (AF)",
    "ext_id": "ET020401"
  },
  {
    "name": "Euwa",
    "ext_id": "ET020402"
  },
  {
    "name": "Teru",
    "ext_id": "ET020403"
  },
  {
    "name": "Yalo",
    "ext_id": "ET020404"
  },
  {
    "name": "Gulina",
    "ext_id": "ET020405"
  },
  {
    "name": "Telalek",
    "ext_id": "ET020501"
  },
  {
    "name": "Samurobi",
    "ext_id": "ET020502"
  },
  {
    "name": "Dawe",
    "ext_id": "ET020503"
  },
  {
    "name": "Dalefage",
    "ext_id": "ET020504"
  },
  {
    "name": "Hadelela",
    "ext_id": "ET020505"
  },
  {
    "name": "Yabelo",
    "ext_id": "ET041207"
  },
  {
    "name": "Arero",
    "ext_id": "ET041208"
  },
  {
    "name": "Moyale (OR)",
    "ext_id": "ET041210"
  },
  {
    "name": "Dire",
    "ext_id": "ET041211"
  },
  {
    "name": "Teltale",
    "ext_id": "ET041212"
  },
  {
    "name": "Miyo",
    "ext_id": "ET041216"
  },
  {
    "name": "Dilo",
    "ext_id": "ET041219"
  },
  {
    "name": "Dhas",
    "ext_id": "ET041220"
  },
  {
    "name": "Gomole",
    "ext_id": "ET041223"
  },
  {
    "name": "Guchi",
    "ext_id": "ET041290"
  },
  {
    "name": "Dubluk",
    "ext_id": "ET041291"
  },
  {
    "name": "Elwaya",
    "ext_id": "ET041295"
  },
  {
    "name": "Yabelo town",
    "ext_id": "ET041296"
  },
  {
    "name": "Wachile",
    "ext_id": "ET041298"
  },
  {
    "name": "Ayisha",
    "ext_id": "ET050101"
  },
  {
    "name": "Dembel",
    "ext_id": "ET050102"
  },
  {
    "name": "Shinile",
    "ext_id": "ET050103"
  },
  {
    "name": "Erer (SM)",
    "ext_id": "ET050104"
  },
  {
    "name": "Afdem",
    "ext_id": "ET050105"
  },
  {
    "name": "Hadhagala",
    "ext_id": "ET050106"
  },
  {
    "name": "Miesso",
    "ext_id": "ET050107"
  },
  {
    "name": "Gota-Biki",
    "ext_id": "ET050198"
  },
  {
    "name": "Gablalu",
    "ext_id": "ET050199"
  },
  {
    "name": "Gursum (SM)",
    "ext_id": "ET050202"
  },
  {
    "name": "Babile (SM)",
    "ext_id": "ET050203"
  },
  {
    "name": "Shabeeley",
    "ext_id": "ET050204"
  },
  {
    "name": "Aw-Bare",
    "ext_id": "ET050205"
  },
  {
    "name": "Kebribeyah",
    "ext_id": "ET050206"
  },
  {
    "name": "Harshin",
    "ext_id": "ET050207"
  },
  {
    "name": "Tuliguled",
    "ext_id": "ET050283"
  },
  {
    "name": "Goljano",
    "ext_id": "ET050290"
  },
  {
    "name": "Jigjiga town",
    "ext_id": "ET050293"
  },
  {
    "name": "Wajale town",
    "ext_id": "ET050295"
  },
  {
    "name": "Kebribayah town",
    "ext_id": "ET050296"
  },
  {
    "name": "Koran /Mulla",
    "ext_id": "ET050297"
  },
  {
    "name": "Haroreys",
    "ext_id": "ET050298"
  },
  {
    "name": "Harawo",
    "ext_id": "ET050299"
  },
  {
    "name": "Degehamedo",
    "ext_id": "ET050301"
  },
  {
    "name": "Degehabur",
    "ext_id": "ET050302"
  },
  {
    "name": "Aware",
    "ext_id": "ET050303"
  },
  {
    "name": "Gashamo",
    "ext_id": "ET050304"
  },
  {
    "name": "Gunagado",
    "ext_id": "ET050305"
  },
  {
    "name": "Bilcil-Bur",
    "ext_id": "ET050306"
  },
  {
    "name": "Degahabur town",
    "ext_id": "ET050307"
  },
  {
    "name": "Yocale",
    "ext_id": "ET050382"
  },
  {
    "name": "Daror",
    "ext_id": "ET050392"
  },
  {
    "name": "Burqod",
    "ext_id": "ET050394"
  },
  {
    "name": "Ararso",
    "ext_id": "ET050395"
  },
  {
    "name": "Dig",
    "ext_id": "ET050399"
  },
  {
    "name": "Fik",
    "ext_id": "ET050402"
  },
  {
    "name": "Salahad",
    "ext_id": "ET050403"
  },
  {
    "name": "Hamero",
    "ext_id": "ET050404"
  },
  {
    "name": "Lagahida",
    "ext_id": "ET050407"
  },
  {
    "name": "Meyumuluka",
    "ext_id": "ET050408"
  },
  {
    "name": "Qubi",
    "ext_id": "ET050497"
  },
  {
    "name": "Yahob",
    "ext_id": "ET050498"
  },
  {
    "name": "Wangey",
    "ext_id": "ET050499"
  },
  {
    "name": "Shaygosh",
    "ext_id": "ET050501"
  },
  {
    "name": "Kebridehar",
    "ext_id": "ET050502"
  },
  {
    "name": "Shilabo",
    "ext_id": "ET050503"
  },
  {
    "name": "Debeweyin",
    "ext_id": "ET050504"
  },
  {
    "name": "Marsin",
    "ext_id": "ET050586"
  },
  {
    "name": "Kebridehar town",
    "ext_id": "ET050592"
  },
  {
    "name": "Goglo",
    "ext_id": "ET050595"
  },
  {
    "name": "Lasdhankayre",
    "ext_id": "ET050596"
  },
  {
    "name": "Higloley",
    "ext_id": "ET050597"
  },
  {
    "name": "El-Ogaden",
    "ext_id": "ET050598"
  },
  {
    "name": "Bodaley",
    "ext_id": "ET050599"
  },
  {
    "name": "East Imi",
    "ext_id": "ET050601"
  },
  {
    "name": "Adadle",
    "ext_id": "ET050602"
  },
  {
    "name": "Danan",
    "ext_id": "ET050603"
  },
  {
    "name": "Gode",
    "ext_id": "ET050604"
  },
  {
    "name": "Kelafo",
    "ext_id": "ET050605"
  },
  {
    "name": "Mustahil",
    "ext_id": "ET050606"
  },
  {
    "name": "Ferfer",
    "ext_id": "ET050607"
  },
  {
    "name": "Berocano",
    "ext_id": "ET050608"
  },
  {
    "name": "Godey town",
    "ext_id": "ET050696"
  },
  {
    "name": "Elale",
    "ext_id": "ET050698"
  },
  {
    "name": "Aba-Korow",
    "ext_id": "ET050699"
  },
  {
    "name": "Danod",
    "ext_id": "ET050701"
  },
  {
    "name": "Bokh",
    "ext_id": "ET050702"
  },
  {
    "name": "Galadi",
    "ext_id": "ET050703"
  },
  {
    "name": "Warder",
    "ext_id": "ET050704"
  },
  {
    "name": "Daratole",
    "ext_id": "ET050788"
  },
  {
    "name": "Lehel-Yucub",
    "ext_id": "ET050798"
  },
  {
    "name": "Galhamur",
    "ext_id": "ET050799"
  },
  {
    "name": "Charati",
    "ext_id": "ET050802"
  },
  {
    "name": "Elkare /Serer",
    "ext_id": "ET050804"
  },
  {
    "name": "West Imi",
    "ext_id": "ET050805"
  },
  {
    "name": "Hargele",
    "ext_id": "ET050806"
  },
  {
    "name": "Barey",
    "ext_id": "ET050807"
  },
  {
    "name": "Dolobay",
    "ext_id": "ET050808"
  },
  {
    "name": "Raso",
    "ext_id": "ET050809"
  },
  {
    "name": "Kohle /Qoxle",
    "ext_id": "ET050898"
  },
  {
    "name": "God-God",
    "ext_id": "ET050899"
  },
  {
    "name": "Filtu",
    "ext_id": "ET050901"
  },
  {
    "name": "Dolo Ado",
    "ext_id": "ET050902"
  },
  {
    "name": "Goro Baqaqsa",
    "ext_id": "ET050903"
  },
  {
    "name": "Guradamole",
    "ext_id": "ET050904"
  },
  {
    "name": "Deka Suftu",
    "ext_id": "ET050991"
  },
  {
    "name": "Bokolmayo",
    "ext_id": "ET050999"
  },
  {
    "name": "Ayun",
    "ext_id": "ET051001"
  },
  {
    "name": "Elwayne",
    "ext_id": "ET051002"
  },
  {
    "name": "Garbo",
    "ext_id": "ET051003"
  },
  {
    "name": "Sagag",
    "ext_id": "ET051005"
  },
  {
    "name": "Dihun",
    "ext_id": "ET051006"
  },
  {
    "name": "Horshagah",
    "ext_id": "ET051095"
  },
  {
    "name": "Hararey",
    "ext_id": "ET051096"
  },
  {
    "name": "Moyale (SM)",
    "ext_id": "ET051103"
  },
  {
    "name": "Hudet",
    "ext_id": "ET051104"
  },
  {
    "name": "Mubarek",
    "ext_id": "ET051187"
  },
  {
    "name": "Qada Duma",
    "ext_id": "ET051198"
  }
]

    for woreda_data in data:
        try:
            # Check if a woreda with the same ext_id exists
            existing_woreda = Woreda.objects(ext_id=woreda_data['ext_id']).first()

            if existing_woreda:
                # Update the existing record
                for key, value in woreda_data.items():
                    setattr(existing_woreda, key, value)
                existing_woreda.save()
                
            else:
                # Save a new record
                new_woreda = Woreda(**woreda_data)
                new_woreda.save()
                

        except Exception as e:
            print(f"Error processing woreda {woreda_data['name']}: {e}")

if __name__ == "__main__":
    seed_woredas()
