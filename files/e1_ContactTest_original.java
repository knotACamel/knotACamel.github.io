package test;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import MS1.Contact;

class ContactTest {

	@Test
	void testContact() {
		Contact contact = new Contact(
				"1234", 
				"first", 
				"last", 
				"1234567890", 
				"1234 Road Lane");
		assertTrue(contact.getID().equals("1234"));
		assertTrue(contact.getFirst().equals("first"));
		assertTrue(contact.getLast().equals("last"));
		assertTrue(contact.getPhone().equals("1234567890"));
		assertTrue(contact.getAddress().equals("1234 Road Lane"));
	}
	
	@Test
	void testContactIDTooLong() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> {
			new Contact("12345678901", "first", "last", "1234567890", "1234");
		});
	}
	
	void testContactFirstTooLong() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> {
			new Contact("1234", "firstfirstfirstfirst", "last", "1234567890", "1234");
		});
	}
	
	void testContactLastTooLong() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> {
			new Contact("12345678901", "first", "lastlastlastlast", "1234567890", "1234");
		});
	}
	
	void testContactPhoneTooShort() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> {
			new Contact("12345678901", "first", "last", "12345", "1234");
		});
	}
	
	void testContactPhoneTooLong() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> {
			new Contact("12345678901", "first", "last", "1234567890123", "1234");
		});
	}
	
	void testContactAddressTooLong() {
		Assertions.assertThrows(IllegalArgumentException.class, () -> {
			new Contact("12345678901", "first", "last", "1234567890", 
					"1234 Keith David is the GOAT, but Raphael Sbarge is pretty good too");
		});
	}

}
