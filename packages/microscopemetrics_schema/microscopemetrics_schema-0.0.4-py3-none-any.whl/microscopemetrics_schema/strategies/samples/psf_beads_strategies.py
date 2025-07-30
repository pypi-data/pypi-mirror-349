from hypothesis import strategies as st
from microscopemetrics_schema.datamodel import microscopemetrics_schema as mm_schema
from microscopemetrics_schema.strategies import st_mm_sample


@st.composite
def st_mm_psf_beads_sample(
    draw,
    sample=st_mm_sample(),
) -> mm_schema.PSFBeads:
    return mm_schema.PSFBeads(
        bead_diameter_micron=draw(st.floats(min_value=0.1, max_value=0.5)),
        **draw(sample)._as_dict,
    )


