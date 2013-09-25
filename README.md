# Caper
Extensible Python filename parsing library

## Development

_How do I, as a developer, start working on the project?_ 

1. _What dependencies does it have (where are they expressed) and how do I install them?_
2. _How can I see the project working before I change anything?_

## Testing

### Unit Tests
*Requires pytest*

1. `py.test`

### Name Tester
*tools/run_tests.py*

1. Create a name database at `tools/<parser_name>.csv` *(see example below)*
2. Run `tools/run_tests.py` - defaults to interactive input mode, command line arguments are available as well *(see below)*

#### Arguments

    run_tests.py [parser_type] [test_file] [logging_mode] [start]
    
    parser_type   --  (scene, anime, etc..)
    test_file     --  file to load for testing (defaults to <parser_type>.csv if it exists)
    logging_mode  --  debug or info (defaults to info)
    start         --  0-based index of first name to test (defaults to 0)

#### Example

    name[,another_column,...]
    [...]
    <name>[,<another_value>,...]
    [...]

 - **Header is required**
 - **Only the *name* column is required, other columns are ignored**

## Contributing

- _Pull request guidelines_

## License
