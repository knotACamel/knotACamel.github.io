package test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import MS1.Contact; 
import MS1.ContactServices;

class ContactServicesTest {

    private ContactServices contactServices;

    @BeforeEach
    void setUp() {
        contactServices = ContactServices.getInstance();
        contactServices.reset();
    }

    // Singleton

    @Test
    @DisplayName("getInstance returns the same object on every call")
    void getInstanceReturnsSingleton() {
        assertEquals(ContactServices.getInstance(), ContactServices.getInstance());
    }

    @Test
    @DisplayName("reset clears storage and restarts ID generation at 1")
    void resetClearsState() {
        contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");
        contactServices.addContact("Other", "Person", "1234567891", "456 Green St");
        assertEquals(2, contactServices.getContactCount());

        contactServices.reset();

        assertEquals(0, contactServices.getContactCount());
        assertEquals("1", contactServices.addContact("New", "Contact", "1234567892", "789 Blue Rd"));
    }

    
    // Add
    

    @Test
    @DisplayName("addContact returns a non-null identifier and stores the contact")
    void addContactStoresContact() {
        String contactId = contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");

        assertNotNull(contactId);
        assertEquals("1", contactId);
        assertEquals(1, contactServices.getContactCount());

        Contact stored = contactServices.getContact(contactId);
        assertNotNull(stored);
        assertEquals("First", stored.getFirst());
        assertEquals("1234567890", stored.getPhone());
    }

    @Test
    @DisplayName("addContact issues sequential identifiers")
    void addContactIssuesSequentialIds() {
        assertEquals("1", contactServices.addContact("A", "One", "1111111111", "1 A St"));
        assertEquals("2", contactServices.addContact("B", "Two", "2222222222", "2 B St"));
        assertEquals("3", contactServices.addContact("C", "Three", "3333333333", "3 C St"));
        assertEquals(3, contactServices.getContactCount());
    }

    @Test
    @DisplayName("addContact rejects invalid input and stores nothing")
    void addContactRejectsInvalidInput() {
        assertThrows(IllegalArgumentException.class,
                () -> contactServices.addContact("First", "Last", "555-1234", "123 Purple Ave"));

        assertEquals(0, contactServices.getContactCount());
    }

    @Test
    @DisplayName("Storage exceeds the original 9,999-contact ceiling")
    void addContactHasNoCapacityLimit() {
        for (int i = 0; i < 20000; i++) {
            contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");
        }

        assertEquals(20000, contactServices.getContactCount());
        assertNotNull(contactServices.getContact("20000"));
    }

    
    // Delete
    

    @Test
    @DisplayName("deleteContact removes an existing contact and reports success once")
    void deleteContactRemovesContact() {
        String contactId = contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");

        assertTrue(contactServices.deleteContact(contactId));
        assertFalse(contactServices.deleteContact(contactId));
        assertNull(contactServices.getContact(contactId));
        assertEquals(0, contactServices.getContactCount());
    }

    @Test
    @DisplayName("deleteContact returns false for an unknown or null identifier")
    void deleteContactHandlesMissingIds() {
        assertFalse(contactServices.deleteContact("does-not-exist"));
        assertFalse(contactServices.deleteContact(null));
    }

    @Test
    @DisplayName("Deleting one contact leaves the remaining contacts intact")
    void deleteContactPreservesOtherContacts() {
        String first = contactServices.addContact("A", "One", "1111111111", "1 A St");
        String second = contactServices.addContact("B", "Two", "2222222222", "2 B St");
        String third = contactServices.addContact("C", "Three", "3333333333", "3 C St");

        assertTrue(contactServices.deleteContact(second));

        assertEquals(2, contactServices.getContactCount());
        assertNotNull(contactServices.getContact(first));
        assertNull(contactServices.getContact(second));
        assertNotNull(contactServices.getContact(third));
        assertEquals("C", contactServices.getContact(third).getFirst());
    }

    
    // Update
    

    @Test
    @DisplayName("Each update method changes the stored value and reports success")
    void updateMethodsChangeStoredValues() {
        String contactId = contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");

        assertTrue(contactServices.updateFirstName(contactId, "Dustin"));
        assertTrue(contactServices.updateLastName(contactId, "Ledbetter"));
        assertTrue(contactServices.updatePhone(contactId, "9876543210"));
        assertTrue(contactServices.updateAddress(contactId, "42 Enhancement Way"));

        Contact stored = contactServices.getContact(contactId);
        assertEquals("Dustin", stored.getFirst());
        assertEquals("Ledbetter", stored.getLast());
        assertEquals("9876543210", stored.getPhone());
        assertEquals("42 Enhancement Way", stored.getAddress());
    }

    @Test
    @DisplayName("Every update method returns false for an unknown identifier")
    void updateMethodsReturnFalseForMissingContact() {
        assertFalse(contactServices.updateFirstName("missing", "Dustin"));
        assertFalse(contactServices.updateLastName("missing", "Ledbetter"));
        assertFalse(contactServices.updatePhone("missing", "9876543210"));
        assertFalse(contactServices.updateAddress("missing", "42 Enhancement Way"));
    }

    @Test
    @DisplayName("Updates enforce validation, which the original setters bypassed")
    void updateMethodsEnforceValidation() {
        String contactId = contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");

        assertThrows(IllegalArgumentException.class,
                () -> contactServices.updateFirstName(contactId, null));
        assertThrows(IllegalArgumentException.class,
                () -> contactServices.updatePhone(contactId, "555-1234"));

        Contact stored = contactServices.getContact(contactId);
        assertEquals("First", stored.getFirst());
        assertEquals("1234567890", stored.getPhone());
    }

    
    // Read views
    

    @Test
    @DisplayName("getContact returns null for an unknown identifier")
    void getContactReturnsNullForMissingId() {
        assertNull(contactServices.getContact("missing"));
    }

    @Test
    @DisplayName("getAllContacts exposes a read-only view of storage")
    void getAllContactsIsUnmodifiable() {
        String contactId = contactServices.addContact("First", "Last", "1234567890", "123 Purple Ave");
        Map<String, Contact> view = contactServices.getAllContacts();

        assertEquals(1, view.size());
        assertTrue(view.containsKey(contactId));
        assertThrows(UnsupportedOperationException.class, () -> view.remove(contactId));
    }
}
