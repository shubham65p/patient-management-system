

class PatientService:
    def __init__(self, patient_repo, appointment_repo, medicine_repo, therapy_repo):
        self.patient_repo = patient_repo
        self.appointment_repo = appointment_repo
        self.medicine_repo = medicine_repo
        self.therapy_repo = therapy_repo

    def add_patient(self, patient):
        patient_id = self.patient_repo.add(patient)

        for ap in patient.fees.data:
            appt_id = self.appointment_repo.add(patient_id, ap.appointment, ap.consultation)

            for med in ap.medicines:
                self.medicine_repo.add(appt_id, med.name, med.fee)

            for th in ap.therapies:
                self.therapy_repo.add(appt_id, th.name, th.fee)

        return patient_id
    
    def update_patient(self, patient_id, raw_data):
        self.patient_repo.update(patient_id, raw_data)


        for appt in raw_data.fees.data:
            appt_id = self.appointment_repo.add(patient_id, appt.appointment, appt.consultation)

            for med in appt.medicines:
                self.medicine_repo.add(appt_id, med.name, med.fee)

            for th in appt.therapies:
                self.therapy_repo.add(appt_id, th.name, th.fee)
    
    def get_fees_data(self, patient_id):
        appointments = self.appointment_repo.get_appointment_by_patient_id(patient_id)
        fees_data = []
        for appt in appointments:
            ap = {
                "appointment": appt[2],     
                "consultation": appt[3],
                "medicines": [],
                "therapies": []
            }

            medicines = self.medicine_repo.get_medicine_by_appointment_id(appt[0])
            for med in medicines:
                ap["medicines"].append({"name": med[2], "fee": med[3]})

            therapies = self.therapy_repo.get_therapy_by_appointment_id(appt[0])
            for th in therapies:
                ap["therapies"].append({"name": th[2], "fee": th[3] })
            
            fees_data.append(ap)

        return fees_data


