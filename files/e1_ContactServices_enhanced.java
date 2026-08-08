package MS1;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

// Singleton service holding all Contact records.
public class ContactServices {

    // The singleton instance
    private static ContactServices instance;

    // Contact storage keyed by contact ID. Never null or reassigned.
    private final Map<String, Contact> contacts = new HashMap<>();

    // Source of sequential contact identifiers.
    private int nextId;

    private ContactServices() {
        this.nextId = 1;
    }

    public static ContactServices getInstance() {
        if (instance == null) {
            instance = new ContactServices();
        }
        return instance;
    }

    // Create

    // Validation happens inside the Contact constructor, so invalid input throws before
    // anything is stored and nextId is not consumed.
    public String addContact(String firstName, String lastName, String phone, String address) {
        String contactId = String.valueOf(nextId);
        Contact newContact = new Contact(contactId, firstName, lastName, phone, address);
        contacts.put(contactId, newContact);
        nextId++;
        return contactId;
    }

    // Delete

    // Replaces the original find-then-shift-left loop
    public boolean deleteContact(String contactId) {
        return contacts.remove(contactId) != null;
    }

    // Read views

    // Added so tests can confirm an update changed stored state
    public Contact getContact(String contactId) {
        return contacts.get(contactId);
    }

    // Replaces the original contactCount field
    public int getContactCount() {
        return contacts.size();
    }

    // Read-only view. 
    public Map<String, Contact> getAllContacts() {
        return Collections.unmodifiableMap(contacts);
    }

    // Update

    // Single lookup shared by all four update methods.
    private Contact findContact(String contactId) {
        return contacts.get(contactId);
    }

    // Each update returns false for an unknown ID and delegates the value rules to the
    // Contact setters, so an invalid value throws and leaves the record unchanged.
    public boolean updateFirstName(String contactId, String firstName) {
        Contact contact = findContact(contactId);
        if (contact == null) {
            return false;
        }
        contact.setFirst(firstName);
        return true;
    }

    public boolean updateLastName(String contactId, String lastName) {
        Contact contact = findContact(contactId);
        if (contact == null) {
            return false;
        }
        contact.setLast(lastName);
        return true;
    }

    public boolean updatePhone(String contactId, String phone) {
        Contact contact = findContact(contactId);
        if (contact == null) {
            return false;
        }
        contact.setPhone(phone);
        return true;
    }

    public boolean updateAddress(String contactId, String address) {
        Contact contact = findContact(contactId);
        if (contact == null) {
            return false;
        }
        contact.setAddress(address);
        return true;
    }

    // Test support. Clears storage and restarts ID generation so each test starts clean
    public void reset() {
        contacts.clear();
        nextId = 1;
    }
}
