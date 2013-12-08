# Caper 
[![](https://travis-ci.org/fuzeman/Caper.png?branch=master)](https://travis-ci.org/fuzeman/Caper)
[![](https://coveralls.io/repos/fuzeman/Caper/badge.png?branch=master)](https://coveralls.io/r/fuzeman/Caper?branch=master)

Extensible filename parsing library for Python

## Development

### Requirements

**Python:** versions 2.6 - 3.3 supported

    Logr>=0.2.2

## Testing

### Unit Tests

1. Run `py.test`

### Name Tester
*(tools/run_tests.py)*

1. Create a name database at `tools/<parser_name>.csv` *(see example below)*
2. Run `tools/run_tests.py` - defaults to interactive mode, command line arguments are available *(see below)*

#### Arguments

    run_tests.py [parser_type] [test_file] [logging_mode] [start]
    
    parser_type   --  Type of parser to run (scene, anime, ...)
    test_file     --  File to use for testing [defaults to <parser_type>.csv if it exists]
    logging_mode  --  Logging mode to use (debug or info) [defaults to info]
    start         --  0-based index of first name to test [defaults to 0]

#### Example Name Database

    name[,another_column,...]
    [...]
    <name>[,<another_value>,...]
    [...]

 - **Header is required**
 - **Only the "name" column is required, other columns are ignored**

## Contributing

Pull requests, bug reports and enhancement requests are welcome.

Feel free to contact me if you have any questions.

## Contact

**IRC:** fuzeman on freenode  
**Email:** fuzeman91@gmail.com

## License

    # Copyright 2013 Dean Gardiner <gardiner91@gmail.com>
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    # http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
