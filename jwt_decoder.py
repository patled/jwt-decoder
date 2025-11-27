#!/usr/bin/env python3
"""
JWT Decoder CLI Tool

A Command-Line-Tool to decode JWT tokens without verification.
"""

import argparse
import base64
import json
import sys
from typing import Dict, Any, Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def decode_base64url(data: str) -> bytes:
    """Decodes Base64URL encoded data."""
    # Base64URL uses '-' instead of '+' and '_' instead of '/'
    # Padding is removed, but must be added again
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    data = data.replace('-', '+').replace('_', '/')
    return base64.b64decode(data)


def decode_jwt(token: str) -> Dict[str, Any]:
    """
    Decodes a JWT token and returns header and payload.

    Args:
        token: The JWT token as a string

    Returns:
        Dictionary with 'header' and 'payload' keys

    Raises:
        ValueError: If the token is invalid
    """
    parts = token.split('.')

    if len(parts) != 3:
        raise ValueError(
            "Invalid JWT token: A JWT must consist of 3 parts (Header.Payload.Signature)")

    header_b64, payload_b64, signature_b64 = parts

    try:
        # Decode header
        header_bytes = decode_base64url(header_b64)
        header = json.loads(header_bytes.decode('utf-8'))

        # Decode payload
        payload_bytes = decode_base64url(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))

        return {
            'header': header,
            'payload': payload,
            'signature': signature_b64  # Signature remains Base64URL encoded
        }
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")
    except Exception as e:
        raise ValueError(f"Error decoding token: {e}")


def format_pretty(decoded: Dict[str, Any], fancy: bool = True) -> str:
    """Formats the decoded data in a readable format."""
    if fancy and RICH_AVAILABLE:
        return format_pretty_fancy(decoded)

    # Fallback to plain text format
    output = []
    output.append("=" * 80)
    output.append("JWT TOKEN - DECODED")
    output.append("=" * 80)
    output.append("")

    output.append("HEADER:")
    output.append("-" * 80)
    output.append(json.dumps(decoded['header'], indent=2, ensure_ascii=False))
    output.append("")

    output.append("PAYLOAD:")
    output.append("-" * 80)
    output.append(json.dumps(decoded['payload'], indent=2, ensure_ascii=False))
    output.append("")

    output.append("SIGNATURE:")
    output.append("-" * 80)
    output.append(decoded['signature'])
    output.append("")
    output.append("=" * 80)

    return "\n".join(output)


def format_pretty_fancy(decoded: Dict[str, Any]) -> str:
    """Formats the decoded data with rich formatting."""
    console = Console()

    # Create panels for each section
    header_json = json.dumps(decoded['header'], indent=2, ensure_ascii=False)
    payload_json = json.dumps(decoded['payload'], indent=2, ensure_ascii=False)

    header_syntax = Syntax(header_json, "json",
                           theme="monokai", line_numbers=False)
    payload_syntax = Syntax(payload_json, "json",
                            theme="monokai", line_numbers=False)

    # Create output
    output_parts = []

    # Title
    title = Text("JWT TOKEN - DECODED", style="bold bright_cyan")
    output_parts.append(
        Panel(title, border_style="bright_cyan", padding=(1, 2)))
    output_parts.append("")

    # Header section
    header_panel = Panel(
        header_syntax,
        title="[bold bright_yellow]HEADER[/bold bright_yellow]",
        border_style="bright_yellow",
        padding=(1, 2)
    )
    output_parts.append(header_panel)
    output_parts.append("")

    # Payload section
    payload_panel = Panel(
        payload_syntax,
        title="[bold bright_green]PAYLOAD[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 2)
    )
    output_parts.append(payload_panel)
    output_parts.append("")

    # Signature section
    signature_panel = Panel(
        decoded['signature'],
        title="[bold bright_magenta]SIGNATURE[/bold bright_magenta]",
        border_style="bright_magenta",
        padding=(1, 2)
    )
    output_parts.append(signature_panel)

    # Render to string
    with console.capture() as capture:
        for part in output_parts:
            console.print(part)

    return capture.get()


def format_json(decoded: Dict[str, Any]) -> str:
    """Formats the decoded data as JSON."""
    return json.dumps(decoded, indent=2, ensure_ascii=False)


def main():
    """Main function for the CLI tool."""
    parser = argparse.ArgumentParser(
        description='Decodes a JWT token and shows header and payload.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
  
  echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." | %(prog)s
  
  %(prog)s --format json eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        """
    )

    parser.add_argument(
        'token',
        nargs='?',
        help='The JWT token to decode (optional, can also be passed over stdin)'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['json', 'pretty'],
        default='pretty',
        help='Output format: json or pretty (default: pretty)'
    )

    parser.add_argument(
        '--no-fancy',
        dest='fancy',
        action='store_false',
        default=True,
        help='Disable fancy colored output (default: fancy output enabled)'
    )

    args = parser.parse_args()

    # Read token from argument or stdin
    token: Optional[str] = args.token

    if not token:
        # Try to read from stdin
        if sys.stdin.isatty():
            parser.error(
                "No token provided. Please provide token as argument or over stdin.")
        token = sys.stdin.read().strip()

    if not token:
        parser.error("No token found.")

    try:
        # Decode the token
        decoded = decode_jwt(token)

        # Format the output
        if args.format == 'json':
            output = format_json(decoded)
        else:
            output = format_pretty(decoded, fancy=args.fancy)

        print(output)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
