from data_sources.googlesheet_interco import get_quote_df, get_invoice_df
from app import db
from app.models import User, Company, Contact, Email, Phone, FollowUp, Quote, Contractor, Service, Invoice, Amount, \
    Label_service
import pandas as pd


def get_list_quote(quote_df, db):
    li_no_company = []
    for tup in quote_df.itertuples():
        compagnie = Company.query.filter_by(company_name=tup.nom_entreprise)
        if compagnie.count() == 1:
            quote_params = {
                'ref_quote': tup.ref_devis,
                'quote_status': tup.statuts_devis,
                'created_at': tup.date_devis,
                'company': compagnie.first()
            }

            quote = Quote(**quote_params)
            db.session.add(quote)
            db.session.commit()
        else:
            li_no_company.append({
                'nb_comp':compagnie.count(),
                'nom_entreprise': tup.nom_entreprise,
                'ref_quotr': tup.ref_devis,
                #'ref_invoice': tup.ref_facture
            })
    return li_no_company


def get_list_invoice(invoice_df, db):
    li_no_company = [] #a enlever apres que ça marche
    for tup in invoice_df.itertuples():
        company = Company.query.filter_by(company_name=tup.nom_entreprise)
        if company.count() == 1:
            quote = Quote.query.filter_by(ref_quote=tup.ref_devis)

            invoice_params = {
                'ref_invoice': tup.ref_facture,
                'invoice_type': tup.type_facture,
                'company': company.first(),
                'created_at': tup.date_paiement_recu,
                'quotes': quote.all()
            }

            if quote.count() != 0:
                invoice_params['quotes'] = quote.all()
            invoice = Invoice(**invoice_params)
            db.session.add(invoice)
            db.session.commit()
        else: # ?? si pas compagnie on ajoute pas ?
            li_no_company.append({
                'nb_comp': company.count(),
                'nom_entreprise': tup.nom_entreprise,
                'ref_invoice': tup.ref_facture,
                'ref_quote': tup.ref_devis
            })
    return li_no_company #a enlever apres que ça marche


def get_list_amount(quote_df, db):
    li_no_amount = [] #a enlever apres que ça marche
    """
    col_left = ['ref_devis', 'date_devis', 'type_devis', 'nom_entreprise', 'montant_ht', 'statuts_devis', 'year']
    col_right = ['ref_devis', 'ref_facture', 'montant_ttc', 'status_invoice', 'date_paiement_recu']
    df_resultat = pd.merge(quote_df[col_left], invoice_df[col_right],
                           on=['ref_devis'], how='left')
    """
    for tup in quote_df.itertuples():
        company = Company.query.filter_by(company_name=tup.nom_entreprise)
        if company.count() == 1:
            amount_params = {
                'ht_amount': tup.montant_ht,
                'ttc_amount': tup.montant_ttc,
            }
            quote = Quote.query.filter_by(ref_quote=tup.ref_devis)
            if quote.count() != 0:
                amount_params['quote'] = quote.first()
            """
            # if tup.ref_facture is not pd.np.nan:
                # invoice = Invoice.query.filter_by(ref_invoice=tup.ref_facture)
                # if invoice.count() != 0:
                    # amount_params['invoices'] = invoice.all()
                    # amount_params['payment_status'] = tup.status_invoice
                    # amount_params['paid_at'] = tup.date_paiement_recu
            """
            amount = Amount(**amount_params)
            db.session.add(amount)
            db.session.commit()
        else: # ?? si pas compagnie on ajoute pas ?
            li_no_amount.append({
                'nb_comp': company.count(),
                'nom_entreprise': tup.nom_entreprise,
                #'ref_invoice': tup.ref_facture,
                'ref_quote': tup.ref_devis,
            })
    return li_no_amount #a enlever apres que ça marche


def get_list_service(quote_df, db):
    li_no_service = [] #a enlever apres que ça marche
    taille = len(quote_df)
    for i, tup in enumerate(quote_df.itertuples()):
        if i % 10 == 0:
            print(f"{i} / {taille} service processed")
        company = Company.query.filter_by(company_name=tup.nom_entreprise)
        if company.count() == 1:
            service_params = {
                'companies': company.all()
            }

            li_label = []
            for lab_serv in tup.type_prestation.split(','):
                label_service = Label_service.query.filter_by(label=lab_serv)
                if label_service.count() != 1:
                    label_service = Label_service(label=lab_serv)
                    li_label.append(label_service)
                else:
                    li_label.append(label_service.first())
            service_params['label_services'] = li_label

            quote = Quote.query.filter_by(ref_quote=tup.ref_devis)
            if quote.count() != 0:
                service_params['quotes'] = quote.all()

            service = Service(**service_params)

            db.session.add(service)
            db.session.commit()
        else: # ?? si pas compagnie on ajoute pas ?
            li_no_service.append({
                'nb_comp': company.count(),
                'nom_entreprise': tup.nom_entreprise,
                'ref_quote': tup.ref_devis,
            })
    return li_no_service #a enlever apres que ça marche


def populate_xls():
    quote_df = get_quote_df()
    invoice_df = get_invoice_df()
    get_list_quote(quote_df, db)
    get_list_invoice(invoice_df, db)
    get_list_amount(quote_df, db)
    get_list_service(quote_df, db)


if __name__ == '__main__':
    populate_xls()

""" 
def test_compabilite_ent():
    li_company = []
    li_no_company = []
    li_df = []

    for tup in df.itertuples():
        a = Company.query.filter_by(company_name=tup.nom_entreprise).count()
        company = Company(company_name=tup.nom_entreprise)
        # search = f'%{tup.nom_entreprise}%'
        # a = Company.query.filter(Company.company_name.ilike(search))

        di = {
            'ent_df': tup.nom_entreprise,
            'ent_db': [y.company_name for y in list(a)],
            'count_db': a.count()
        }

        # li_df.append(di)
        if a == 0:
            li_no_company.append(company)
            ref_quote = tup.ref_devis
            quote_status = tup.statuts_devis
            created_at = tup.date_devis

            # print('company exist pas en db')
        else:
            li_company.append(company)

            # print('existe en db')

"""