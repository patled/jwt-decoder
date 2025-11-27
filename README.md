# JWT Decoder CLI Tool

A simple CLI tool to decode JWT tokens without verification. The tool shows the header and payload information of a JWT token in a readable format.

## Features

- Decodes JWT tokens without verification (only base64 decoding)
- Supports tokens as command line argument or over stdin
- Two output formats: JSON and readable format
- No external dependencies (uses only Python standard libraries)
- Error handling for invalid tokens

## Installation

### Install as Python package

If you're using a virtual environment (recommended), activate it first:

```bash
# Activate virtual environment (if you have one)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### Run

```bash
python jwt_decoder.py <token>
```

Or make the file executable:

```bash
chmod +x jwt_decoder.py
./jwt_decoder.py <token>
```

## Usage

### Basic usage

```bash
jwt-decoder eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Pass token over stdin

```bash
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." | jwt-decoder
```

### JSON output format

```bash
jwt-decoder --format json <token>
```

or

```bash
jwt-decoder -f json <token>
```

## Output formats

### Pretty Format (Standard)

The default format shows header, payload and signature separated and formatted:

```text
================================================================================
JWT TOKEN - DECODED
================================================================================

HEADER:
--------------------------------------------------------------------------------
{
  "alg": "HS256",
  "typ": "JWT"
}

PAYLOAD:
--------------------------------------------------------------------------------
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}

SIGNATURE:
--------------------------------------------------------------------------------
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
================================================================================
```

### JSON Format

With `--format json` the output is formatted as structured JSON:

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "1234567890",
    "name": "John Doe",
    "iat": 1516239022
  },
  "signature": "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

## Example token

You can test the tool with this example token:

```bash
jwt-decoder eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

## Error handling

The tool gives informative error messages when:

- The token does not have the expected format (3 parts separated by dots)
- The Base64 decoding fails
- The JSON content is invalid

## Requirements

- Python 3.7 or higher
- rich library

## Notes

- **Important**: This tool **does not verify signatures**. It only decodes the Base64 encoded parts of the token.
- For production environments, you should always verify the signature of the token before trusting the content.

## License

MIT License
