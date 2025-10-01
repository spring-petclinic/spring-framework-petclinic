// src/main/java/org/springframework/samples/petclinic/owner/BadCodeExamplesController.java

package org.springframework.samples.petclinic.owner;

import org.springframework.stereotype.Controller;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Bu sınıf, SonarQube Quality Gate'ini test etmek için kasıtlı olarak
 * kötü kod pratikleri içermektedir.
 */
@Controller
class BadCodeExamplesController {

	/**
	 * VULNERABILITY: Hardcoded credentials (Sabit kodlanmış parola)
	 * Parolalar ve diğer hassas bilgiler asla kodun içinde açıkça yazılmamalıdır.
	 */
	private String dbPassword = "password123"; // KÖTÜ KOD

	/**
	 * BUG: String'ler '==' ile karşılaştırılıyor.
	 * Nesne referanslarını karşılaştırdığı için beklenmedik sonuçlar doğurabilir.
	 * Bunun yerine .equals() metodu kullanılmalıdır.
	 */
	public boolean compareStrings(String name1, String name2) {
		if (name1 == "test") { // KÖTÜ KOD
			return true;
		}
		return false;
	}

	/**
	 * BUG: Olası NullPointerException.
	 * 'owner' parametresi null gelirse, 'getFirstName()' metodu çağrıldığında
	 * uygulama çökecektir.
	 */
	public void printOwnerName(Owner owner) {
		System.out.println("Owner name length: " + owner.getFirstName().length()); // KÖTÜ KOD
	}

	/**
	 * VULNERABILITY: SQL Injection (SQL Enjeksiyonu)
	 * Kullanıcıdan gelen veri, SQL sorgusuna doğrudan eklenmemelidir. Bu,
	 * kötü niyetli kullanıcıların veritabanınıza zarar vermesine yol açabilir.
	 */
	public void findOwnerByUnsafeQuery(String lastName) throws SQLException {
		String sql = "SELECT * FROM owners WHERE last_name = '" + lastName + "'"; // KÖTÜ KOD

		try (Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/petclinic", "user", dbPassword);
			 Statement stmt = conn.createStatement()) {
			stmt.executeQuery(sql);
		}
	}

	/**
	 * CODE SMELL: Boş catch bloğu.
	 * Hatalar yakalandığında görmezden gelinmemelidir. En azından loglanmalıdır.
	 */
	public void doSomething risky() {
		try {
			// Riskli bir işlem yapılıyor...
			throw new UnsupportedOperationException();
		}
		catch (UnsupportedOperationException e) {
			// Hata yutuluyor, hiçbir şey yapılmıyor. KÖTÜ KOD
		}
	}
    
	/**
	 * CODE SMELL: Yüksek Bilişsel Karmaşıklık (High Cognitive Complexity)
	 * İç içe geçmiş çok fazla if/else/switch bloğu kodun okunmasını ve
	 * bakımını zorlaştırır.
	 */
	public String getOwnerLevel(Owner owner) {
		int petCount = owner.getPets().size();
		if (petCount > 0) { // +1
			if (owner.getCity().equals("Madison")) { // +2
				if (petCount > 2) { // +3
					return "Gold";
				} else {
					return "Silver";
				}
			}
		} else {
			if (owner.getAddress().contains("Street")) { // +2
				return "Bronze";
			}
		}
		return "N/A";
	}

	/**
	 * CODE SMELL: Kullanılmayan private metot.
	 * Bu metot hiçbir yerde çağrılmıyor ve gereksiz yer kaplıyor.
	 */
	private void unusedHelperMethod() { // KÖTÜ KOD
		System.out.println("Bu metot hiç kullanılmadı.");
	}

}