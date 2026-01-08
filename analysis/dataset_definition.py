# copy from "https://github.com/opensafely/Pharmacy-First-protocol-2-healthcare-usage/blob/main/analysis/codelist.py"
# opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition.py
# opensafely exec ehrql:v1 create-dummy-tables analysis/dataset_definition.py dummy-folder

from ehrql import create_dataset
from ehrql.tables.tpp import patients, practice_registrations, clinical_events
import codelists
dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000) # By default, ten patients will be generated in a dummy dataset. This line increases this number.

start_date = "2024-01-31"

index_date = "2025-11-30"
registration_start = practice_registrations.for_patient_on(start_date)
registration_end = practice_registrations.for_patient_on(index_date)
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between(start_date, index_date)
)
pf_consultation_events = selected_events.where(selected_events.snomedct_code.is_in(codelists.pf_consultation_events_dict["pf_consultation_services_combined"]))

 
dataset.has_pf_consultation = pf_consultation_events.exists_for_patient()
 
pf_ids = pf_consultation_events.consultation_id
selected_pf_id_events = selected_events.where(
    selected_events.consultation_id.is_in(pf_ids)
)
dataset.sex = patients.sex
dataset.age = patients.age_on(index_date)
dataset.define_population(
    registration_start.exists_for_patient() | registration_end.exists_for_patient()) 