# import random
# import hashlib

# def random_hex_digit():
#     """Helper to generate a random hexadecimal digit."""
#     return f"{random.randint(0, 15):x}"

# def random_decimal_digit():
#     """Generate a random decimal digit."""
#     return str(random.randint(0, 9))

# def generate_uuid1():
#     """Generate a UUID with version 1, ensuring the correct UUID structure."""
#     part1 = ''.join([random_hex_digit() for _ in range(8)])
#     part2 = ''.join([random_hex_digit() for _ in range(4)])
#     part3 = '1' + ''.join([random_hex_digit() for _ in range(3)])  # Version 1 identifier
#     part4 = ''.join([random_hex_digit() for _ in range(4)])
#     part5 = ''.join([random_hex_digit() for _ in range(12)])
#     return f"{part1}-{part2}-{part3}-{part4}-{part5}"

# def generate_uuid4():
#     """Generate a UUID with version 4, ensuring the correct UUID structure."""
#     part1 = ''.join([random_hex_digit() for _ in range(8)])
#     part2 = ''.join([random_hex_digit() for _ in range(4)])
#     part3 = '4' + ''.join([random_hex_digit() for _ in range(3)])  # Version 4 identifier
#     part4 = ''.join([random_hex_digit() for _ in range(4)])
#     part5 = ''.join([random_hex_digit() for _ in range(12)])
#     return f"{part1}-{part2}-{part3}-{part4}-{part5}"

# def generate_uuid7():
#     """Generate a UUID with version 7, ensuring the correct UUID structure."""
#     part1 = ''.join([random_hex_digit() for _ in range(8)])
#     part2 = ''.join([random_hex_digit() for _ in range(4)])
#     part3 = '7' + ''.join([random_hex_digit() for _ in range(3)])  # Version 7 identifier
#     part4 = ''.join([random_hex_digit() for _ in range(4)])
#     part5 = ''.join([random_hex_digit() for _ in range(12)])
#     return f"{part1}-{part2}-{part3}-{part4}-{part5}"

# def generate_nil_uuid():
#     """Generate a nil UUID."""
#     return '00000000-0000-0000-0000-000000000000'

# def generate_guid():
#     """Generate a UUID with version 4, ensuring the correct UUID structure."""
#     part1 = ''.join([random_hex_digit() for _ in range(8)])
#     part2 = ''.join([random_hex_digit() for _ in range(4)])
#     part3 = ''.join([random_hex_digit() for _ in range(4)])
#     part4 = ''.join([random_hex_digit() for _ in range(4)])
#     part5 = ''.join([random_hex_digit() for _ in range(12)])
#     return f"{part1}-{part2}-{part3}-{part4}-{part5}"

# def generate_multiple_uuids(version, count):
#     """Generate multiple UUIDs for a specified version."""
#     if count < 2 or count > 50:
#         raise ValueError("Count must be between 2 and 50.")
#     generator = {
#         1: generate_uuid1,
#         4: generate_uuid4,
#         7: generate_uuid7,
#     }.get(version)

#     if not generator:
#         raise ValueError("Unsupported version.")
#     return [generator() for _ in range(count)]

# def generate_uuid_for_email(email):
#     """Generate a consistent UUID-like string based on an email."""
#     if not isinstance(email, str) or not email:
#         raise ValueError("Please provide a valid email address.")
#     return email_to_uuid(email)

# def email_to_uuid(email):
#     """Convert an email to a UUID-like format using hashing."""
#     email_hash = hashlib.md5(email.encode()).hexdigest()
#     return f"{email_hash[:8]}-{email_hash[8:12]}-4{email_hash[12:15]}-{email_hash[15:19]}-{email_hash[19:32]}"

# def generate_custom_uuid(pattern: str, segment_length: int, static_prefix: str = ""):
#     """
#     Generate a custom UUID-like string based on a user-defined pattern and segment length.

#     :param pattern: A string defining the pattern (e.g., 'xxxx-xxxx-xxxx').
#                     Use 'x' for random hex digits and 'd' for random decimal digits.
#     :param segment_length: The length of each segment defined by the user.
#     :param static_prefix: A static string to prepend to the generated UUID.
#     :return: A custom UUID-like string.
#     """
#     result = []

#     # Split the pattern by the separator '-'
#     segments = pattern.split('-')

#     for segment in segments:
#         segment_result = ""
#         for char in segment:
#             if char == 'x':
#                 segment_result += random_hex_digit()
#             elif char == 'd':
#                 segment_result += random_decimal_digit()
#             else:
#                 segment_result += char  # Static characters stay the same

#         # Ensure the segment matches the desired segment length
#         if len(segment_result) < segment_length:
#             segment_result += ''.join(random_hex_digit() for _ in range(segment_length - len(segment_result)))

#         result.append(segment_result[:segment_length])  # Trim to segment length

#     return f"{static_prefix}-{'-'.join(result)}" if static_prefix else '-'.join(result)






# import secrets
# import time
# import os
# import hashlib
# import random
# import threading

# _lock = threading.Lock()

# # Simulate MAC address (6 bytes, 48 bits)
# def get_node_identifier():
#     return secrets.token_bytes(6)

# # Simulated clock sequence (14 bits)
# _clock_seq = secrets.randbits(14)

# # Time-based UUID v1 (60-bit timestamp, 48-bit node, 14-bit clock_seq)
# def generate_uuid1():
#     global _clock_seq

#     with _lock:
#         timestamp = int((time.time() + 12219292800) * 1e7)  # 100ns intervals since UUID epoch
#         time_low = timestamp & 0xFFFFFFFF
#         time_mid = (timestamp >> 32) & 0xFFFF
#         time_hi_and_version = ((timestamp >> 48) & 0x0FFF) | (1 << 12)

#         clock_seq_low = _clock_seq & 0xFF
#         clock_seq_hi_and_reserved = (_clock_seq >> 8) & 0x3F
#         clock_seq_hi_and_reserved |= 0x80  # RFC reserved bits

#         node = get_node_identifier()
#         fields = [
#             f"{time_low:08x}",
#             f"{time_mid:04x}",
#             f"{time_hi_and_version:04x}",
#             f"{clock_seq_hi_and_reserved:02x}{clock_seq_low:02x}",
#             node.hex()
#         ]
#         return "-".join(fields)

# # UUID v4 (pure randomness, 122 random bits)
# def generate_uuid4():
#     rand_bytes = secrets.token_bytes(16)
#     rand_bytes = bytearray(rand_bytes)
#     rand_bytes[6] = (rand_bytes[6] & 0x0F) | 0x40  # version 4
#     rand_bytes[8] = (rand_bytes[8] & 0x3F) | 0x80  # variant bits

#     return f"{rand_bytes[0:4].hex()}-{rand_bytes[4:6].hex()}-{rand_bytes[6:8].hex()}-{rand_bytes[8:10].hex()}-{rand_bytes[10:16].hex()}"

# # UUID v7 (time-ordered + randomness, newer format)
# def generate_uuid7():
#     unix_ts_ms = int(time.time() * 1000)
#     ts_bytes = unix_ts_ms.to_bytes(6, 'big')

#     rand_bytes = secrets.token_bytes(10)
#     uuid_bytes = bytearray(ts_bytes + rand_bytes)

#     uuid_bytes[6] = (uuid_bytes[6] & 0x0F) | 0x70  # version 7
#     uuid_bytes[8] = (uuid_bytes[8] & 0x3F) | 0x80  # variant

#     return f"{uuid_bytes[0:4].hex()}-{uuid_bytes[4:6].hex()}-{uuid_bytes[6:8].hex()}-{uuid_bytes[8:10].hex()}-{uuid_bytes[10:16].hex()}"

# # Nil UUID (all zero)
# def nil_uuid():
#     return "00000000-0000-0000-0000-000000000000"

# # GUID alias
# def generate_guid():
#     return generate_uuid4()

# # UUID for email (SHA-256 instead of MD5)
# def custom_uuid_from_email(email):
#     hash_val = hashlib.sha256(email.encode()).hexdigest()
#     return f"{hash_val[:8]}-{hash_val[8:12]}-4{hash_val[12:15]}-{hash_val[15:19]}-{hash_val[19:31]}"

# # UUID for email Validation
# def validate_uuid_for_email(uuid_str: str, email: str) -> bool:
#     """
#     Validate if the given UUID string matches the UUID generated from the provided email.

#     Args:
#         uuid_str: The UUID string to validate.
#         email: The email to generate UUID from.

#     Returns:
#         True if the UUID matches the email-derived UUID, False otherwise.
#     """
#     try:
#         expected_uuid = custom_uuid_from_email(email)
#     except Exception:
#         return False
#     return uuid_str.lower() == expected_uuid.lower()


# # Custom user-defined pattern UUID
# def custom_uuid_pattern(pattern: str):
#     """
#     Example: pattern = "xxxx-xxxx-xxxx"
#     """
#     result = []
#     for char in pattern:
#         if char == 'x':
#             result.append(secrets.choice("0123456789abcdef"))
#         elif char == '-':
#             result.append('-')
#         else:
#             result.append(char)
#     return ''.join(result)

# # Generate multiple UUIDs securely
# def generate_batch(version, count):
#     if version == 1:
#         fn = generate_uuid1
#     elif version == 4:
#         fn = generate_uuid4
#     elif version == 7:
#         fn = generate_uuid7
#     else:
#         raise ValueError("Unsupported version.")

#     return [fn() for _ in range(count)]





# import secrets
# import time
# import hashlib
# import threading

# # Thread-safe locking for UUIDv1
# _lock = threading.Lock()
# _clock_seq = secrets.randbits(14)  # 14-bit clock sequence

# # MAC-like Node ID (48-bit)
# def _get_node_id():
#     return secrets.token_bytes(6)

# # UUIDv1: Time-based UUID (60-bit timestamp + 14-bit clock sequence + 48-bit node)
# def generate_uuid1():
#     global _clock_seq

#     with _lock:
#         timestamp = int((time.time() + 12219292800) * 1e7)  # 100ns since UUID epoch
#         time_low = timestamp & 0xFFFFFFFF
#         time_mid = (timestamp >> 32) & 0xFFFF
#         time_hi_and_version = ((timestamp >> 48) & 0x0FFF) | (1 << 12)  # version 1

#         clock_seq_low = _clock_seq & 0xFF
#         clock_seq_hi = (_clock_seq >> 8) & 0x3F
#         clock_seq_hi |= 0x80  # variant bits

#         node = _get_node_id()

#         return f"{time_low:08x}-{time_mid:04x}-{time_hi_and_version:04x}-{clock_seq_hi:02x}{clock_seq_low:02x}-{node.hex()}"

# # UUIDv4: Random-based UUID
# def generate_uuid4():
#     rand = bytearray(secrets.token_bytes(16))
#     rand[6] = (rand[6] & 0x0F) | 0x40  # version 4
#     rand[8] = (rand[8] & 0x3F) | 0x80  # variant
#     return f"{rand[0:4].hex()}-{rand[4:6].hex()}-{rand[6:8].hex()}-{rand[8:10].hex()}-{rand[10:].hex()}"

# # UUIDv7: Unix timestamp in ms + randomness
# def generate_uuid7():
#     unix_ms = int(time.time() * 1000)
#     ts_bytes = unix_ms.to_bytes(6, 'big')
#     rand = secrets.token_bytes(10)
#     uuid_bytes = bytearray(ts_bytes + rand)
#     uuid_bytes[6] = (uuid_bytes[6] & 0x0F) | 0x70  # version 7
#     uuid_bytes[8] = (uuid_bytes[8] & 0x3F) | 0x80  # variant
#     return f"{uuid_bytes[0:4].hex()}-{uuid_bytes[4:6].hex()}-{uuid_bytes[6:8].hex()}-{uuid_bytes[8:10].hex()}-{uuid_bytes[10:].hex()}"

# # Nil UUID (all zeros)
# def generate_nil_uuid():
#     return "00000000-0000-0000-0000-000000000000"

# # GUID is the same as UUIDv4 in many implementations
# def generate_guid():
#     return generate_uuid4()

# # UUID based on email using SHA-256 (more secure than MD5)
# def generate_uuid_for_email(email: str):
#     if not isinstance(email, str) or not email:
#         raise ValueError("Invalid email provided.")
#     hash_val = hashlib.sha256(email.encode()).hexdigest()
#     return f"{hash_val[:8]}-{hash_val[8:12]}-4{hash_val[12:15]}-{hash_val[15:19]}-{hash_val[19:31]}"

# # Validate UUID against email
# def validate_uuid_for_email(uuid_str: str, email: str):
#     try:
#         return uuid_str.lower() == generate_uuid_for_email(email).lower()
#     except Exception:
#         return False

# # Custom pattern-based UUID
# def generate_custom_uuid(pattern: str):
#     """
#     Example: pattern='xxxx-dddd-xxxx' (x: hex, d: decimal)
#     """
#     output = []
#     for ch in pattern:
#         if ch == 'x':
#             output.append(secrets.choice('0123456789abcdef'))
#         elif ch == 'd':
#             output.append(secrets.choice('0123456789'))
#         else:
#             output.append(ch)
#     return ''.join(output)

# # Generate multiple UUIDs
# def generate_multiple_uuids(version: int, count: int):
#     if not (2 <= count <= 50):
#         raise ValueError("Count must be between 2 and 50.")
#     gen_map = {
#         1: generate_uuid1,
#         4: generate_uuid4,
#         7: generate_uuid7
#     }
#     if version not in gen_map:
#         raise ValueError("Unsupported version. Choose 1, 4, or 7.")
#     return [gen_map[version]() for _ in range(count)]



import secrets
import time
import hashlib
import threading
import os

# Global thread lock for UUIDv1 clock sequence safety
_lock = threading.Lock()
_clock_seq = secrets.randbits(14)  # 14-bit random clock sequence
_last_timestamp = 0

# One-time generated 48-bit Node ID to simulate MAC (stable for the run)
_node_id = secrets.token_bytes(6)

def _get_node_id():
    return _node_id

def _get_uuid_timestamp():
    """Return timestamp in 100-ns intervals since UUID epoch."""
    return int((time.time() + 12219292800) * 1e7)

# UUIDv1: Time-based UUID (with clock sequence and node ID)
def generate_uuid1():
    global _clock_seq, _last_timestamp

    with _lock:
        timestamp = _get_uuid_timestamp()

        if timestamp <= _last_timestamp:
            _clock_seq = (_clock_seq + 1) & 0x3FFF  # Increment clock_seq if time doesn't advance
        _last_timestamp = timestamp

        time_low = timestamp & 0xFFFFFFFF
        time_mid = (timestamp >> 32) & 0xFFFF
        time_hi_and_version = ((timestamp >> 48) & 0x0FFF) | (1 << 12)  # version 1

        clock_seq_low = _clock_seq & 0xFF
        clock_seq_hi = (_clock_seq >> 8) & 0x3F
        clock_seq_hi |= 0x80  # variant

        node = _get_node_id()

        return f"{time_low:08x}-{time_mid:04x}-{time_hi_and_version:04x}-{clock_seq_hi:02x}{clock_seq_low:02x}-{node.hex()}"

# UUIDv4: Random-based UUID
def generate_uuid4():
    rand = bytearray(secrets.token_bytes(16))
    rand[6] = (rand[6] & 0x0F) | 0x40  # version 4
    rand[8] = (rand[8] & 0x3F) | 0x80  # variant
    return f"{rand[0:4].hex()}-{rand[4:6].hex()}-{rand[6:8].hex()}-{rand[8:10].hex()}-{rand[10:].hex()}"

# UUIDv7: Unix timestamp in milliseconds + randomness
def generate_uuid7():
    unix_ms = int(time.time() * 1000)
    ts_bytes = unix_ms.to_bytes(6, 'big')
    rand = secrets.token_bytes(10)
    uuid_bytes = bytearray(ts_bytes + rand)
    uuid_bytes[6] = (uuid_bytes[6] & 0x0F) | 0x70  # version 7
    uuid_bytes[8] = (uuid_bytes[8] & 0x3F) | 0x80  # variant
    return f"{uuid_bytes[0:4].hex()}-{uuid_bytes[4:6].hex()}-{uuid_bytes[6:8].hex()}-{uuid_bytes[8:10].hex()}-{uuid_bytes[10:].hex()}"

# Nil UUID (all zeros)
def generate_nil_uuid():
    return "00000000-0000-0000-0000-000000000000"

# GUID (same as UUIDv4 in many platforms)
def generate_guid():
    return generate_uuid4()

# UUID based on email using SHA-256 (UUIDv5-like approach)
def generate_uuid_for_email(email: str):
    """
    Generates a deterministic UUID from email using SHA-256.
    """
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Invalid email provided.")

    namespace = b"urn:uuid:email"
    hash_bytes = hashlib.sha256(namespace + email.encode('utf-8')).digest()

    uuid_bytes = bytearray(hash_bytes[:16])
    uuid_bytes[6] = (uuid_bytes[6] & 0x0F) | 0x50  # fake version 5 using SHA-256
    uuid_bytes[8] = (uuid_bytes[8] & 0x3F) | 0x80  # variant

    return f"{uuid_bytes[0:4].hex()}-{uuid_bytes[4:6].hex()}-{uuid_bytes[6:8].hex()}-{uuid_bytes[8:10].hex()}-{uuid_bytes[10:].hex()}"

# Validate UUID against email
def validate_uuid_for_email(uuid_str: str, email: str):
    try:
        return uuid_str.lower() == generate_uuid_for_email(email).lower()
    except Exception:
        return False

# Custom pattern-based UUID
def generate_custom_uuid(pattern: str):
    """
    Example: pattern='xxxx-dddd-xxxx' (x: hex, d: digit)
    """
    output = []
    for ch in pattern:
        if ch == 'x':
            output.append(secrets.choice('0123456789abcdef'))
        elif ch == 'd':
            output.append(secrets.choice('0123456789'))
        else:
            output.append(ch)
    return ''.join(output)

# Generate multiple UUIDs of given version
def generate_multiple_uuids(version: int, count: int):
    if not (2 <= count <= 50):
        raise ValueError("Count must be between 2 and 50.")
    gen_map = {
        1: generate_uuid1,
        4: generate_uuid4,
        7: generate_uuid7
    }
    if version not in gen_map:
        raise ValueError("Unsupported version. Choose 1, 4, or 7.")
    return [gen_map[version]() for _ in range(count)]
