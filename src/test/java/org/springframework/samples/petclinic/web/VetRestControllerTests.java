package org.springframework.samples.petclinic.web;

import org.assertj.core.util.Lists;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.samples.petclinic.model.Specialty;
import org.springframework.samples.petclinic.model.Vet;
import org.springframework.samples.petclinic.service.ClinicService;
import org.springframework.test.context.junit.jupiter.web.SpringJUnitWebConfig;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.hamcrest.xml.HasXPath.hasXPath;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Test class for {@link VetRestController}.
 *
 * <p>Uses MockMvc standalone setup (no full Spring context) with a mocked {@link ClinicService}.
 * Fixture: James Carter (no specialties, id=1) and Helen Leary (radiology, id=2).
 */
@SpringJUnitWebConfig(locations = {"classpath:spring/mvc-core-config.xml", "classpath:spring/mvc-test-config.xml"})
class VetRestControllerTests {

    @Autowired
    private VetRestController vetRestController;

    @Autowired
    private ClinicService clinicService;

    private MockMvc mockMvc;

    @BeforeEach
    void setup() {
        this.mockMvc = MockMvcBuilders.standaloneSetup(vetRestController).build();

        Vet james = new Vet();
        james.setFirstName("James");
        james.setLastName("Carter");
        james.setId(1);

        Vet helen = new Vet();
        helen.setFirstName("Helen");
        helen.setLastName("Leary");
        helen.setId(2);
        Specialty radiology = new Specialty();
        radiology.setId(1);
        radiology.setName("radiology");
        helen.addSpecialty(radiology);

        given(this.clinicService.findVets()).willReturn(Lists.newArrayList(james, helen));
    }

    @Test
    void testListVetsJson_returns200() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }

    @Test
    void testListVetsJson_firstVetFields() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.vetList[0].id").value(1))
            .andExpect(jsonPath("$.vetList[0].firstName").value("James"))
            .andExpect(jsonPath("$.vetList[0].lastName").value("Carter"));
    }

    @Test
    void testListVetsJson_secondVetHasSpecialty() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.vetList[1].specialties[0].name").value("radiology"));
    }

    @Test
    void testListVetsJson_vetListSize() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.vetList.length()").value(2));
    }

    @Test
    void testListVetsXml_returns200() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.APPLICATION_XML))
            .andExpect(status().isOk())
            .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_XML));
    }

    @Test
    void testListVetsXml_containsVetId() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.APPLICATION_XML))
            .andExpect(status().isOk())
            .andExpect(content().node(hasXPath("/vets/vet[id=1]/id")));
    }

    @Test
    void testListVets_noAcceptHeader_returnsJsonByDefault() throws Exception {
        // No Accept header: Spring MVC picks first produces value (JSON)
        mockMvc.perform(get("/api/vets"))
            .andExpect(status().isOk())
            .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON));
    }

    @Test
    void testListVets_htmlAcceptNotSupported_returns406() throws Exception {
        mockMvc.perform(get("/api/vets").accept(MediaType.TEXT_HTML))
            .andExpect(status().isNotAcceptable());
    }

}
