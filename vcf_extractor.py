from config import Config, config
import vobject


class VcfExtractor:
    """
        Création d'une class qui permette l'extraction des metadata du fichier .vcf pour pouvoir exploiter la donnée.

    """
    def __init__(self, path_vcf):
        self.path_vcf = path_vcf
        self.list_contact = None

    def read_vcf(self):
        with open(self.path_vcf, 'r') as f:
            a = f.readlines()
        vcf_contacts = vobject.readComponents(''.join(a))

        li = []
        # TODO identifier label pour les numéros (31 numéro non pas un nbr de label équivalent contre 17)
        """
        li = []
        for i, client in enumerate(x.df):
            if 'tel' in client and 'x-ablabel' in client:
                if len(client['tel']) == len(client['x-ablabel']):
                    li.append(True)
                else:
                    li.append(False)
        """
        for i, contact in enumerate(vcf_contacts):
            di = {}
            for key in contact.contents.keys():
                di[key] = []
                # drop photo du json
                if key == 'photo':
                    continue
                for k, value in enumerate(contact.contents[key]):
                    if type(value.__dict__['value']) in [list, str, bytes]:
                        di[key].append(value.__dict__['value'])
                    else:
                        di[key].append(value.__dict__['value'].__dict__)
            li.append(di)
        self.list_contact = li


conf = Config(config)
x = VcfExtractor(conf.clients)

"""
To save x.list_contact as a json file:
---
import json
with open("list_contact.json", "w") as f:
    f.write(json.dumps(json.loads(output), indent=4, sort_keys=True))

"""