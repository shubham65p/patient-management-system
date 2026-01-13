from config import config

class PatientSearchService:
    ALLOWED_COLUMNS = config['ALLOWED_COLUMNS']

    def build_query(self, criteria: str, value: str):
        if criteria == "all":
            return "SELECT * FROM patients", ()

        # if criteria not in self.ALLOWED_COLUMNS:
        #     raise ValueError("Invalid search column")

        if criteria == "gender":
            return (
                "SELECT * FROM patients WHERE LOWER(gender) = LOWER(?)",
                (value,)
            )

        return (
            f"SELECT * FROM patients WHERE {criteria} LIKE ?",
            (f"%{value}%",)
        )
