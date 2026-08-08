package test;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ContactServicesTest {
	
	@BeforeEach
	void setUp() {
		contactService = ContactServices.getInstance();
		contactService.reset();
	}

	@Test
	void addContactTest() {
		String contactId = contactServices.addContact("first", "last", "1234567890", "123 Purple Ave");
		
		assertNotNull(contactId);
		assertEquals("1", contactId);
	}

}
