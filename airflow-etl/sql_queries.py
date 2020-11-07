drop_query = "DROP TABLE IF EXISTS covid_data_tb"

table_columns = ['@type', 'accessLevel', 'bureauCode', 'description', 'distribution',
                 'identifier', 'issued', 'keyword', 'landingPage', 'modified',
                 'programCode', 'theme', 'title', 'contactPoint.fn',
                 'contactPoint.hasEmail', 'publisher.@type', 'publisher.name',
                 'describedBy', 'references', 'accrualPeriodicity', 'temporal',
                 'dataQuality', 'license', 'describedByType', 'rights', 'language']

column_query = ["{} string".format(column_name) for column_name in table_columns]

create_query = """CREATE TABLE IF NOT EXISTS covid_data_tb ({})""".format(", \n".join(column_query))
