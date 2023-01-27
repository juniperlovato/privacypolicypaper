# This list contains all the types of PII identified by CCPA and CPRA legislature, as well as the concrete terms
# that are associated with each type of PII. The list is used to identify PII in text.

import pandas as pd

from lib import data_cleaning

def get_list(cleaning_steps=set()):
    processed = data_cleaning.clean_series(pd.Series(__PII_TERMS), log=False, parallel=False, steps=cleaning_steps)
    joined = [' '.join(tokens) for tokens in processed]
    # return terms without duplicates
    return list(set(joined))

# Note: Make sure this is the same as in negation_filtered_policytext_PII.ipynb
__PII_TERMS = [
    'Identifiers',
    'alias',
    'online identifier',
    'Internet Protocol (IP) address',
    'account name',
    'social security number',
    'passport number',
    'Customer records information',
    'IDENTIFICATION NUMBER',
    'signature',
    'electronic mail address',
    'address',
    'telephone number',
    'PROTECTED HEALTH INFORMATION',
    'state identification card number',
    'education',
    'employment history',
    'bank account number',
    'face',
    'financial information',
    'Records of personal property',
    'products purchased',
    'health condition',
    'consuming histories',
    'Services purchased',
    'eye color',
    'retina scans',
    'network activity',
    'Internet  activity',
    'search history',
    'Geolocation',
    'visual',
    'thermal',
    'olfactory',
    'Professional',
    'Medical Condition',
    'Characteristics',
    'Aggregated data',
    'Predispositions',
    'Behavior',
    'specific location',
    'facial recognition',
    'physiological',
    'behavioral',
    'Audio',
    'DNA',
    'iris',
    'retina',
    'hand',
    'palm',
    'vein patterns',
    'voice recordings',
    'minutiae template',
    'HEALTH STATUS',
    'keystroke patterns ',
    'keystroke rhythms',
    'gait rhythms',
    'sleep',
    'health',
    'exercise',
    'Cross-context behavioral advertising',
    'targeted advertising',
    'Dark pattern',
    'Personal information',
    'RACIAL',
    'real name',
    'Account number',
    'postal address',
    'financial account number',
    'Internet Protocol address',
    'Gender identity',
    'email address',
    'security question',
    'Color',
    'Religion',
    'Sex',
    'Sexual orientation',
    'Marital status',
    'National origin',
    'Ancestry',
    'Genetic information',
    'Retaliation for reporting patient abuse in tax-supported institutions',
    'Age',
    'religious dress',
    'pregnancy',
    'Gender',
    'childbirth',
    'breastfeeding',
    'mental characteristics',
    'physical characteristics',
    'HIV/AIDS',
    'cancer',
    'genetic characteristics',
    'Geolocation data',
    'record of cancer',
    'history of cancer',
    'gender expression',
    'abilities',
    'MENTAL CONDITION',
    'PREDICT',
    'biological',
    'purchasing tendencies',
    'Aggregate consumer information',
    'first name',
    'voice',
    'electronic network activity',
    'biological characteristic',
    'interaction with an advertisement',
    'Browsing history',
    'employment',
    'Race',
    'health records',
    'citizenship',
    'Military or veteran status',
    'medical identification number',
    'access code',
    'preferences',
    'protected classifications',
    'psychological trends',
    'Commercial information',
    'medical information',
    'attitudes',
    'intelligence',
    'Name',
    'driver\'s license',
    'Sensitive personal information',
    'Precise geolocation',
    'locate',
    'geographic area',
    'radius',
    'Sensitive data',
    'Profiling',
    'consumer\'s social security',
    'driver\'s license',
    'state Identification card',
    'account log-In',
    'credit card',
    'health insurance information',
    'password',
    'credentials allowing access to an account',
    'combination',
    'racial origin',
    'ethnic origin',
    'philosophical beliefs',
    'union membership',
    'text messages',
    'genetic data',
    'biometric data',
    'Personally identifiable information',
    'security code',
    'fingerprint',
    'device identifier',
    'IP address',
    'cookies',
    'beacons',
    'pixel tags',
    'customer number',
    'unique pseudonym',
    'telephone numbers',
    'persistent identifier',
    'probabilistic identifier',
    'family',
    'child',
    'identifier template',
    'DE-IDENTIFIED DATA',
    'HEALTH-CARE INFORMATION',
    'HEALTH-CARE PROVIDER',
    'MEDICINE',
    'PHARMACY',
    'CHIROPRACTIC',
    'NURSING',
    'PHYSICAL THERAPY',
    'PODIATRY',
    'DENTISTRY',
    'OPTOMETRY',
    'OCCUPATIONAL THERAPY',
    'HEALING ARTS',
    'IDENTIFIED',
    'IDENTIFIABLE INDIVIDUAL',
    'ONLINE IDENTIFIER',
    'PERSONAL DATA',
    'products obtained',
    'AUTOMATED PROCESSING',
    'Request for Pregnancy Disability Leave',
    'ANALYZE',
    'ECONOMIC SITUATION',
    'PERSONAL PREFERENCES',
    'religious beliefs',
    'RELIABILITY',
    'LOCATION',
    'MOVEMENTS',
    'PHYSICAL HEALTH CONDITION',
    'DIAGNOSIS',
    'credit card number',
    'CITIZENSHIP STATUS',
    'GENETIC',
    'last name',
    'mobile ad identifiers',
    'HEALTH-CARE',
    'PATIENT',
    'fingerprints',
    'products considered',
    'physical description',
    'voiceprint',
    'eye retinas',
    'Unique identifier',
    'consuming tendencies',
    'faceprint',
    'driver\'s license number',
    'Services considered',
    'global positioning system',
    'latitude',
    'longitude',
    'coordinates',
    'interests',
    'financial account',
    'user alias',
    'irises',
    'Request for leave for an employee\'s own serious health condition',
    'condition',
    'physical',
    'diagnosis',
    'insurance policy number',
    'immigration status',
    'known child',
    'sex life',
    'height',
    'AIDS',
    'medical diagnosis',
    'religious grooming practices',
    'Identifiable individual',
    'debit card',
    'ethnic',
    'origin',
    'medical treatment',
    'Inferences',
    'medical history',
    'mental health',
    'physical health',
    'mental',
    'Biometric information',
    'email content',
    'physical representation',
    'biological pattern',
    'mother\'s maiden name',
    'interaction with an internet website application',
    'deoxyribonucleic acid',
    'purchasing histories',
    'Disability',
    'targeting of advertising',
    'movements',
    'Hair color',
    'digital representation',
    'Initials',
    'SPECIFIC GEOLOCATION DATA',
    'driver authorization card number',
    'identification card number',
    'debit card number',
    'health insurance identification number',
    'user name',
    'Request for family care leave',
    'date of birth',
    'place of birth',
    'unique biometric',
    'human body',
    'HIV',
    'biometric',
    'language',
    'household',
    'driver\'s license number',
    'government-issued identification number',
    'driver license',
    'nondriver State identification card number',
    'individual taxpayer identification number',
    'military identification card number',
    'gait patterns',
    'unique personal identifier',
    'passwords',
    'personal identification number',
    'services obtained',
    'wellness program',
    'health promotion',
    'disease prevention',
    'health insurance policy number'
]
