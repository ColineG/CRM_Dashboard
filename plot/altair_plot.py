import altair as alt
from data_sources.googlesheet_interco import get_quote_df
from data_exploitation.generate_csv_from_prod import create_df_quote_amount, create_df_quote_company, \
    create_df_service_amount


def html_contrat_signed_vs_refused_count():
    quote_df = create_df_quote_amount()
    quote_df['year'] = quote_df.created_at.dt.year

    plot = alt.Chart(quote_df, width=100).mark_bar().encode(
        alt.X('quote_status:O', title='',),
        alt.Y('count(ref_quote):Q', title='Number of contract'),
        alt.Column('year:N', title='Number of contract signed vs refused per year'),
        alt.Color('quote_status:N', title='Quote status')
    )
    plot.save('app/templates/plot/count_signed_vs_refused.html')
    return plot


def html_contrat_signed_vs_refused_amount():
    quote_df = create_df_quote_amount()
    quote_df['year'] = quote_df.created_at.dt.year
    quote_df.columns = [col + '_' for col in quote_df]

    plot = alt.Chart(quote_df, width=100).mark_bar().encode(
        alt.X('quote_status_:O', title='', axis=alt.Axis(titleFont="Helvetica Neue")),
        alt.Y('sum(ht_amount_):Q', title='Sum of montant HT', axis=alt.Axis(titleFont="Helvetica Neue")),
        alt.Column('year_:N', title='Amount of contract signed vs refused per year'),
        alt.Color('quote_status_:N', title='Quote status')
    )
    plot.save('app/templates/plot/amount_signed_vs_refused.html')
    return plot


def html_ca_entreprise():
    df = create_df_quote_company()
    df_signed = df[df.quote_status == 'signed']
    df_signed_company = df_signed.groupby('company_name').agg({'ht_amount': sum, 'quote_status': 'count'}).reset_index()
    df_signed_company.company_name = df_signed_company.company_name.str.title()
    plot = alt.Chart(df_signed_company, title="Part du chiffre d'affaire par entreprise").transform_joinaggregate(
        TotalAmount='sum(ht_amount)',
    ).transform_calculate(
        PercentOfTotal="datum.ht_amount / datum.TotalAmount"
    ).mark_bar().encode(
        x=alt.X('PercentOfTotal:Q', axis=alt.Axis(format='.0%'), title='Pourcentage du CA'),
        y=alt.Y('company_name:N', title='Nom entreprises',
                sort=alt.EncodingSortField(field="PercentOfTotal", order='descending')),
        tooltip=[alt.Tooltip('sum(ht_amount)', title='Sum Montant HT€'),
                 alt.Tooltip('quote_status', title='Nbr contrat')]
    )
    plot.save('app/templates/plot/repartition_ca_entreprise.html')
    return plot


def html_demande_type_presta():
    df = create_df_service_amount()
    df.loc[df.ttc_amount.isnull(), 'payment_status'] = 'Refused'
    df.loc[~df.ttc_amount.isnull(), 'payment_status'] = 'Accepted'
    df.label_services = df.label_services.str.title()

    show_comp = False
    plot = alt.Chart(df, title='Nombre de vente/refus par prestation').mark_bar(
    ).encode(
        y=alt.Y('label_services:N', title='Types prestations', sort=alt.EncodingSortField(field="ht_amount", op="count", order='descending')),
        x=alt.X('count()', title='Nombre de ventes'),
        color= alt.Color('compagnie' if show_comp else 'payment_status', title='Status paiement'),
        tooltip=[alt.Tooltip('distinct(compagnie)', title='Nbr entreprise'),
                alt.Tooltip('count()', title='Nbr devis')],
    )
    plot.save('app/templates/plot/analyse_vente_type_presta.html')
    return plot


def concat(plot_1, plot_2, dash_name):
    plot = alt.vconcat(plot_1, plot_2, spacing=60).configure(
        legend=alt.LegendConfig(labelFontSize=16, titleFontSize=16, symbolSize=100, labelFont='Lato'),
        axis=alt.AxisConfig(labelFontSize=16, tickSize=16, labels=True, titleFontSize=16),
        header=alt.HeaderConfig(titleFontSize=20, labelFontSize=20)
    ).configure_title(fontSize=24)
    plot.save(f"app/templates/plot/{dash_name}.html")


def html_detail_company():
    df = create_df_service_amount()
    df.loc[df.ttc_amount.isnull(), 'payment_status'] = 'Refused'
    df.loc[~df.ttc_amount.isnull(), 'payment_status'] = 'Accepted'
    df.label_services = df.label_services.str.title()
    df.compagnie = df.compagnie.str.title()

    chart = alt.Chart(df).mark_bar(
    ).encode(
        y=alt.Y('label_services', title='Types prestations'),
        x=alt.X('count(label_services)', title='Nombre de contrats'),
        color=alt.Color('payment_status', title='Status paiement'),
        tooltip=[
            alt.Tooltip('label_services', title='Prestation'),
            alt.Tooltip('max(ht_amount)', title='Max amount'),
            alt.Tooltip('min(ht_amount)', title='Min amount'),
            alt.Tooltip('count()', title='Devis count')
        ]
    ).facet(
        facet=alt.Facet('compagnie:N', title='Compagnies'),
        columns=2,
    )
    chart.save("app/templates/plot/detail_company.html")


def html_marge_montant_ht():
    quote_df = get_quote_df()
    df_signed = quote_df[quote_df.statuts_devis == 'signed']

    # Pre-processing/wrangling de la df pour faciliter le plot
    tmp1 = df_signed[['nom_entreprise', 'montant_ht']].copy()
    tmp1['label_montant'] = 'montant_ht'
    tmp1 = tmp1.rename(columns={'montant_ht': 'montant'})

    tmp2 = df_signed[['nom_entreprise', 'Marge ']].copy()
    tmp2['label_montant'] = 'Marge'
    tmp2 = tmp2.rename(columns={'Marge ': 'montant'})

    df_signed = tmp1.append(tmp2)

    plot = alt.Chart(df_signed, title='Part de marge en fonction du montant global des ventes').mark_bar(
    ).encode(
        y=alt.Y('nom_entreprise:N', title='Nom entreprise',
                sort=alt.EncodingSortField(field="montant_ht", op="count", order='descending')),
        x=alt.X('sum(montant):Q', title='Montant global des ventes', stack=False),
        color=alt.Color('label_montant'),
        tooltip=[alt.Tooltip('sum(montant)', title='Global'),
                 alt.Tooltip('label_montant', title='Montant'),
                 alt.Tooltip('count()', title='Nbr devis')],
    )
    plot.save("app/templates/plot/marge_amount_ht_analyse.html")

    return plot
