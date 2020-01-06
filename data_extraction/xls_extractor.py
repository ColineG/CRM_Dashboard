from config import Config, config
from app import db
from app.models import Company
import pandas as pd
import vobject


class XlsExtractor:
    def __init__(self):
        self.param = Config(config)
        self.recap_DF = None

    def read_xls(self):
        self.recap_DF = pd.read_excel(self.param.)

        return self.recap_DF.limit()

    def rename_df_col(self):
        self.recap_DF.columns = ['date_devis_emis', 'ref_quote', 'company_name_prestation', 'montant_ht',
                                 'montant_ttc', 'ref_invoice', 'date_payement']
        return self.recap_DF






conf = Config(config)

"""
for excel_keys in conf.excel.keys():
    excel_info = conf.excel[excel_keys]
    print(f"{excel_info['path']} {excel_info['sheetname']}")
    recap_DF = pd.read_excel(excel_info['path'], sheet_name=excel_info['sheetname'])

li_company_name = []
for value in db.session.query(Company.company_name).distinct().all():
     li_company_name.append(value.company_name)
     print(li_company_name)

"""

for tup in df.itertuples():
    di_quote = {
        'ref_quote': tup.ref_devis,
        'quote_status': tup.statuts_devis,
        'created_at': tup.date_devis,
        '?': tup.nom_entreprise
    }
    di_invoice = {
        'ref_invoice': tup.ref_facture,
        'invoice_type': tup.type_facture
    }
    di_service = {
        'services': tup.type_prestation,
        'amount_id': tup.
    }
    m1 = Model1(**di_model_1)
    m2 = Model2(**di_model_2)
    m1.une_colonne_jointure_si_relation.append_ou_extend_si_plusieurs([m_n] OU m2)
    db.session.add_all(tes_m1)
    db.session.commit()