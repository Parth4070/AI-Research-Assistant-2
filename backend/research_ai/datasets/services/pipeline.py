from .cleaning import *

class DataCleaningPipeline:

    def run(self, df):

        report = {}

        df, duplicates = remove_duplicates(df)

        report["duplicates_removed"] = duplicates

        df, missing = impute_values(df)

        report["missing_values_filled"] = missing

        return df, report

import os


def generate_clean_filename(dataset):

    filename = os.path.basename(dataset.file.name)

    name, extension = os.path.splitext(filename)

    return f"{name}_clean{extension}"