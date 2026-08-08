package test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import MS1.Contact;

class ContactTest {

    private static final String VALID_ID = "1234";
    private static final String VALID_FIRST = "First";
    private static final String VALID_LAST = "Last";
    private static final String VALID_PHONE = "1234567890";
    private static final String VALID_ADDRESS = "1234 Road Lane";

    private static Contact newValidContact() {
        return new Contact(VALID_ID, VALID_FIRST, VALID_LAST, VALID_PHONE, VALID_ADDRESS);
    }

    // Construction

    @Test
    @DisplayName("A fully valid contact stores every field unchanged")
    void constructorStoresAllFields() {
        Contact contact = newValidContact();

        assertEquals(VALID_ID, contact.getID());
        assertEquals(VALID_FIRST, contact.getFirst());
        assertEquals(VALID_LAST, contact.getLast());
        assertEquals(VALID_PHONE, contact.getPhone());
        assertEquals(VALID_ADDRESS, contact.getAddress());
    }

    @Test
    @DisplayName("Boundary values at the maximum allowed length are accepted")
    void constructorAcceptsMaximumLengths() {
        Contact contact = new Contact("1234567890", "0123456789", "0123456789",
                VALID_PHONE, "123456789012345678901234567890");

        assertEquals("1234567890", contact.getID());
        assertEquals("0123456789", contact.getFirst());
        assertEquals(30, contact.getAddress().length());
    }

    // Contact ID

    @Test
    @DisplayName("A null contact ID is rejected")
    void constructorRejectsNullId() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(null, VALID_FIRST, VALID_LAST, VALID_PHONE, VALID_ADDRESS));
    }

    @Test
    @DisplayName("An empty contact ID is rejected")
    void constructorRejectsEmptyId() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact("", VALID_FIRST, VALID_LAST, VALID_PHONE, VALID_ADDRESS));
    }

    @Test
    @DisplayName("A contact ID of 11 characters is rejected")
    void constructorRejectsLongId() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact("12345678901", VALID_FIRST, VALID_LAST, VALID_PHONE, VALID_ADDRESS));
    }

    // Names

    @Test
    @DisplayName("A null first name is rejected")
    void constructorRejectsNullFirstName() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, null, VALID_LAST, VALID_PHONE, VALID_ADDRESS));
    }

    @Test
    @DisplayName("A first name of 11 characters is rejected")
    void constructorRejectsLongFirstName() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, "FirstFirstF", VALID_LAST, VALID_PHONE, VALID_ADDRESS));
    }

    @Test
    @DisplayName("A null last name is rejected")
    void constructorRejectsNullLastName() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, null, VALID_PHONE, VALID_ADDRESS));
    }

    @Test
    @DisplayName("A last name of 11 characters is rejected")
    void constructorRejectsLongLastName() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, "LastLastLas", VALID_PHONE, VALID_ADDRESS));
    }

    
    // Phone
    

    @Test
    @DisplayName("A null phone number is rejected")
    void constructorRejectsNullPhone() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, null, VALID_ADDRESS));
    }

    @Test
    @DisplayName("A 9-digit phone number is rejected")
    void constructorRejectsShortPhone() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, "123456789", VALID_ADDRESS));
    }

    @Test
    @DisplayName("A single-digit phone number is rejected")
    void constructorRejectsSingleDigitPhone() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, "5", VALID_ADDRESS));
    }

    @Test
    @DisplayName("An 11-digit phone number is rejected")
    void constructorRejectsLongPhone() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, "12345678901", VALID_ADDRESS));
    }

    @Test
    @DisplayName("A formatted phone number with non-digit characters is rejected")
    void constructorRejectsNonNumericPhone() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, "555-123456", VALID_ADDRESS));
    }

    
    // Address
    

    @Test
    @DisplayName("A null address is rejected")
    void constructorRejectsNullAddress() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, VALID_PHONE, null));
    }

    @Test
    @DisplayName("An address of 31 characters is rejected")
    void constructorRejectsLongAddress() {
        assertThrows(IllegalArgumentException.class,
                () -> new Contact(VALID_ID, VALID_FIRST, VALID_LAST, VALID_PHONE,
                        "1234567890123456789012345678901"));
    }

    
    // Setters
    

    @Test
    @DisplayName("Valid setter values replace the stored field")
    void settersUpdateFields() {
        Contact contact = newValidContact();

        contact.setFirst("Dustin");
        contact.setLast("Ledbetter");
        contact.setPhone("9876543210");
        contact.setAddress("1234 Enhancement Way");

        assertEquals("Dustin", contact.getFirst());
        assertEquals("Ledbetter", contact.getLast());
        assertEquals("9876543210", contact.getPhone());
        assertEquals("1234 Enhancement Way", contact.getAddress());
    }

    @Test
    @DisplayName("setFirst rejects null and leaves the contact unchanged")
    void setFirstRejectsNull() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setFirst(null));
        assertEquals(VALID_FIRST, contact.getFirst());
    }

    @Test
    @DisplayName("setFirst rejects an over-length value and leaves the contact unchanged")
    void setFirstRejectsLongValue() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setFirst("FirstFirstF"));
        assertEquals(VALID_FIRST, contact.getFirst());
    }

    @Test
    @DisplayName("setLast rejects null and leaves the contact unchanged")
    void setLastRejectsNull() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setLast(null));
        assertEquals(VALID_LAST, contact.getLast());
    }

    @Test
    @DisplayName("setLast rejects an over-length value and leaves the contact unchanged")
    void setLastRejectsLongValue() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setLast("LastLastLas"));
        assertEquals(VALID_LAST, contact.getLast());
    }

    @Test
    @DisplayName("setPhone rejects null and leaves the contact unchanged")
    void setPhoneRejectsNull() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setPhone(null));
        assertEquals(VALID_PHONE, contact.getPhone());
    }

    @Test
    @DisplayName("setPhone rejects a non-numeric value and leaves the contact unchanged")
    void setPhoneRejectsNonNumeric() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setPhone("555-123456"));
        assertEquals(VALID_PHONE, contact.getPhone());
    }

    @Test
    @DisplayName("setAddress rejects null and leaves the contact unchanged")
    void setAddressRejectsNull() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class, () -> contact.setAddress(null));
        assertEquals(VALID_ADDRESS, contact.getAddress());
    }

    @Test
    @DisplayName("setAddress rejects an over-length value and leaves the contact unchanged")
    void setAddressRejectsLongValue() {
        Contact contact = newValidContact();

        assertThrows(IllegalArgumentException.class,
                () -> contact.setAddress("1234567890123456789012345678901"));
        assertEquals(VALID_ADDRESS, contact.getAddress());
    }

    // Diagnostics

    @Test
    @DisplayName("toString masks all but the last four digits of the phone number")
    void toStringMasksPhone() {
        Contact contact = newValidContact();
        String rendered = contact.toString();

        assertEquals(false, rendered.contains(VALID_PHONE));
        assertEquals(true, rendered.contains("7890"));
    }
}
