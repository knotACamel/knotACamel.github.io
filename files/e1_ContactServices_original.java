package MS1;

public class ContactServices {
	private static ContactServices instance;
	private Contact[] contacts;
	private int nextId;
	private int contactCount;
	private static final int MAX_CONTACTS = 9999;
	
	private ContactServices() {
		this.contacts = new Contact[MAX_CONTACTS];
		this.nextId = 1;
		this.contactCount = 0;
	}
	
	public static ContactServices getInstance() {
		if (instance == null) {
			instance = new ContactServices();
		}
		return instance;
	}
	
	public String addContact(String firstName, String lastName, String phone, String address) {
		if (contactCount > MAX_CONTACTS) {
			return null;
		}
		
		String contactId = String.valueOf(nextId++);
		Contact newContact = new Contact(contactId, firstName, lastName, phone, address);
		contacts[contactCount++] = newContact;
		
		return contactId;
	}
	
	public boolean deleteContact(String contactId) {
		int index = findContactIndex(contactId);
		if (index == -1) {
			return false;
		}
		
		for (int i = index; i < contactCount - 1; i++) {
			contacts[i] = contacts[i + 1];
		}
		contacts[--contactCount] = null;
		
		return true;
	}
	
	private int findContactIndex(String contactId) {
		for (int i = 0; i < contactCount; i++) {
			if (contacts[i].getID().equals(contactId)) {
				return i;
			}
		}
		
		return -1;
	}
	
	private Contact findContact(String contactId) {
		for (int i = 0; i < contactCount; i++) {
			if (contacts[i].getID().equals(contactId)) {
				return contacts[i];
			}
		}
		
		return null;
	}
	
	public boolean updateFirstName(String contactId, String firstName) {
		Contact contact = findContact(contactId);
		if (contact != null) {
			contact.setFirst(firstName);
			return true;
		}
		return false;
	}
	
	public boolean updateLastName(String contactId, String lastName) {
		Contact contact = findContact(contactId);
		if (contact != null) {
			contact.setLast(lastName);
			return true;
		}
		return false;
	}
	
	public boolean updatePhone(String contactId, String phone) {
		Contact contact = findContact(contactId);
		if (contact != null) {
			contact.setPhone(phone);
			return true;
		}
		return false;
	}
	
	public boolean updateAddress(String contactId, String address) {
		Contact contact = findContact(contactId);
		if (contact != null) {
			contact.setAddress(address);
			return true;
		}
		return false;
	}
	
	public void reset() {
		contacts = new Contact
	}
	
}
