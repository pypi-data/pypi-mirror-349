from py_convert.format_settings import SettingsBase

class SettingsLabo(SettingsBase):
    """Gestion des paramètres de l'import du fichier Excel de L@B.BIO."""
    def name(self):
        return "L@B.BIO"
    
    def get_allowed_import(self) -> list[str]:
        return ["VOSFACTURES"]
    
    def process_file(self):
        df = self.entries
        df = self.replace_str(df, "CompteNum", "70600000", "70113100")
        df = self.replace_str(df, "CompteNum", "44571000", "44551100")
        return df