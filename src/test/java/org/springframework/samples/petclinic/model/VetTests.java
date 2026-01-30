package org.springframework.samples.petclinic.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class VetTests {

    private Vet vet;

    @BeforeEach
    void setUp() {
        vet = new Vet();
        vet.setFirstName("James");
        vet.setLastName("Carter");
    }

    @Test
    void getSpecialties_shouldReturnEmptyList_whenNoSpecialtiesAdded() {
        List<Specialty> specialties = vet.getSpecialties();

        assertNotNull(specialties);
        assertTrue(specialties.isEmpty());
    }

    @Test
    void getSpecialties_shouldReturnSpecialties_whenSpecialtiesAdded() {
        Specialty surgery = new Specialty();
        surgery.setName("surgery");

        Specialty radiology = new Specialty();
        radiology.setName("radiology");

        vet.addSpecialty(surgery);
        vet.addSpecialty(radiology);

        List<Specialty> specialties = vet.getSpecialties();

        assertNotNull(specialties);
        assertEquals(2, specialties.size());
    }

    @Test
    void getSpecialties_shouldReturnSortedSpecialtiesByName() {
        Specialty surgery = new Specialty();
        surgery.setName("surgery");

        Specialty dentistry = new Specialty();
        dentistry.setName("dentistry");

        Specialty radiology = new Specialty();
        radiology.setName("radiology");

        vet.addSpecialty(surgery);
        vet.addSpecialty(dentistry);
        vet.addSpecialty(radiology);

        List<Specialty> specialties = vet.getSpecialties();

        assertEquals(3, specialties.size());
        assertEquals("dentistry", specialties.get(0).getName());
        assertEquals("radiology", specialties.get(1).getName());
        assertEquals("surgery", specialties.get(2).getName());
    }

    @Test
    void getNrOfSpecialties_shouldReturnZero_whenNoSpecialties() {
        assertEquals(0, vet.getNrOfSpecialties());
    }

    @Test
    void getNrOfSpecialties_shouldReturnCorrectCount() {
        Specialty specialty1 = new Specialty();
        specialty1.setName("surgery");

        Specialty specialty2 = new Specialty();
        specialty2.setName("radiology");

        vet.addSpecialty(specialty1);
        vet.addSpecialty(specialty2);

        assertEquals(2, vet.getNrOfSpecialties());
    }
}
