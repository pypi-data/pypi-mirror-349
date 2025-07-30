from hypothesis import strategies as st
from microscopemetrics_schema.datamodel import microscopemetrics_schema as mm_schema
from microscopemetrics_schema.strategies import st_mm_sample


@st.composite
def st_mm_user_experiment_sample(
    draw,
    sample=st_mm_sample(),
) -> mm_schema.UserExperiment:
    return mm_schema.UserExperiment(
        **draw(sample)._as_dict,
    )

