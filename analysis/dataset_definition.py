# copy from "https://github.com/opensafely/Pharmacy-First-protocol-2-healthcare-usage/blob/main/analysis/codelist.py"
# opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition.py
# opensafely exec ehrql:v1 create-dummy-tables analysis/dataset_definition.py dummy-folder

# The data sources used is TPP,
# including patients, practice_registrations, clinical_events,
# and self-defined SNOMED code lists
from ehrql import create_dataset
from ehrql.tables.tpp import patients, practice_registrations, clinical_events
import codelists

dataset = create_dataset() # create an empty table
dataset.configure_dummy_data(population_size=20) # By default, ten patients will be generated in a dummy dataset. This line increases this number.

# analysis time frame
start_date = "2020-03-31"
index_date = "2025-11-30"

# patient registration criteria
registration_start = practice_registrations.for_patient_on(start_date)
registration_end = practice_registrations.for_patient_on(index_date)

# select GP clinical events within time frame
selected_events = clinical_events.where(clinical_events.date.is_on_or_between(start_date, index_date))

# define PF consultation events
pf_consultation_events = selected_events.where(selected_events.snomedct_code.is_in(codelists.pf_consultation_events_dict["pf_consultation_services_combined"]))

# create a variable - whether a patient has had PF consultation event or not
dataset.has_pf_consultation = pf_consultation_events.exists_for_patient()

pf_ids = pf_consultation_events.consultation_id
selected_pf_id_events = selected_events.where(
    selected_events.consultation_id.is_in(pf_ids)
)
dataset.sex = patients.sex
dataset.age = patients.age_on(index_date)
dataset.define_population(
    registration_start.exists_for_patient() | registration_end.exists_for_patient()) 