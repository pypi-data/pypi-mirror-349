import subprocess
import os
import tempfile
from .ExtractorStrategy import ExtractorStrategy
from ...Logging import Debug

class NetezzaExtractor(ExtractorStrategy):
    """Handles extraction from Netezza specifically."""
    
    def build_table_query(self, fully_qualified_table_name: str, output_path: str, verbose: bool = False)->str:
        """ Extracts tablestrucutre and builds a query to correctly extract data from the table.
        Args:
            fully_qualified_table_name (str): The fully qualified table name in the format database.schema.table.
            verbose (bool): If True, enables verbose logging.

        Returns:
            Query (str): Complete query string to extract data from the table.
        """


        database, _, table = fully_qualified_table_name.split('.')
        file_path = os.path.join(output_path, f"{table}_structure.txt")
        
        try:
            structure_query = f"SELECT column_name, CASE WHEN DATA_TYPE LIKE '%CHAR%' OR DATA_TYPE LIKE '%TEXT%' OR DATA_TYPE LIKE '%NAME%' then 'CHAR' else DATA_TYPE END as TYPE FROM {database}.information_schema.columns where TABLE_CATALOG LIKE '{database}' AND table_name = '{table}' order by ordinal_position;"
            
            nzsql_command = f"""$NZ_HOME/nzsql -c "{structure_query}"  > {file_path}"""

            Debug.log(f"Running command: {nzsql_command}", 'DEBUG', verbose)
            subprocess.run(nzsql_command, shell=True, check=True)

        except Exception as e:
            Debug.log(f"Error extracting table structure: {e}", 'ERROR')
            return ''
        
        finally:
            Debug.log(f"Table structure for {fully_qualified_table_name} extracted successfully.", 'DEBUG', verbose)


        try: 
            with open(file_path, 'r') as f:
                lines = f.readlines()[2:]  # Skip the first two lines and the last line
                structure = [line.strip() for line in lines if line.strip()]
            
            Debug.log(f"Table structure: {structure}", 'WARNING', verbose)

            column_list = []
            
            for i, line in enumerate(structure):
                parts = line.split('|')
                
                if len(parts) < 2:
                    continue

                name = parts[0].strip()
                data_type = parts[1].strip()

                if data_type == 'CHAR':
                    column_expr = f""" '"' || REPLACE(REPLACE ({name},'\','\\'),'"','\"') || '"' as {name} """
                else:
                    column_expr = name

                column_list.append(column_expr)

            columns_str = ', '.join(column_list)
            
            altered_query = f"SELECT {columns_str} FROM {fully_qualified_table_name}"

            Debug.log(f"############ \nExtracted query: {altered_query} \n############", 'WARNING', verbose)
            
            return altered_query

        except FileNotFoundError:
            Debug.log(f"File {table}_structure.txt not found.", 'ERROR')
            return ''
        except Exception as e:
            Debug.log(f"Error reading file {table}_structure.txt: {e}", 'ERROR')
            return ''
        
    def extract_table_query(self, fully_qualified_table_name: str, filter_column: str = None, filter_value: str = None, verbose: bool = False)->str:
        """Build query against database table. (Can be extended in a future version)."""
        
        if filter_column is not None and filter_value is None:
            Debug.log(f"You must provide a filter value in order to apply any filtering.", 'WARNING')
            raise Exception
        
        elif filter_column is None and filter_value is not None:
            Debug.log(f"You cannot supply a filter value without specifying a filter (--filter option)\ncontinuing without filter.", 'WARNING')
            raise Exception
        
        if filter_value is None or filter_column is None:
            query = f"SELECT * FROM {fully_qualified_table_name}"
        else:
            query = f"SELECT * FROM {fully_qualified_table_name} WHERE {filter_column} BETWEEN TO_DATE('{filter_value}', 'DD.MM.YYYY') AND CURRENT_DATE+1"
        
        return query

    def list_all_tables(self, database_name: str, verbose: bool = False)->list:
        """Query all tables in the specified database and export them as an array."""
        
        command = f"nzsql -q -c \"SELECT TABLE_NAME FROM _V_TABLE WHERE TABLE_SCHEMA = '{database_name}';\""
        output = subprocess.check_output(command, shell=True).decode('ISO-8859-1')
        table_list = [line.strip() for line in output.split('\n') if line.strip()]

        return table_list

    def export_external_table(self, output_path: str, fully_qualified_table_name: str, filter_column: str = None, filter_value: str = None, verbose: bool = False) -> tuple:
        """Runs the query on Netezza and exports the data to a CSV file.
        Requires NZ_HOME, NZ_USER, NZ_PASSWORD and NZ_DATABASE environment variables to be set."""

        table_name = fully_qualified_table_name.split('.')[-1] if fully_qualified_table_name else None
        query = self.build_table_query(fully_qualified_table_name, output_path, verbose)

        os.makedirs(output_path, exist_ok=True)
        exported_csv_file = os.path.join(output_path, f"{table_name}_full.csv")        

        external_table_query = f"""
        CREATE EXTERNAL TABLE '{exported_csv_file}' 
        USING (
            REMOTESOURCE 'NZSQL'
            delimiter '|'
            escapeChar '\\'
            QuotedValue 'DOUBLE'
            RequireQuotes 'true'
            nullValue 'NULL'
            encoding 'internal'
        )
        AS {query};
        """

        try:
            # Write the query to a temp .sql file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_sql_file:
                temp_sql_file.write(external_table_query)
                temp_sql_path = temp_sql_file.name

            nzsql_command = f"$NZ_HOME/nzsql -f {temp_sql_path}"

            Debug.log(f"Running Netezza SQL script via: {nzsql_command}", 'DEBUG', verbose)
            subprocess.run(nzsql_command, shell=True, check=True)

            # Optionally re-encode file after export (if needed)
            #encoding_command = f"iconv -f ISO-8859-1 -t UTF-8 {exported_csv_file} -o {exported_csv_file}"
            #Debug.log(f"Running encoding conversion: {encoding_command}", 'DEBUG', verbose)
            #subprocess.run(encoding_command, shell=True, check=True)

        except subprocess.CalledProcessError as e:
            Debug.log(f"Error executing Netezza command: {e}", 'ERROR')
            return None, None

        header = "ddd"  # Replace or extract real header if needed
        return header, exported_csv_file

    