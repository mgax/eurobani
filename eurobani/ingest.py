import csv
import re
from datetime import date
from . import models

def parse_date(text):
    if text.strip() in ['', '-']:
        return None
    m = re.match(r'^(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})$', text)
    return '{year}-{month}-{day}'.format(**m.groupdict())

def parse_money(text):
    if text.strip() in ['', '-']:
        return None
    return float(text.replace(',', ''))

def chunked(iter, chunk_size):
    try:
        while True:
            buffer = []
            for _ in range(chunk_size):
                buffer.append(next(iter))
            yield buffer

    except StopIteration:
        if buffer:
            yield buffer

def csv_chunked_rows(path, chunk_size=1000):
    with path.open('rt', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        n = 0
        for chunk in chunked(reader, chunk_size):
            yield chunk
            n += len(chunk)
            print(n)

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

    for chunk in csv_chunked_rows(path):
        rows = [models.Contract(data=parse(row)) for row in chunk]
        models.Contract.objects.bulk_create(rows)

def payments(path):
    def parse(row):
        return {
            'smis':             row['Smis Code'],
            'beneficiary_code': row['Benef Code'],
            'beneficiary':      row['Benef Name'],
            'commitment_type':  row['Commitment Type'],
            'contract_number':  row['Contr No'],
            'contract_type':    row['Contr Type Descr'],
            'contractor':       row['Contractor Name'],
            'county':           row['Judet Benef'],
            'locality':         row['Loc Benef'],
            'procedure':        row['Proced Type Descr'],
            'region':           row['Regiune Benef'],
            'status':           row['Status'],
            'subproject':       row['Subproj'],
            'title':            row['Title'],

            'start_date': parse_date(row['Start Date']),
            'end_date':   parse_date(row['End Date']),
            'seap_date':  parse_date(row['Seap Publish Date']),

            'value': parse_money(row['Contr value']),
        }

    for chunk in csv_chunked_rows(path):
        rows = [models.Payment(data=parse(row)) for row in chunk]
        models.Payment.objects.bulk_create(rows)
