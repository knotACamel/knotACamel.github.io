package MS1;

public class Contact {

    // Maximum length of the ID field.
    private static final int MAX_ID_LENGTH = 10;
    // Maximum length shared by both name fields.
    private static final int MAX_NAME_LENGTH = 10;
    // Required length of a phone number
    private static final int PHONE_LENGTH = 10;
    // Maximum length of the address field
    private static final int MAX_ADDRESS_LENGTH = 30;

    // Immutable unique identifier. Assigned at construction and never reassigned.
    private final String contactID;

    private String firstName;
    private String lastName;
    private String phone;
    private String address;

    // Constructor 
    public Contact(String contactID,
                   String firstName,
                   String lastName,
                   String phone,
                   String address) {
        this.contactID = validateId(contactID);
        this.firstName = validateName(firstName, "First name");
        this.lastName = validateName(lastName, "Last name");
        this.phone = validatePhone(phone);
        this.address = validateAddress(address);
    }


    // Validation methods for constructor and setter methods. All current and future
    // methods that change internal variables shall run through these methods as a constraint validation layer. 
    private static String validateId(String value) {
        if (value == null) {
            throw new IllegalArgumentException("Contact ID must not be null");
        }
        if (value.isEmpty()) {
            throw new IllegalArgumentException("Contact ID must not be empty");
        }
        if (value.length() > MAX_ID_LENGTH) {
            throw new IllegalArgumentException(
                    "Contact ID must be at most " + MAX_ID_LENGTH
                            + " characters but was " + value.length());
        }
        return value;
    }

    private static String validateName(String value, String fieldName) {
        if (value == null) {
            throw new IllegalArgumentException(fieldName + " must not be null");
        }
        if (value.length() > MAX_NAME_LENGTH) {
            throw new IllegalArgumentException(
                    fieldName + " must be at most " + MAX_NAME_LENGTH
                            + " characters but was " + value.length());
        }
        return value;
    }

    private static String validatePhone(String value) {
        if (value == null) {
            throw new IllegalArgumentException("Phone must not be null");
        }
        if (value.length() != PHONE_LENGTH) {
            throw new IllegalArgumentException(
                    "Phone must be exactly " + PHONE_LENGTH
                            + " digits but was " + value.length() + " characters");
        }
        if (!value.matches("\\d{" + PHONE_LENGTH + "}")) {
            throw new IllegalArgumentException(
                    "Phone must contain digits only but was \"" + value + "\"");
        }
        return value;
    }

    private static String validateAddress(String value) {
        if (value == null) {
            throw new IllegalArgumentException("Address must not be null");
        }
        if (value.length() > MAX_ADDRESS_LENGTH) {
            throw new IllegalArgumentException(
                    "Address must be at most " + MAX_ADDRESS_LENGTH
                            + " characters but was " + value.length());
        }
        return value;
    }

    // Getters, all fields
    public String getID() {
        return contactID;
    }

    public String getFirst() {
        return firstName;
    }

    public String getLast() {
        return lastName;
    }

    public String getPhone() {
        return phone;
    }

    public String getAddress() {
        return address;
    }

    // Setters, all fields minus immutable ID
    // All setters go through validation methods to ensure compliance to constraints
    public void setFirst(String firstName) {
        this.firstName = validateName(firstName, "First name");
    }

    public void setLast(String lastName) {
        this.lastName = validateName(lastName, "Last name");
    }

    public void setPhone(String phone) {
        this.phone = validatePhone(phone);
    }

    public void setAddress(String address) {
        this.address = validateAddress(address);
    }

    @Override
    public String toString() {
        return "Contact{id=" + contactID
                + ", name=" + firstName + " " + lastName
                + ", phone=******" + phone.substring(PHONE_LENGTH - 4)
                + "}";
    }
}
