package MS1;

public class Contact {

		private String contactID;
		private String firstName;
		private String lastName;
		private String phone;
		private String address;
		
		public Contact(
				String contactID,
				String firstName,
				String lastName,
				String phone,
				String address) {
			if (contactID == null || contactID.length() > 10) {
				throw new IllegalArgumentException("Invalid Contact ID");
			}
			if (firstName == null || firstName.length() > 10) {
				throw new IllegalArgumentException("Invalid First Name");
			}
			if (lastName == null || lastName.length() > 10) {
				throw new IllegalArgumentException("Invalid Last Name");
			}
			if (phone == null || phone.length() > 10) {
				throw new IllegalArgumentException("Invalid phone");
			}
			if (address == null || address.length() > 10) {
				throw new IllegalArgumentException("Invalid address");
			}
			
			this.contactID = contactID;
			this.firstName = firstName;
			this.lastName = lastName;
			this.phone = phone;
			this.address = address;
		}
		
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
		
		public void setFirst(String firstName) {
			this.firstName = firstName;
		}
		public void setLast(String lastName) {
			this.lastName = lastName;
		}
		public void setPhone(String phone) {
			this.phone = phone;
		}
		public void setAddress(String address) {
			this.address = address;
		}
}
