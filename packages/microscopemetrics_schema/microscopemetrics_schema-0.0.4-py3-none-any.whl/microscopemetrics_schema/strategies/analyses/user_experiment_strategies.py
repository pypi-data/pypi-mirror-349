from hypothesis import strategies as st
from microscopemetrics_schema.datamodel import microscopemetrics_schema as mm_schema
from microscopemetrics_schema.strategies import (
    st_mm_image,
    st_mm_dataset,
    st_mm_output,
)
from microscopemetrics_schema.strategies.samples.user_experiment_strategies import (
    st_mm_user_experiment_sample,
)


@st.composite
def st_mm_user_experiment_input_data(
    draw,
    user_experiment_images=st.lists(st_mm_image(), min_size=1, max_size=3),
) -> mm_schema.UserExperimentInputData:
    return mm_schema.UserExperimentInputData(
        user_experiment_images=draw(user_experiment_images),
    )


@st.composite
def st_mm_user_experiment_input_parameters(
    draw,
    bit_depth=st.sampled_from([8, 10, 11, 12, 15, 16, 32]),
    saturation_threshold=st.floats(min_value=0.01, max_value=0.05),
) -> mm_schema.UserExperimentInputParameters:
    return mm_schema.UserExperimentInputParameters(
        bit_depth=draw(bit_depth),
        saturation_threshold=draw(saturation_threshold),
    )


@st.composite
def st_mm_user_experiment_output(
    draw,
    output=st_mm_output(
        processing_entity=st.just("UserExperimentAnalysis"),
    ),
) -> mm_schema.UserExperimentOutput:
    mm_output = draw(output)
    return mm_schema.UserExperimentOutput(
        processing_application=mm_output.processing_application,
        processing_version=mm_output.processing_version,
        processing_entity=mm_output.processing_entity,
        processing_datetime=mm_output.processing_datetime,
        processing_log=mm_output.processing_log,
        warnings=mm_output.warnings,
        errors=mm_output.errors,
        comment=mm_output.comment,
    )


@st.composite
def st_mm_user_experiment_unprocessed_dataset(
    draw,
    dataset=st_mm_dataset(
        target_class=mm_schema.UserExperimentDataset,
        sample=st_mm_user_experiment_sample(),
        processed=st.just(False),
        input_data=st_mm_user_experiment_input_data(),
        input_parameters=st_mm_user_experiment_input_parameters(),
    )
) -> mm_schema.UserExperimentDataset:
    return draw(dataset)


@st.composite
def st_mm_user_experiment_processed_dataset(
    draw,
    dataset=st_mm_dataset(
        target_class=mm_schema.UserExperimentDataset,
        sample=st_mm_user_experiment_sample(),
        processed=st.just(True),
        input_data=st_mm_user_experiment_input_data(),
        input_parameters=st_mm_user_experiment_input_parameters(),
        output=st_mm_user_experiment_output(),
    )
) -> mm_schema.UserExperimentDataset:
    return draw(dataset)

