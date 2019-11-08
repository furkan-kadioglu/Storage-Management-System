# Storage-Management-System

I tested in a Linux system (specifically Ubuntu 16.04)
```bash
python3 2016400XXX/src/storageManager.py inputFile outputFile
```
`files` directory and `system_catalog.pickle` file are created in current directory after query processing.

## Introduction
The design of a storage management system is the aim of this project. The storage management system must be able to store meta-data and actual data. Actual data composed of files, pages, records. The storage management system must be able to do DLL and DML operations. DLL operations in the system are creating a type, delete a type, list all types. DML operations are creating a record, delete a record, search for a record (by primary key), list all records of a type.
## Constraints & Assumptions
### Constraints
- Data must be stored in multiple pages and pages must contain multiple records for scalability. 
- A file must composed of multiple pages but not all pages can’t be included by only one file.
- A file must be deleted when the file becomes free due to deletions.
- The management system must read a file page by page for scalability.
- Database’s name composed of lower-case letter from ASCII. 
- Fields of a type cannot be altered after creation of the type. 
- Each table has one or more fields.
### Assumptions
- Fields are integers
- Field and type names can be alphanumeric.
- User always enters valid input.
- A disk manager has already existed and it can fetch the necessary pages when addressed. 
- A alphanumeric character is stored as 1 byte by using ASCII.
- A Boolean(1/0) field is stored as 1 bit.
- A Integer field is stored in 32 bits / 4 bytes.
## Storage Structures
### Design Decisions
- Page’s size is up to 1.6KB.
- File’s size is up to 101KB.
- The number of fields a type is up to 20.
- The number of types a database is up to 40.
- Type and field names’ size are up to 128 bytes. 
- The primary key is field-1.
- Dense Index is for index files.

### System Catalog
#### System-Catalog File Header
| name of DB | number of types in the DB |
|:----------:|:--------------------------:|
|128 bytes   |4 bytes                     |

_**Table 1: System-Catalog File Header**_

#### System-Catalog File 
| type name | state | number of fields | field-1 name |field-2 name | ... |field-k name |
|:----------:|:---------:|:----------:|:---------:|:----------:|:---------:|:----------:|
|128 bytes   |1 bit      | 4 bytes| 128 bytes|128 bytes|...|128 bytes|

_**Table 2: Entry of the system-catalog file for k fields**_

- The state indicates that deleted/0 or not/1.
- The size of the system-catalog file is up to (5 + 128 ∗ 20) ∗ 40 ≈ 101KB

### Page Header
| page index | number of records in the page |
|:----------:|:--------------------------:|
|4 bytes   |4 bytes                     |

_**Table 3: Page Header**_

- 2^32 possible page index
### Page
| record-1 | record-2 | ... | record-n |
|:----------:|:---------:|:----------:|:---------:|
|max 80 bytes + 1 bit |max 80 bytes + 1 bit  | ...| max 80 bytes + 1 bit|
| min 33 bits | min 33 bits | ... | min 33 bits |

_**Table 4: Page with n records**_
- Record size up to 80 bytes, because number of fields in a record is up to 20. (20 * 80 bytes ≈ 1.6KB)
### Record Header
| record state |
|:----------:|
|1 bit  |

_**Table 5: Record Header**_
- Record state is deleted/0 or not/1.

### Record
| field-1 (primary key) | field-2 | ... | field-k |
|:----------:|:---------:|:----------:|:---------:|
| 4 bytes | 4 bytes  | ...| 4 bytes|

_**Table 6:Record with k fields**_
- Fields are in 4 bytes, since integer storing.
- Record size is in between 80 byte(20 * 4 bytes + 1 bit) and 33 bits(4 bytes + 1 bit).

### Index File
Dense Index
#### Index File Header
| DB name | type name |
|:----------:|:---------:|
| 128 bytes | 128 bytes  | 

_**Table 7: Index file header**_

#### Entry of Index File
| primary key | page index |
|:----------:|:---------:|
| 128 bytes | 4 bytes  | 

_**Table 8: Entry of an index file**_

## Operations
Operations need to check some conditions belongs to storage structures which are above. When someone wants to create a query for operations, processing the query and validation of the query would be handled separately. I think that query processing details should be handled by regarding encapsulation concept.
### DDL Operations
#### Create a type

```bash
procedure CreateType(database, type)
  catalog = find_catalog(database)
  if catalog = Null then throw ”database does not exist” 
  else
    if is_used(catalog, type) then
      throw ”type name is already used”
    else
      increase num_types(catalog) 
      add entry(catalog, type) 
      create index(database, type)
```

#### Delete a type
```bash
procedure DeleteType(database,type)
  catalog = find_catalog(database)
  if catalog = Null then throw ”database does not exist” 
  else
    if is_used(catalog, type) then 
      decrease num_types(catalog) 
      delete type(catalog, type) 
      delete index(database, type)
    else
      throw ”type does not exist”
```
#### List all types
```bash
procedure ListTypes(database)
  catalog = find_catalog(database_name)
  if catalog = Null then throw ”database does not exist” 
  else
    print types(catalog)
```

### DML Operations
#### Create a record
```bash
procedure CreateRecord(database, type, values) 
  catalog = find_catalog(database)
  if catalog = Null then throw ”database does not exist” 
  else
    if is_used(catalog, type) then
      if is_valid_values(type, values) then
          insert(database, type, values) 
        else
          throw ”invalid input for this type” 
        else
          throw ”type does not exist”
```
#### Search for a record (by primary key)
```bash
procedure SearchRecord(database,type,key)
  catalog = find_catalog(database)
  if catalog = Null then throw ”database does not exist” 
  else
    if is_used(catalog, type) then
      record = get_key(database, type, key) 
      if record = Null then
        throw ”key does not exist” 
        else
          return record 
    else
      throw ”type does not exist”
```
#### Delete a record
```bash
procedure DeleteRecord(database,type,key)
  catalog = find_catalog(database)
   if catalog = Null then throw ”database does not exist” 
   else
    if is_used(catalog, type) then
      record = get key(database, type, key) 
      if record  ̸= Null then
        delete(database, type, key)
    else
      throw ”type does not exist”
```
#### Update a record
```bash
procedure UpdateRecord(database,type,key)
  catalog = find_catalog(database)
  if catalog = Null then throw ”database does not exist” 
  else
    if is_used(catalog, type) then
      record = get_key(database, type, key) 
      if record ̸= Null then
        update(database, type, key) 
    else
      throw ”type does not exist”
```
#### List all records of a type
```bash
procedure ListRecords(database,type)
  catalog = find_catalog(database)
  if catalog = Null then throw ”database does not exist” 
  else
    if is_used(catalog, type) then
      return get_record_list(catalog, type)
    else
      throw ”type does not exist”
```
## Conclusions & Assesment
In this project, I have designed a storage management system. I have written pseudo-code for operations supported by the management system. Maybe the storage manager system can support more operations like as update. Other downward is primary key selection. On the other hand, simple is good. Overall, the storage management system is sufficient to learn database.
