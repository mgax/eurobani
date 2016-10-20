import csv
import re
from datetime import date

def parse_date(text):
    if text.strip() in ['', '-']:
        return None
    m = re.match(r'^(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})$', text)
    return '{year}-{month}-{day}'.format(**m.groupdict())

def parse_money(text):
    if text.strip() in ['', '-']:
        return None
    return float(text.replace(',', ''))

def contracts(path):
    def parse(row):
        return {
            'smis':             row['Cod SMIS'],
            'caen':             row['Caen Code'],
            'rationale':        row['Rationale'],
            'locality':         row['Localitatea'],
            'objectives':       row['Objectives'],
            'contract_date':    row['Data contract/decizie finantare'],
            'contract_number':  row['Nr contract/decizie finantare'],
            'expected_results': row['Expected Results'],

            'approval_date':     parse_date(row['Data aprobare proiect']),
            'start_date':        parse_date(row['Proj Start Date']),
            'end_date':          parse_date(row['Proj End Date']),
            'last_payment_date': parse_date(row['Last Payment']),

            'state':            row['Stare'],
            'title':            row['Titlu proiect'],
            'region':           row['Regiunea'],
            'county':           row['Judetul'],
            'authority':        row['Autoritate responsabila'],
            'representative':   row['Legal Repr'],
            'beneficiary_type': row['Tip beneficiar'],
            'beneficiary':      row['Beneficiar'],

            'eu_grant_budget':             parse_money(row['Bug neram UE']),
            'national_grant_budget':       parse_money(row['Bug neram nat']),
            'nongrant_budget':             parse_money(row['Bug chelt neram']),
            'eligible_budget':             parse_money(row['Bug chelt elig']),
            'ineligible_budget':           parse_money(row['Bug chelt neelig']),
            'eligible_beneficiary_budget': parse_money(row['Bug elig benef']),
            'total_budget':                parse_money(row['Bug total']),
            'reimbursed':                  parse_money(row['Rambursat']),
            'prefinance':                  parse_money(row['Prefinantare']),
            'prefinance_amortized':        parse_money(row['Prefin Amortiz']),
        }

    with path.open('rt', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            from pprint import pprint; pprint(parse(row))
            break
