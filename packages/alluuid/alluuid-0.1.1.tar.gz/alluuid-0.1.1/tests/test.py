from alluuid import (
    generate_uuid1,
    generate_uuid4,
    generate_uuid7,
    generate_nil_uuid,
    generate_guid,
    generate_uuid_for_email,
    validate_uuid_for_email,
    generate_custom_uuid,
    generate_multiple_uuids

)

# def test_generate_uuid1():
#     uuid1 = generate_uuid1()
#     print("Generated UUID1:", uuid1)

# def test_generate_uuid4():
#     uuid4 = generate_uuid4()
#     print("Generated UUID4:", uuid4)

# def test_generate_uuid7():
#     uuid7 = generate_uuid7()
#     print("Generated UUID7:", uuid7)

# def test_generate_multiple_uuids():
#     try:
#         uuids = generate_multiple_uuids(4, 5)
#         print("Generated Multiple UUIDs:", uuids)
#     except ValueError as e:
#         print("Error:", e)

# def test_generate_uuid_for_email():
#     email = "test@example.com"
#     uuid_email = generate_uuid_for_email(email)
#     print("Generated UUID for Email:", uuid_email)

# def test_generate_custom_uuid():
#     print("Custom UUID (pattern: 'xxxx-xxxx', length: 4):", generate_custom_uuid('xxxx-xxxx',4))
#     print("Custom UUID (pattern: 'abcd-dddd', length: 4, prefix: 'user'):", generate_custom_uuid('abcd-dddd', 4, 'user'))
#     print("Custom UUID (pattern: 'x-dx-x', length: 3):", generate_custom_uuid('x-dx-x', 3))
#     basic_uuid = generate_custom_uuid('x-x-x-x-x',10)
#     print(basic_uuid)
#     prefixed_uuid = generate_custom_uuid('abcd-dddd', 4, 'user')
#     print(prefixed_uuid)
    


# if __name__ == "__main__":
#     print("Running tests...")
#     test_generate_uuid1()
#     test_generate_uuid4()
#     test_generate_uuid7()
#     test_generate_multiple_uuids()
#     test_generate_uuid_for_email()
#     test_generate_custom_uuid()


print("UUIDv1:", generate_uuid1())
print("UUIDv4:", generate_uuid4())
print("UUIDv7:", generate_uuid7())
print("Nil UUID:", generate_nil_uuid())
print("GUID:", generate_guid())
createdEmailUUID = generate_uuid_for_email("user@bank.com")
print("UUID from Email:", createdEmailUUID)
print(validate_uuid_for_email(createdEmailUUID, 'user@bank.com'))
print("Pattern UUID:", generate_custom_uuid("xxxx-xxxx-BANK-yyyy"))
print("Batch UUIDs:", generate_multiple_uuids(4, 5))

