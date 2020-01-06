from ast import literal_eval
from sqlalchemy import func

from config import Config, config
from data_extraction.vcf_extractor import VcfExtractor
from app import db
from app.models import User, Company, Contact, Email, Phone, FollowUp, Quote, Contractor, Service, Invoice, Amount
from pprint import pprint
import pandas as pd

df_clean_cmp_name = pd.read_csv('data_cleaning/data/clean_populate_company_name.csv')
df_clean_cmp_name.comp_db = df_clean_cmp_name.comp_db.apply(literal_eval)
df_clean_cmp_name = df_clean_cmp_name.explode('comp_db')


def get_list_companies(item, dict_li):
    for n_company in item['fn']:
        n_company = n_company.lower().rstrip()

        if n_company in df_clean_cmp_name.comp_db.unique():
            n_company = df_clean_cmp_name.loc[df_clean_cmp_name.comp_db == n_company, 'comp_devis'].values[0]

        if Company.query.filter_by(company_name=n_company).count() == 0:
            company = Company(company_name=n_company)

            company.phones.extend(dict_li['phones'])
            company.emails.extend(dict_li['emails'])

            dict_li['companies'].append(company)
        else:
            company = Company.query.filter_by(company_name=n_company).first()

            company.phones.extend(dict_li['phones'])
            company.emails.extend(dict_li['emails'])

            dict_li['companies'].append(company)

    return dict_li


def get_list_contacts(item, contact_status, dict_li):
    for n_contact in item['n']:
        di_contact = {
            'last_name': n_contact['family'],
            'first_name': n_contact['given'],
            'job_position': n_contact['prefix'],
            'contact_status': contact_status,
        }
        contact = Contact(**di_contact)
        contact.phones.extend(dict_li['phones'])
        contact.emails.extend(dict_li['emails'])
        contact.companies.extend(dict_li['companies'])
        dict_li['contacts'].append(contact)

    return dict_li


def get_list_mails(item, dict_li):
    for n_email in item['email']:
        if Email.query.filter_by(email=n_email).count() != 0:
            email = Email.query.filter_by(email=n_email).first()
        else:
            email = Email(email=n_email, label='pro')
        dict_li['emails'].append(email)

    return dict_li


def get_list_tels(item, dict_li):
    for n_phone in item['tel']:
        n_phone = n_phone.replace(' ', '').replace('+33', '0')[:10]
        if n_phone in [x.phone for x in dict_li['phones']]:
            continue
        if Phone.query.filter_by(phone=n_phone).count() != 0:
            tel = Phone.query.filter_by(phone=n_phone).first()
        else:
            di_tel = {
                'phone': n_phone
            }
            tel = Phone(**di_tel)

        dict_li['phones'].append(tel)

    return dict_li


def get_list_follow_up(item, dict_li):
    for n_note in item['note']:
        di_note = {
            'note': n_note
        }
        if len(dict_li['companies']) > 0:
            di_note['company'] = dict_li['companies'][0]
        if len(dict_li['contacts']) > 0:
            di_note['contact'] = dict_li['contacts'][0]

        note = FollowUp(**di_note)
        dict_li['notes'].append(note)

    return dict_li


def vcf_to_database(list_contact, db, contact_status='Client'):
    taille = len(list_contact)
    for index, item in enumerate(list_contact):
        if index % 10 == 0:
            print(f'{index} / {taille} service processed')
            li_elems = {
                'phones':[],
                'emails':[],
                'contacts':[],
                'companies':[],
                'notes':[]
            }

        if 'tel' in item:
            li_elems = get_list_tels(item, li_elems)
        else:
            #print(f'No tels in item {index}!')

        if 'email' in item:
            li_elems = get_list_mails(item, li_elems)
        else:
            #print(f'No mails in item {index}!')

        if 'fn' in item:
            li_elems = get_list_companies(item, li_elems)
        else:
            #print(f'No company in item {index}!')

        if 'n' in item:
            li_elems = get_list_contacts(item, contact_status, li_elems)
        else:
            #print(f'No contact in item {index}!')

        if 'note' in item:
            li_elems = get_list_follow_up(item, li_elems)
        else:
            #print(f'No note in item {index}!')

        #pprint(li_elems)
        for val in ['phones', 'contacts', 'companies', 'emails', 'notes']:
            db.session.add_all(li_elems[val])
        db.session.commit()


if __name__ == '__main__':
    # Integration clients details into the database
    conf = Config(config)
    x = VcfExtractor(conf.clients)
    x.read_vcf()

    vcf_to_database(x.list_contact, db)

    # Integration prospects details into the database
    x = VcfExtractor(conf.prospects)
    x.read_vcf()

    vcf_to_database(x.list_contact, db, contact_status='Prospect')

    # Integration repérages details into the database
    x = VcfExtractor(conf.reperages)
    x.read_vcf()

    vcf_to_database(x.list_contact, db, contact_status='Reperage')

"""
[{'email': ['bbobet@adexsi.com'],
 'fn': ['ADEXSI'],
 'n': [{'additional': '',
        'family': 'BOBET',
        'given': 'Baptiste',
        'prefix': 'resp com mark',
        'suffix': ''}],
 'note': ['prospect Linkedin x2\n'
          'Assemble pièces pour sécurité incendie et énergie\n'
          '\n'
          'Tel 16/06/17 vient d’arriver A mes coordonnées par Rodolphe GODIN '
          'Intéressé par 3D et animations Prend ses marques Sera peut être sur '
          'Batimat en visiteur !? Le rappeler Envoi lien via invit linkedin\n'
          'Tel 17/10/17 dde scanner 3D pour plans techniques SAV '
          'http://www.coolea.fr/produits/wetbox/\n'
          '24/10/17 devis vues éclatées bloc en 3D \n'
          '27/10/17 rdv avec chef produit tel 31/10/17 opte pour solution '
          'simple dans un premier temps Te consultera si les clients utilisent '
          'cet outil et si besoin de qualité \n'
          'AVP17\n'
          'tel 16/03/18 a choisi solution en 2D proposée par Coolea Vont '
          'tester et te rappelle si besoin de + de qualité en 3D\n'
          'tel 13/12/18 Coolea a été racheté mais ne sait pas si besoin de 3D '
          'te rappelle au cas où…\n'
          'Reportages photo en interne pour ref clients '],
 'org': [['ADEXSI']],
 'photo': [],`
 'tel': ['02 47 55 36 37', '0786355218'],
 'uid': ['166ff3c9-14bb-4b3a-876e-0f935f1a9e66'],
 'url': ['http://www.adexsi.com'],
 'version': ['3.0'],
 'x-ablabel': ['_$!<HomePage>!$_'],
 'x-abshowas': ['COMPANY'],
 'x-abuid': ['166FF3C9-14BB-4B3A-876E-0F935F1A9E66:ABPerson']}]
"""