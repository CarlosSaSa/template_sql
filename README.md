# Script to generate sql template from descriptive json file

## Keys allowed
- tables -> array of objects
- audit -> boolean flag
- columns -> array of objects
    - name: column name
    - type: datatype of column
    - required: for required columns
    - primaryKey: for columns that are primary keys
    - identity: just for identities columns
    - maxlength: just for columns that are varchar and has a size of string
    - isFk: flag that indicates if a column is foreign key
    - dependsOn: if the flag is present then represent the parent table
