from hypothesis import strategies as st
from microscopemetrics_schema.datamodel import microscopemetrics_schema as mm_schema
from microscopemetrics_schema.strategies import st_mm_sample

@st.composite
def st_mm_homogeneous_field_sample(
    draw,
    sample=st_mm_sample(),
) -> mm_schema.HomogeneousField:
    return draw(sample)


@st.composite
def st_mm_homogeneous_thin_field_sample(
    draw,
    sample=st_mm_homogeneous_field_sample(),
) -> mm_schema.FluorescentHomogeneousThinField:
    return draw(sample)


@st.composite
def st_mm_homogeneous_thick_field_sample(
    draw,
    sample=st_mm_homogeneous_field_sample(),
) -> mm_schema.FluorescentHomogeneousThickField:
    return draw(sample)


