package org.springframework.samples.petclinic.model;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;
import java.util.Locale;
import java.util.Set;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validator;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;

/**
 * @author Michael Isvy
 *         Simple test to make sure that Bean Validation is working
 *         (useful when upgrading to a new version of Hibernate Validator/ Bean Validation)
 */
class ValidatorTests {

    private LocalValidatorFactoryBean localValidatorFactoryBean;

    @BeforeEach
    void setUp() {
        localValidatorFactoryBean = new LocalValidatorFactoryBean();
        localValidatorFactoryBean.afterPropertiesSet();
    }

    @AfterEach
    void tearDown() {
        localValidatorFactoryBean.close();
    }

    @Test
    void shouldNotValidateWhenFirstNameEmpty() {

        LocaleContextHolder.setLocale(Locale.ENGLISH);
        Person person = new Person();
        person.setFirstName("");
        person.setLastName("smith");

        Validator validator = createValidator();
        Set<ConstraintViolation<Person>> constraintViolations = validator.validate(person);

        assertThat(constraintViolations).hasSize(1);
        ConstraintViolation<Person> violation = constraintViolations.iterator().next();
        assertThat(violation.getPropertyPath()).hasToString("firstName");
        assertThat(violation.getMessage()).isEqualTo("must not be empty");
    }

    private Validator createValidator() {
        return localValidatorFactoryBean.getValidator();
    }

    @Test
    void shouldRejectMicrochipIdWithWrongLength() {
        LocaleContextHolder.setLocale(Locale.ENGLISH);
        Pet pet = new Pet();
        pet.setName("TestPet");
        PetType type = new PetType();
        type.setName("cat");
        pet.setType(type);
        pet.setBirthDate(LocalDate.now());

        // 14 digits — too short
        pet.setMicrochipId("12345678901234");
        Validator validator = createValidator();
        Set<ConstraintViolation<Pet>> violations = validator.validate(pet);
        assertThat(violations).anyMatch(v -> v.getPropertyPath().toString().equals("microchipId"));

        // 16 digits — too long
        pet.setMicrochipId("1234567890123456");
        violations = validator.validate(pet);
        assertThat(violations).anyMatch(v -> v.getPropertyPath().toString().equals("microchipId"));
    }

    @Test
    void shouldRejectMicrochipIdWithNonNumericCharacters() {
        LocaleContextHolder.setLocale(Locale.ENGLISH);
        Pet pet = new Pet();
        pet.setName("TestPet");
        PetType type = new PetType();
        type.setName("cat");
        pet.setType(type);
        pet.setBirthDate(LocalDate.now());

        // non-numeric
        pet.setMicrochipId("ABCDE1234567890");
        Validator validator = createValidator();
        Set<ConstraintViolation<Pet>> violations = validator.validate(pet);
        assertThat(violations).anyMatch(v -> v.getPropertyPath().toString().equals("microchipId"));
    }

    @Test
    void shouldAcceptValidMicrochipId() {
        LocaleContextHolder.setLocale(Locale.ENGLISH);
        Pet pet = new Pet();
        pet.setName("TestPet");
        PetType type = new PetType();
        type.setName("cat");
        pet.setType(type);
        pet.setBirthDate(LocalDate.now());

        // exactly 15 digits — valid
        pet.setMicrochipId("123456789012345");
        Validator validator = createValidator();
        Set<ConstraintViolation<Pet>> violations = validator.validate(pet);
        assertThat(violations).noneMatch(v -> v.getPropertyPath().toString().equals("microchipId"));
    }

}
