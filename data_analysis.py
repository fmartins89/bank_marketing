# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 23:07:02 2018

@author: Felipe A Martins
"""

import pandas as pd
import matplotlib.pyplot as plt

def age_category (data):
    """Create a new dataframe column with the categorized ages"""
    data["age_category"] = "0-unknown"
    data.loc[(data["age"] <= 30) & (data["age"] >= 18),"age_category"] = "1-youngling_18-30"
    data.loc[(data["age"] <= 40) & (data["age"] > 30),"age_category"] = "2-adult_31-40"
    data.loc[(data["age"] <= 50) & (data["age"] > 40),"age_category"] = "3-middle_41-50"
    data.loc[(data["age"] > 50),"age_category"] = "4-elderly_51+"
    return data

def bal_category (data):
    """Create a new dataframe column with the categorized balances"""
    data["bal_category"] = "0-unknown"
    data.loc[(data["balance"] < 0),"bal_category"] = "1-negative"
    data.loc[(data["balance"] >= 0) & (data["balance"] < 100),"bal_category"] = "2-verylow_0-99"
    data.loc[(data["balance"] >= 100) & (data["balance"] < 400),"bal_category"] = "3-low_100-399"
    data.loc[(data["balance"] >= 400) & (data["balance"] < 1000),"bal_category"] = "4-medium_400-999"
    data.loc[(data["balance"] >= 1000) & (data["balance"] < 3000),"bal_category"] = "5-high_1000-2999"
    data.loc[(data["balance"] >= 3000),"bal_category"] = "6-veryhigh_3000+"

    return data

def prev_category (data):
    """Create a new dataframe column with the categorized previous"""
    data.loc[(data["previous"] <=7),"prev_category"] = "0"+data['previous'].astype(str)
    data.loc[(data["previous"] >= 8) & (data["previous"] <= 10),"prev_category"] = "08-10"
    data.loc[(data["previous"] >= 11),"prev_category"] = "11+"

    data["prev_category"] = data["prev_category"].astype(str)
    return data

def camp_category (data):
    """Create a new dataframe column with the categorized campaigns"""
    data.loc[(data["campaign"] <=6),"camp_category"] = "0"+data['campaign'].astype(str)
    data.loc[(data["campaign"] == 7) | (data["campaign"] == 8),"camp_category"] ="07-08"
    data.loc[(data["campaign"] >= 9),"camp_category"] = "09+"

    data["camp_category"] = data["camp_category"].astype(str)
    return data

def check_outliers (data):
    """Calculate and Print the beggining values of High and Low outliers"""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    print("IQR:")
    print(IQR)

    print("Outliers Baixos:")
    print (Q1 - 1.5 * IQR)

    print("Outliers Altos:")
    print (Q3 + 1.5 * IQR)

    return

def show_hist (data, bins = 10):
    """Plot histograms"""
    plt.hist((data),bins=bins)
    plt.show()

def show_bar (data, title=""):
    """Plot bar chart"""
    plt.xticks(rotation='vertical')
    plt.bar(data.keys(),data)
    plt.title(title)
    plt.show()

def show_box (data, fmt = 'g', title=""):
    """Plot boxplot"""
    plt.boxplot(data,0,fmt)
    plt.title(title)
    plt.show()

#1. Qual profissão tem mais tendência a fazer um empréstimo? De qual tipo?
def ex1 (dataset):

    df_loan = dataset.query('loan == "yes" | housing == "yes"')
    df_personal = dataset.query('loan == "yes"')
    df_housing = dataset.query('housing == "yes"')

    personal_jobs = df_personal.job.value_counts()
    housing_jobs = df_housing.job.value_counts()
    loan_jobs = df_loan .job.value_counts()
    total_jobs = dataset.job.value_counts()

    percent_loan = loan_jobs * 100 / total_jobs
    percent_hous = housing_jobs * 100 / total_jobs
    percent_personal = personal_jobs * 100 / total_jobs

    loans_df = pd.DataFrame({"Loans": loan_jobs, "Total": total_jobs, "Percent": percent_loan, "Personal_Loans": personal_jobs, "Housings": housing_jobs, "Percent_Housing": percent_hous, "Percent_Personal": percent_personal }).sort_values(by=["Percent"])

    gen_loans_df = pd.DataFrame({"Loans": personal_jobs, "Total": total_jobs, "Percent": percent_loan }).sort_values(by=["Percent"])

    pers_loans_df = pd.DataFrame({"Total": total_jobs, "Percent": percent_personal, "Persoanl_Loans": personal_jobs }).sort_values(by=["Percent"])

    hous_loans_df = pd.DataFrame({"Total": total_jobs, "Housing_Loans": housing_jobs, "Percent": percent_hous}).sort_values(by=["Percent"])

    return loans_df, gen_loans_df, pers_loans_df, hous_loans_df


#2. Fazendo uma relação entre número de contatos e sucesso da campanha quais são os pontos relevantes a serem observados?
def ex2_previous(dataset):
    '''
    retorna a porcentagem de sucesso da campanha anterior por numero de contatos
    '''
    dataset_prev = dataset.query('previous > 0')

    df_psuccess = dataset_prev.query('poutcome == "success"')
    success_previous = df_psuccess.prev_category.value_counts()
    total_previous = dataset_prev.prev_category.value_counts()

    percent_previous = success_previous * 100 / total_previous
    return percent_previous.fillna(0).sort_index()


#3. Baseando-se nos resultados de adesão desta campanha qual o número médio e o máximo de ligações que você indica para otimizar a adesão?
def ex2_3_current_percentage (dataset):
    '''
    retorna a porcentagem de sucesso da campanha atual por numero de contatos
    '''

    df_success = dataset.query('y == "yes"')

    success_campaing = df_success.camp_category.value_counts()
    total_campaing = dataset.camp_category.value_counts()

    percent_success = success_campaing * 100 / total_campaing
    return percent_success.fillna(0)

#4. O resultado da campanha anterior tem relevância na campanha atual?
def ex4(dataset):
    dataset_no_prev = dataset.query('previous <= 0')
    dataset_prev = dataset.query('previous > 0')
    df_pfail = dataset_prev.query('poutcome == "failure"')
    df_pother = dataset_prev.query('poutcome == "other"')
    df_psuccess = dataset_prev.query('poutcome == "success"')

    yes_psucc = 100 * df_psuccess.y.value_counts().yes / df_psuccess.y.value_counts().sum()
    yes_pfail = 100 * df_pfail.y.value_counts().yes / df_pfail.y.value_counts().sum()
    yes_pother = 100 * df_pother.y.value_counts().yes / df_pother.y.value_counts().sum()
    yes_noprev = 100 * dataset_no_prev.y.value_counts().yes / dataset_no_prev.y.value_counts().sum()

    return pd.Series({"Success": yes_psucc, "Fail":yes_pfail, "Other": yes_pother, "No_Prev":yes_noprev
                         }).sort_values()
#5. Qual o fator determinante para que o banco exija um seguro de crédito?
def ex5(dataset):

    df_default = dataset.query('default == "yes" ')

    def_age = df_default.age.value_counts()
    def_age_category = df_default.age_category.value_counts()
    def_bal_category = df_default.bal_category.value_counts()
    def_marital = df_default.marital.value_counts()
    def_education = df_default.education.value_counts()
    def_balance = df_default.balance.value_counts()
    def_jobs = df_default.job.value_counts()
    def_loan = df_default.loan.value_counts()
    def_housing = df_default.housing.value_counts()

    total_age = dataset.age.value_counts()
    total_age_category = dataset.age_category.value_counts()
    total_bal_category = dataset.bal_category.value_counts()
    total_marital = dataset.marital.value_counts()
    total_education = dataset.education.value_counts()
    total_balance = dataset.balance.value_counts()
    total_jobs = dataset.job.value_counts()
    total_loan = dataset.loan.value_counts()
    total_housing = dataset.housing.value_counts()

    perc_age = def_age * 100 / total_age
    perc_age_category = def_age_category * 100 / total_age_category
    perc_bal_category = def_bal_category * 100 / total_bal_category
    perc_marital = def_marital * 100 / total_marital
    perc_education = def_education * 100 / total_education
    perc_balance = def_balance * 100 / total_balance
    perc_jobs = def_jobs * 100 / total_jobs
    perc_loan = def_loan * 100 / total_loan
    perc_housing = def_housing * 100 / total_housing


    return perc_age.fillna(0),\
            perc_age_category.fillna(0),\
            perc_bal_category.fillna(0),\
            perc_marital.fillna(0),\
            perc_education.fillna(0),\
            perc_balance.fillna(0),\
            perc_jobs.fillna(0),\
            perc_loan.fillna(0),\
            perc_housing.fillna(0)


#6. Quais são as características mais proeminentes de um cliente que possua empréstimo imobiliário?
def ex6(dataset):
    df_housing = dataset.query('housing == "yes" ')
    df_no_hous = dataset.query('housing == "no" ')

    #Count values of the columns where the client has housing loan
    hou_age = df_housing.age.value_counts()
    hou_age_category = df_housing.age_category.value_counts()
    hou_bal_category = df_housing.bal_category.value_counts()
    hou_camp_category = df_housing.camp_category.value_counts()
    hou_prev_category = df_housing.prev_category.value_counts()
    hou_marital = df_housing.marital.value_counts()
    hou_education = df_housing.education.value_counts()
    hou_balance = df_housing.balance.value_counts()
    hou_jobs = df_housing.job.value_counts()
    hou_loan = df_housing.loan.value_counts()
    hou_default = df_housing.default.value_counts()
    hou_contact = df_housing.contact.value_counts()
    hou_y = df_housing.y.value_counts()
    #Special case: we dont want to count the clients that did not were contacted in the previous campaing
    hou_poutcome = df_housing[~(df_housing.poutcome == 'unknown')].poutcome.value_counts()

    hou_total = len(df_housing)
    hou_total_poutcome = len(df_housing[~(df_housing.poutcome == 'unknown')])

    hou_perc_age = hou_age * 100 / hou_total
    hou_perc_age_category = hou_age_category * 100 / hou_total
    hou_perc_bal_category = hou_bal_category * 100 / hou_total
    hou_perc_camp_category = hou_camp_category * 100 / hou_total
    hou_perc_prev_category = hou_prev_category * 100 / hou_total
    hou_perc_marital = hou_marital * 100 / hou_total
    hou_perc_education = hou_education * 100 / hou_total
    hou_perc_balance = hou_balance * 100 / hou_total
    hou_perc_jobs = hou_jobs * 100 / hou_total
    hou_perc_loan = hou_loan * 100 / hou_total
    hou_perc_default = hou_default * 100 / hou_total
    hou_perc_contact = hou_contact * 100 / hou_total
    hou_perc_poutcome = hou_poutcome * 100 / hou_total_poutcome
    hou_perc_y = hou_y * 100 / hou_total

    #Count values of the columns where the client has not housing loan
    not_age = df_no_hous.age.value_counts()
    not_age_category = df_no_hous.age_category.value_counts()
    not_bal_category = df_no_hous.bal_category.value_counts()
    not_camp_category = df_no_hous.camp_category.value_counts()
    not_prev_category = df_no_hous.prev_category.value_counts()
    not_marital = df_no_hous.marital.value_counts()
    not_education = df_no_hous.education.value_counts()
    not_balance = df_no_hous.balance.value_counts()
    not_jobs = df_no_hous.job.value_counts()
    not_loan = df_no_hous.loan.value_counts()
    not_default = df_no_hous.default.value_counts()
    not_contact = df_no_hous.contact.value_counts()
    not_poutcome = df_no_hous[~(df_no_hous.poutcome == 'unknown')].poutcome.value_counts()
    not_y = df_no_hous.y.value_counts()

    not_total = len(df_no_hous)
    not_total_poutcome = len(df_no_hous[~(df_no_hous.poutcome == 'unknown')])

    not_perc_age = not_age * 100 / not_total
    not_perc_age_category = not_age_category * 100 / not_total
    not_perc_bal_category = not_bal_category * 100 / not_total
    not_perc_camp_category = not_camp_category * 100 / not_total
    not_perc_prev_category = not_prev_category * 100 / not_total
    not_perc_marital = not_marital * 100 / not_total
    not_perc_education = not_education * 100 / not_total
    not_perc_balance = not_balance * 100 / not_total
    not_perc_jobs = not_jobs * 100 / not_total
    not_perc_loan = not_loan * 100 / not_total
    not_perc_default = not_default * 100 / not_total
    not_perc_contact = not_contact * 100 / not_total
    not_perc_poutcome = not_poutcome * 100 / not_total_poutcome
    not_perc_y = not_y * 100 / not_total

    return pd.DataFrame({"Housing": hou_perc_age.fillna(0),
                         "Not_Housing":not_perc_age.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_age_category.fillna(0),
                             "Not_Housing":not_perc_age_category.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_bal_category.fillna(0),
                             "Not_Housing":not_perc_bal_category.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_camp_category.fillna(0),
                             "Not_Housing":not_perc_camp_category.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_prev_category.fillna(0),
                             "Not_Housing":not_perc_prev_category.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_marital.fillna(0),
                             "Not_Housing":not_perc_marital.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_education.fillna(0),
                             "Not_Housing":not_perc_education.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_balance.fillna(0),
                             "Not_Housing":not_perc_balance.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_jobs.fillna(0),
                             "Not_Housing":not_perc_jobs.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_loan.fillna(0),
                             "Not_Housing":not_perc_loan.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_default.fillna(0),
                             "Not_Housing":not_perc_default.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_contact.fillna(0),
                             "Not_Housing":not_perc_contact.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_poutcome.fillna(0),
                             "Not_Housing":not_perc_poutcome.fillna(0)}).sort_index(),\
               pd.DataFrame({"Housing": hou_perc_y.fillna(0),
                             "Not_Housing":not_perc_y.fillna(0)}).sort_index()

try: dataset
except NameError:
    dataset = pd.read_csv('data/bank-full.csv',sep=';',header='infer')

#boxplots
show_box(dataset.duration, title="Duração")
show_box(dataset.age, title="Idade")
show_box(dataset.balance, title="Saldo Médio Anual")
show_box(dataset.previous, title="Contatos Campanha Anterior")
show_box(dataset.campaign, title="Contatos Campanha Atual")

#cehcking outliers
check_outliers (dataset)
#Como temos mtos valores 0 na coluna previous (e nao serao usados), verificamos os outliers sem esses valores
check_outliers (dataset[~(dataset.previous == 0)])

#Verifying distribution of values

#categorizing
dataset = age_category(dataset)
dataset = bal_category(dataset)
dataset = prev_category(dataset)
dataset = camp_category(dataset)


#Solutions:

#1. Qual profissão tem mais tendência a fazer um empréstimo? De qual tipo?
sol_keys = ("full", "loans", "pers_loans", "housing")

#calculate the rate of clients who have some kind of loan
sol_tuples = ex1(dataset)
sol_ex1_original = dict(zip(sol_keys, sol_tuples))

#Prnting results
print ("Loans")
print(sol_ex1_original['loans'])

print ("Housing")
print(sol_ex1_original['housing'])

print ("Personal Loans")
print(sol_ex1_original['pers_loans'])

#Prinitng charts
sol_ex1_original["full"][['Percent']].plot.bar(title =
                "Porcentagem de clientes com\nEMPRESTIMOS por PROFISSÃO")
sol_ex1_original["full"][['Percent_Housing']].sort_values(by='Percent_Housing').plot.bar(
        title = "Porcentagem de clientes com\nEMPRESTIMO IMOBILIÁRIO por PROFISSÂO")
sol_ex1_original["full"][['Percent_Personal']].sort_values(by='Percent_Personal').plot.bar(
        title = "Porcentagem de clientes com\nEMPRESTIMO PESSOAL por PROFISSÂO")

#2. Fazendo uma relação entre número de contatos e sucesso da campanha quais são os pontos relevantes a serem observados?
#3. Baseando-se nos resultados de adesão desta campanha qual o número médio e o máximo de ligações que você indica para otimizar a adesão?

#calculate the distribution of contatcs and outcomos of previous campaing
prev_success = ex2_previous(dataset)
print(prev_success)

#calculate the distribution of contatcs and outcoms of current campaing
curr_success = ex2_3_current_percentage (dataset)
print(curr_success)

#Prinitng charts
show_bar(prev_success , title="Porcentagem de SUCCESSO da campaha\nANTERIOR por quantidade de CONTATOS")
show_bar(curr_success , title="Porcentagem de SUCCESSO da campaha\nATUAL por quantidade de CONTATOS")


#4. O resultado da campanha anterior tem relevância na campanha atual?
#Calculate rate of success of current campaing based on the outcome of previous campaing
sol_ex4_original = ex4(dataset)

print (sol_ex4_original)
sol_ex4_original.plot.bar(
        title="% de seucesso na campanha ATUAL para cada\nresultado em relação à campanha ANTERIOR")

#5. Qual o fator determinante para que o banco exija um seguro de crédito?
sol_keys =("def_age","def_age_category","def_bal_category",
           "def_marital","def_education","def_balance",
           "def_jobs","def_loan","def_housing")
#Calculate rate of DEFAULT among different colmns
sol_tuples = ex5(dataset)
sol_ex5_original = dict(zip(sol_keys, sol_tuples))

#Plotting chats
show_bar(sol_ex5_original["def_age_category"],title="% de De credito em DEFAULT por IDADE")
show_bar(sol_ex5_original["def_bal_category"],title="% de De credito em DEFAULT\npor MEDIA DE BALANÇO")
show_bar(sol_ex5_original["def_marital"],title="% de De credito em DEFAULT\npor ESTADO CIVIL")
show_bar(sol_ex5_original["def_education"],title="% de De credito em DEFAULT\npor EDUCAÇÃO")
show_bar(sol_ex5_original["def_loan"],title="% de De credito em DEFAULT por\nEMPRESTIMO PESS.")
show_bar(sol_ex5_original["def_housing"],title="% de De credito em DEFAULT\npor EMPRESTIMO IMOB.")
sol_ex5_original["def_jobs"].sort_values().plot.bar(title="% de De credito em DEFAULT\npor PROFISSÃO")

print("Frequencia de DEFAULT considerando todos clientes")
print (100 * dataset.default.value_counts()/dataset.default.value_counts().sum())

print("Frequencia de DEFAULT por saldo medio")
print(sol_ex5_original["def_bal_category"])

#6. Quais são as características mais proeminentes de um cliente que possua empréstimo imobiliário?
sol_keys = ("hou_age","hou_age_category","hou_bal_category","hou_camp_category","hou_prev_category","hou_marital","hou_education","hou_balance","hou_jobs","hou_loan","hou_default","hou_contact","hou_poutcome","hou_y")
sol_tuples = ex6(dataset)
sol_ex6_original = dict(zip(sol_keys, sol_tuples))

sol_ex6_original["hou_age_category"].plot.bar(title="Distribuição de IDADE dos clientes")
sol_ex6_original["hou_bal_category"].plot.bar(title="Distribuição de SALDO MEDIO dos clientes", legend=False)
sol_ex6_original["hou_camp_category"].plot.bar(
        title="Distribuição de QTD de\nCONTATOS da CAMP. ATUAL dos clientes")
sol_ex6_original["hou_prev_category"].plot.bar(
        title="Distribuição de QTD de\nCONTATOS da CAMP. ANTERIOR dos clientes")
sol_ex6_original["hou_marital"].plot.bar(title="Distribuição de ESTADO CIVIL dos clientes")
sol_ex6_original["hou_education"].plot.bar(title="Distribuição de EDUCAÇÃO dos clientes")
sol_ex6_original["hou_loan"].plot.bar(title="Distribuição de\nEMPRESTIMO PESSOAL dos clientes ")
sol_ex6_original["hou_default"].plot.bar(title="Distribuição de DEFAULT dos clientes")
sol_ex6_original["hou_contact"].plot.bar(title="Distribuição de TIPO DE CONTATO dos clientes")
sol_ex6_original["hou_poutcome"].plot.bar(title="Distribuição de SUCESSO\nda CAMP. ANTERIOR dos clientes")
sol_ex6_original["hou_y"].plot.bar(title="Distribuição de SUCESSO\nda CAMP. ATUAL dos clientes")
sol_ex6_original["hou_jobs"].sort_values(by='Housing').plot.bar(
        title="Distribuição de PROFISSÃO dos clientes")

print("Porcentagem de pessoas com menos de 51 anos:")
print(sol_ex6_original["hou_age_category"][0:3].sum())

print("Distribuição de SALDO MEDIO:")
print(sol_ex6_original["hou_bal_category"])

print("Distribuição de EDUCAÇÂO:")
print(sol_ex6_original["hou_education"])