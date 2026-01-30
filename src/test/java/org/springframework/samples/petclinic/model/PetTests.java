package org.springframework.samples.petclinic.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PetTests {

    private Pet pet;

    @BeforeEach
    void setUp() {
        pet = new Pet();
        pet.setName("Fido");
        pet.setBirthDate(LocalDate.of(2020, 1, 1));
    }

    @Test
    void getVisits_shouldReturnEmptyList_whenNoVisitsAdded() {
        List<Visit> visits = pet.getVisits();

        assertNotNull(visits);
        assertTrue(visits.isEmpty());
    }

    @Test
    void getVisits_shouldReturnVisits_whenVisitsAdded() {
        Visit visit1 = new Visit();
        visit1.setDate(LocalDate.of(2023, 6, 15));
        visit1.setDescription("Vaccination");

        Visit visit2 = new Visit();
        visit2.setDate(LocalDate.of(2023, 9, 20));
        visit2.setDescription("Checkup");

        pet.addVisit(visit1);
        pet.addVisit(visit2);

        List<Visit> visits = pet.getVisits();

        assertNotNull(visits);
        assertEquals(2, visits.size());
    }

    @Test
    void getVisits_shouldReturnVisitsSortedByDate() {
        Visit olderVisit = new Visit();
        olderVisit.setDate(LocalDate.of(2023, 1, 10));
        olderVisit.setDescription("First visit");

        Visit newerVisit = new Visit();
        newerVisit.setDate(LocalDate.of(2023, 12, 20));
        newerVisit.setDescription("Recent visit");

        pet.addVisit(newerVisit);
        pet.addVisit(olderVisit);

        List<Visit> visits = pet.getVisits();

        assertEquals(2, visits.size());
        assertTrue(visits.get(0).getDate().isAfter(visits.get(1).getDate()) ||
            visits.get(0).getDate().isEqual(visits.get(1).getDate()));
    }

    @Test
    void addVisit_shouldSetPetIdOnVisit() {
        pet.setId(5);
        Visit visit = new Visit();
        visit.setDate(LocalDate.now());
        visit.setDescription("Test visit");

        pet.addVisit(visit);

        assertEquals(pet.getId(), visit.getPet().getId());
    }
}
