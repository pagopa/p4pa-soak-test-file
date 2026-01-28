# -*- coding: utf-8 -*-
"""Import debt positions
"""

from dataclasses import dataclass
import uuid
import random
import pandas
from datetime import datetime, timedelta

@dataclass
class CSVRow:
    _HEADER_FIELDS = {
       'action': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'azione', 'EN': 'action'},
        'draft': {'versions': ["2_0", "2_0-eng"], 'IT': 'draft', 'EN': 'draft'},
        'iupdOrg': {'versions': ["2_0", "2_0-eng"], 'IT': 'IUPD', 'EN': 'iupdOrg'},
        'description': {'versions': ["2_0", "2_0-eng"], 'IT': 'descrizionePosizioneDebitoria', 'EN': 'description'},
        'validityDate': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'dataValidita', 'EN': 'validityDate'},
        'paymentOptionIndex': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'indiceOpzionePagamento',
                               'EN': 'paymentOptionIndex'},
        'paymentOptionType': {'versions': ["2_0", "2_0-eng"], 'IT': 'tipoOpzionePagamento', 'EN': 'paymentOptionType'},
        'paymentOptionDescription': {'versions': ["2_0", "2_0-eng"], 'IT': 'descrizioneOpzionePagamento',
                                     'EN': 'paymentOptionDescription'},
        'iud': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'iud', 'EN': 'iud'},
        'iuv': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'codIUV', 'EN': 'iuv'},
        'dueDate': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'dataEsecuzionePagamento',
                    'EN': 'dueDate'},
        'amount': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'importoDovuto',
                   'EN': 'amount'},
        'remittanceInformation': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"],
                                  'IT': 'causaleVersamento', 'EN': 'remittanceInformation'},
        'entityType': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"],
                       'IT': 'tipoIdentificativoUnivoco', 'EN': 'entityType'},
        'fiscalCode': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"],
                       'IT': 'codiceIdentificativoUnivoco', 'EN': 'fiscalCode'},
        'fullName': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'anagraficaPagatore',
                     'EN': 'fullName'},
        'address': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'indirizzoPagatore',
                    'EN': 'address'},
        'civic': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'civicoPagatore',
                  'EN': 'civic'},
        'postalCode': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'capPagatore',
                       'EN': 'postalCode'},
        'location': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'localitaPagatore',
                     'EN': 'location'},
        'province': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'provinciaPagatore',
                     'EN': 'province'},
        'nation': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'nazionePagatore',
                   'EN': 'nation'},
        'email': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'mailPagatore',
                  'EN': 'email'},
        'notificationDate': {'versions': ["2_0", "2_0-eng"], 'IT': 'dataNotifica', 'EN': 'notificationDate'},
        'multiDebtor': {'versions': ["2_0", "2_0-eng"], 'IT': 'multiDebtor', 'EN': 'multiDebtor'},
        'legacyPaymentMetadata': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"],
                                  'IT': 'datiSpecificiRiscossione', 'EN': 'legacyPaymentMetadata'},
        'generateNotice': {'versions': ["1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'flgGeneraIuv',
                                'EN': 'generateNotice'},
        'flagPuPagoPaPayment': {'versions': ["2_0", "2_0-eng"], 'IT': 'flagPagamentoPu',
                                'EN': 'flagPuPagoPaPayment'},
        'balance': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'bilancio',
                    'EN': 'balance'},
        'debtPositionTypeCode': {'versions': ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"], 'IT': 'tipoDovuto',
                                 'EN': 'debtPositionTypeCode'},
        'flagMultibeneficiary': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'flagMultiBeneficiario',
                                 'EN': 'flagMultibeneficiary'},
        'numberBeneficiary': {'versions': ["2_0", "2_0-eng"], 'IT': 'numeroBeneficiari', 'EN': 'numberBeneficiary'},
        'orgFiscalCode_2': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'codiceFiscaleEnte_2',
                            'EN': 'orgFiscalCode_2'},
        'orgName_2': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'DenominazioneEnte_2', 'EN': 'orgName_2'},
        'iban_2': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'IbanAccreditoEnte_2', 'EN': 'iban_2'},
        'remittanceInformation_2': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'CausaleVersamentoEnte_2',
                                    'EN': 'remittanceInformation_2'},
        'amount_2': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'importoVersamentoEnte_2', 'EN': 'amount_2'},
        'category_2': {'versions': ["1_4", "2_0", "2_0-eng"], 'IT': 'codiceTassonomiaEnte_2', 'EN': 'category_2'},
        'orgFiscalCode_3': {'versions': ["2_0", "2_0-eng"], 'IT': 'codiceFiscaleEnte_3', 'EN': 'orgFiscalCode_3'},
        'orgName_3': {'versions': ["2_0", "2_0-eng"], 'IT': 'DenominazioneEnte_3', 'EN': 'orgName_3'},
        'iban_3': {'versions': ["2_0", "2_0-eng"], 'IT': 'IbanAccreditoEnte_3', 'EN': 'iban_3'},
        'remittanceInformation_3': {'versions': ["2_0", "2_0-eng"], 'IT': 'CausaleVersamentoEnte_3',
                                    'EN': 'remittanceInformation_3'},
        'amount_3': {'versions': ["2_0", "2_0-eng"], 'IT': 'importoVersamentoEnte_3', 'EN': 'amount_3'},
        'category_3': {'versions': ["2_0", "2_0-eng"], 'IT': 'codiceTassonomiaEnte_3', 'EN': 'category_3'},
        'orgFiscalCode_4': {'versions': ["2_0", "2_0-eng"], 'IT': 'codiceFiscaleEnte_4', 'EN': 'orgFiscalCode_4'},
        'orgName_4': {'versions': ["2_0", "2_0-eng"], 'IT': 'DenominazioneEnte_4', 'EN': 'orgName_4'},
        'iban_4': {'versions': ["2_0", "2_0-eng"], 'IT': 'IbanAccreditoEnte_4', 'EN': 'iban_4'},
        'remittanceInformation_4': {'versions': ["2_0", "2_0-eng"], 'IT': 'CausaleVersamentoEnte_4',
                                    'EN': 'remittanceInformation_4'},
        'amount_4': {'versions': ["2_0", "2_0-eng"], 'IT': 'importoVersamentoEnte_4', 'EN': 'amount_4'},
        'category_4': {'versions': ["2_0", "2_0-eng"], 'IT': 'codiceTassonomiaEnte_4', 'EN': 'category_4'},
        'orgFiscalCode_5': {'versions': ["2_0", "2_0-eng"], 'IT': 'codiceFiscaleEnte_5', 'EN': 'orgFiscalCode_5'},
        'orgName_5': {'versions': ["2_0", "2_0-eng"], 'IT': 'DenominazioneEnte_5', 'EN': 'orgName_5'},
        'iban_5': {'versions': ["2_0", "2_0-eng"], 'IT': 'IbanAccreditoEnte_5', 'EN': 'iban_5'},
        'remittanceInformation_5': {'versions': ["2_0", "2_0-eng"], 'IT': 'CausaleVersamentoEnte_5',
                                    'EN': 'remittanceInformation_5'},
        'amount_5': {'versions': ["2_0", "2_0-eng"], 'IT': 'importoVersamentoEnte_5', 'EN': 'amount_5'},
        'category_5': {'versions': ["2_0", "2_0-eng"], 'IT': 'codiceTassonomiaEnte_5', 'EN': 'category_5'},
        'executionConfig': {'versions': ["2_0", "2_0-eng"], 'IT': 'configurazioniEsecuzione', 'EN': 'executionConfig'}
    }

    action: str = 'I'
    draft: bool = False
    iupdOrg: str = None
    description: str = None
    validityDate: str = None
    paymentOptionIndex: int = 1
    paymentOptionType: str = 'SINGLE_INSTALLMENT'
    paymentOptionDescription: str = None
    iud: str = None
    iuv: str = None
    dueDate: str = None
    amount: str = None
    remittanceInformation: str = None
    entityType: str = 'F'
    fiscalCode: str = 'FRRMRA90A41F205D'
    fullName: str = 'Maria Ferrero'
    address: str = "Via del Corso"
    civic: str = "1"
    postalCode: str = "00186"
    location: str = "Roma"
    province: str = "RM"
    nation: str = "IT"
    email: str = 'maria.ferrero@email.it'
    notificationDate: str = None
    multiDebtor: bool = False
    legacyPaymentMetadata: str = None
    generateNotice: bool = True
    flagPuPagoPaPayment: bool = True
    balance: str = None
    debtPositionTypeCode: str = 'FEATURE_TEST'
    flagMultibeneficiary: bool = False
    numberBeneficiary: int = 1
    orgFiscalCode_2: str = None
    orgName_2: str = None
    iban_2: str = None
    remittanceInformation_2: str = None
    amount_2: str = None
    category_2: str = None
    orgFiscalCode_3: str = None
    orgName_3: str = None
    iban_3: str = None
    remittanceInformation_3: str = None
    amount_3: str = None
    category_3: str = None
    orgFiscalCode_4: str = None
    orgName_4: str = None
    iban_4: str = None
    remittanceInformation_4: str = None
    amount_4: str = None
    category_4: str = None
    orgFiscalCode_5: str = None
    orgName_5: str = None
    iban_5: str = None
    remittanceInformation_5: str = None
    amount_5: str = None
    category_5: str = None
    executionConfig: str = None

    @property
    def HEADER_FIELDS(self):
        return self._HEADER_FIELDS

def create_installments_rows(num_rows: int) -> list:
    installments_rows = []
    due_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    for i in range(1, num_rows+1):
      row = CSVRow()
      row.iupdOrg = f'Import-test-{uuid.uuid4().hex[:10]}'
      row.description = f'Import test debt position {str(i)}'
      row.paymentOptionDescription = f'Import test payment option {str(i)}'
      row.iud = f'Import_{str(i)}_{datetime.now().strftime("%Y%m%d%H%M%S%f")[:15]}_{uuid.uuid4().hex[:5]}'
      row.dueDate = due_date
      row.amount = str(random.randint(1, 200))
      row.remittanceInformation = f'Feature test installment {str(i)}'

      installments_rows.append(row)

    return installments_rows

def to_csv_lines(csv_rows: list[CSVRow], csv_version: str, with_header=True) -> list:
    if not csv_rows:
        return []

    lang = 'EN' if csv_version == '2_0-eng' else 'IT'

    first_row = csv_rows[0]
    active_fields = [f for f, meta in first_row.HEADER_FIELDS.items()
                     if csv_version in meta['versions'] and hasattr(first_row, f)]

    lines = []

    if with_header:
        headers = [first_row.HEADER_FIELDS[f][lang] for f in active_fields]
        lines.append(';'.join(f'"{h}"' if ';' in h else h for h in headers))

    for row in csv_rows:
        values = []
        for f in active_fields:
            val = getattr(row, f)
            if val is None:
                values.append('')
            elif hasattr(val, 'value'):
                values.append(val.value)
            else:
                values.append(str(val))

        lines.append(';'.join(f'"{v}"' if ';' in v else v for v in values))

    return lines


def create_ingestion_flow_file(num_rows, csv_version):
    installments_rows = create_installments_rows(num_rows=num_rows)

    filename = f'ImportTest_{datetime.now().strftime("%Y%m%d%H%M%S")}_{csv_version}'
    zip_file_path = f'{filename}.zip'

    csv_lines = to_csv_lines(csv_rows=installments_rows, csv_version=csv_version)

    dataset_dataframe = pandas.DataFrame(data=csv_lines)

    dataset_dataframe.to_csv(zip_file_path, index=False, header=False,
                             compression=dict(method='zip', archive_name=f'{filename}.csv'))

    return zip_file_path


def main():
    version = str(sys.argv[1])
    num_rows = int(sys.argv[2])

    # Validazione input
    error = False
    if num_rows <= 0:
      print("⚠️ Il numero di righe deve essere positivo. Usando 1000 come default.")
      error = True
    if version not in ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"]:
      print('⚠️ Le uniche versioni supportate sono: ["1_0", "1_1", "1_2", "1_3", "1_4", "2_0", "2_0-eng"]')
      error = True

    # Genera il file
    if not error:
      zip_file_path = create_ingestion_flow_file(num_rows, version)

      print(zip_file_path)

if __name__ == "__main__":

  main()