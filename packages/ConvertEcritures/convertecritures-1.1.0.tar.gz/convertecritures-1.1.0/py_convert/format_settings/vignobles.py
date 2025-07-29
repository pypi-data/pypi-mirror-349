import polars as pl

from py_convert.error import run_error
from py_convert.format_settings import SettingsBase

class SettingsVignobles(SettingsBase):
    """Gestion des paramètres de l'import du FEC du VIGNOBLES DE SAINT TROPEZ."""
    def name(self):
        return "VIGNOBLES DE SAINT TROPEZ"
    
    def get_allowed_import(self) -> list[str]:
        return ["FEC"]
    
    def process_file(self):
        df = self.entries
        
        # Remplace les comptes fournisseurs et clients par un compte unique
        df = df.with_columns(
            pl.when(pl.col("CompteNum").str.starts_with("411"))
              .then(pl.lit("41100000"))
              .otherwise(pl.col("CompteNum"))
              .alias("CompteNum"),
        )
        df = df.with_columns(
            pl.when(pl.col("CompteNum").str.starts_with("401"))
              .then(pl.lit("40100000"))
              .otherwise(pl.col("CompteNum"))
              .alias("CompteNum")
        )

        client_list = df.filter(
            (pl.col("CompteNum").is_between(
                pl.lit("41100000"), 
                pl.lit("41200000"),
                closed="both"
                ) |
            (pl.col("CompteNum") == pl.lit("41900000"))
        )).select("CompteNum").unique().to_series()

        supplier_list = df.filter(
            (pl.col("CompteNum").is_between(
                pl.lit("40100000"), 
                pl.lit("40200000"),
                closed="both"
                )
        )).select("CompteNum").unique().to_series()

        # Remplace les comptes auxiliaires des clients
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.starts_with("1")) &
                (pl.col("CompteNum").is_in(client_list))
                )
              .then(pl.concat_str([
                  pl.lit("C1"), 
                  pl.col("CompAuxNum").str.slice(1)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum"),
        )
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.starts_with("2")) &
                (pl.col("CompteNum").is_in(client_list))
                )
              .then(pl.concat_str([
                  pl.lit("CC"), 
                  pl.col("CompAuxNum").str.slice(1)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum"),
        )
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.starts_with("CO1")) &
                (pl.col("CompteNum").is_in(client_list))
                )
              .then(pl.concat_str([
                  pl.lit("CC"), 
                  pl.col("CompAuxNum").str.slice(3)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Remplace les comptes auxiliaires des fournisseurs
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.starts_with("200")) &
                (pl.col("CompteNum").is_in(supplier_list))
                )
              .then(pl.concat_str([
                  pl.lit("F"), 
                  pl.col("CompAuxNum").str.slice(3)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum"),
        )
        df = df.with_columns(
            pl.when(
                (pl.col("CompAuxNum").str.starts_with("CO1")) &
                (pl.col("CompteNum").is_in(supplier_list))
                )
              .then(pl.concat_str([
                  pl.lit("FC"), 
                  pl.col("CompAuxNum").str.slice(3)
                  ]))
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum")
        )

        # Supprime le compte auxiliaire si le compte général n'est pas client ou fournisseur
        df = df.with_columns(
            pl.when(~(
                pl.col("CompteNum").is_in(client_list) |
                pl.col("CompteNum").is_in(supplier_list)
                ))
              .then(None)
              .otherwise(pl.col("CompAuxNum"))
              .alias("CompAuxNum"),
            pl.when(~(
                pl.col("CompteNum").is_in(client_list) |
                pl.col("CompteNum").is_in(supplier_list)
                ))
              .then(None)
              .otherwise(pl.col("CompAuxLib"))
              .alias("CompAuxLib")
        )

        # Contrôle si tous les comptes auxiliaires ont été renumérotés
        invalid_entries = df.filter(~(
            pl.col("CompAuxNum").str.starts_with("F") | 
            pl.col("CompAuxNum").str.starts_with("C")
            ))

        # Si ce n'est pas le cas, affiche un message d'erreur
        if invalid_entries.height > 0:
            invalid_entries = invalid_entries.select(
                "JournalCode",
                "JournalLib",
                "EcritureDate",
                "PieceRef",
                "CompteNum",
                "CompAuxNum",
                "CompAuxLib",
                "EcritureLib",
                "Debit",
                "Credit"
                )

            dict_col = {
                "JournalCode": {"align": "center"},
                "JournalLib": {"align": "center"},
                "EcritureDate": {"align": "center"},
                "PieceRef": {"align": "center"},
                "CompteNum": {"align": "center"},
                "CompAuxNum": {"align": "center"},
                "CompAuxLib": {"align": "left"},
                "EcritureLib": {"align": "left"},
                "Debit": {"align": "center"},
                "Credit": {"align": "center"}
            }

            invalid_file = self._dir / "InvalidAccounts.xlsx"
            invalid_entries.write_excel(
                workbook=invalid_file,
                table_style="TableStyleMedium2",
                dtype_formats={pl.Date:"dd/mm/yyyy"},
                header_format={"bold":True, "align":"center"},
                column_formats=dict_col,
                float_precision=2,
                include_header=True,
                autofit=True
            )

            msg = "L'export contient des comptes auxiliaires qui ne commencent pas par 'F' ou 'C'.\n\n"
            msg += "Veuillez consulter le fichier 'InvalidAccounts.xlsx',\n"
            msg += f"dans votre dossier {self._dir}"
            run_error(msg)

        return df
