# -*- coding: utf-8 -*-
"""Import SEND notifications
"""

import base64
import hashlib
import os
import sys
import time
import zipfile
from dataclasses import dataclass, fields

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'send')
DOCUMENT_FILE_NAME = 'notification.pdf'
DOCUMENT_CONTENT_TYPE = 'application/pdf'
F24_METADATA_FILE_NAME = 'f24_metadata.json'
F24_METADATA_CONTENT_TYPE = 'application/json'


@dataclass
class CSVRow:
    paProtocolNumber: str = None
    externalCampaignId: str = None
    campaignName: str = None
    notificationFeePolicy: str = 'DELIVERY_MODE'
    physicalCommunicationType: str = 'AR_REGISTERED_LETTER'
    subject: str = 'Soak-test send massive import'
    senderDenomination: str = 'Ente P4PA intermediato 2'
    senderTaxId: str = '99999999982'
    taxonomyCode: str = '030101P'
    paFeeCents: int = 100
    vat: int = 22
    pagoPaIntMode: str = 'ASYNC'
    recipientType: str = 'PF'
    taxId: str = 'FRRMRA90A41F205D'
    denomination: str = 'Maria Ferrero'
    address: str = 'Via Larga, 10'
    zip: str = '00186'
    municipality: str = 'Roma'
    province: str = 'RM'
    f24PaymentTitle_1: str = 'Soak-test F24'
    f24PaymentApplyCost_1: bool = True
    metadataAttachmentFileName_1: str = F24_METADATA_FILE_NAME
    metadataAttachmentDigest_1: str = None
    metadataAttachmentContentType_1: str = F24_METADATA_CONTENT_TYPE
    documentFileName_1: str = DOCUMENT_FILE_NAME
    documentDigest_1: str = None
    documentContentType_1: str = DOCUMENT_CONTENT_TYPE


def read_resource(file_name: str) -> bytes:
    with open(os.path.join(RESOURCES_DIR, file_name), 'rb') as resource:
        return resource.read()


def sha256_base64(content: bytes) -> str:
    return base64.b64encode(hashlib.sha256(content).digest()).decode()


def create_notification_rows(num_rows: int, timestamp: int, f24_metadata_digest: str, document_digest: str) -> list:
    notification_rows = []

    for i in range(1, num_rows + 1):
        row = CSVRow()
        row.paProtocolNumber = f'PROT_SOAK_{timestamp}_{i}'
        row.externalCampaignId = f'SOAK_TEST_{timestamp}'
        row.campaignName = row.externalCampaignId
        row.metadataAttachmentDigest_1 = f24_metadata_digest
        row.documentDigest_1 = document_digest

        notification_rows.append(row)

    return notification_rows


def to_csv_value(val) -> str:
    if val is None:
        return ''
    if isinstance(val, bool):
        return str(val).lower()
    return str(val)


def to_csv_lines(csv_rows: list[CSVRow]) -> list:
    field_names = [f.name for f in fields(CSVRow)]

    lines = [';'.join(field_names)]
    for row in csv_rows:
        lines.append(';'.join(to_csv_value(getattr(row, f)) for f in field_names))

    return lines


def create_ingestion_flow_file(num_rows):
    timestamp = int(time.time() * 1000)
    document = read_resource(DOCUMENT_FILE_NAME)
    f24_metadata = read_resource(F24_METADATA_FILE_NAME)

    notification_rows = create_notification_rows(num_rows=num_rows, timestamp=timestamp,
                                                 f24_metadata_digest=sha256_base64(f24_metadata),
                                                 document_digest=sha256_base64(document))

    filename = f'SendCampaignSoakTest_{timestamp}-1_0'
    zip_file_path = f'{filename}.zip'

    with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_STORED) as zip_file:
        zip_file.writestr(f'{filename}.csv', '\n'.join(to_csv_lines(csv_rows=notification_rows)))
        for i in range(1, num_rows + 1):
            zip_file.writestr(f'{i}/{DOCUMENT_FILE_NAME}', document)
            zip_file.writestr(f'{i}/{F24_METADATA_FILE_NAME}', f24_metadata)

    return zip_file_path


def main():
    num_rows = int(sys.argv[1])

    # Validazione input
    error = False
    if num_rows <= 0:
        print(f"⚠️ Il numero di righe deve essere maggiore di 0.")
        error = True

    if not error:
        zip_file_path = create_ingestion_flow_file(num_rows)

        print(zip_file_path)


if __name__ == "__main__":

    main()
