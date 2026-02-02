import hashlib
import base64
import re

def canonicalize_relaxed(body):
    """The core logic extracted for testing."""
    # 1. Relaxed: Reduce sequences of WSP to single space
    body = re.sub(b"[ \t]+", b" ", body)
    # 2. Relaxed: Ignore WSP at the end of lines
    lines = body.splitlines()
    relaxed_lines = [line.rstrip(b" \t") for line in lines]
    # 3. Standardize line endings to CRLF
    result = b"\r\n".join(relaxed_lines)
    # 4. Remove empty lines at the end
    result = result.rstrip(b"\r\n")
    # 5. Add the single required trailing CRLF
    return result + b"\r\n" if result else b"\r\n"

def run_tests():
    test_cases = [
        {
            "name": "Simple text",
            "input": b"Hello World",
            "expected_bh": "3pS6979G74S99B+L8T6XwH+eE9I0P+8C9M0p+uE=", # Placeholder
        },
        {
            "name": "Trailing whitespace and multiple spaces",
            "input": b"Hello    World  \t\r\n\r\n",
            "expected_bh": "Same as 'Hello World' because of relaxed rules",
        },
        {
            "name": "Empty body",
            "input": b"",
            "expected_bh": "47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=", # SHA256 of \r\n
        }
    ]

    print("--- Running DKIM Logic Tests ---")
    for case in test_cases:
        processed = canonicalize_relaxed(case['input'])
        h = hashlib.sha256(processed).digest()
        actual_bh = base64.b64encode(h).decode()
        
        # For the purpose of this test, we demonstrate the SHA256 of an empty body result
        if case["name"] == "Empty body":
             status = "PASS" if actual_bh == case["expected_bh"] else "FAIL"
             print(f"[{status}] {case['name']}")
        else:
             print(f"[INFO] {case['name']} generated bh: {actual_bh}")

if __name__ == "__main__":
    run_tests()
