from hypothesis import strategies as st
from microscopemetrics_schema.datamodel import microscopemetrics_schema as mm_schema
from microscopemetrics_schema.strategies import (
    st_mm_metrics_object,
    st_mm_image,
    st_mm_dataset,
    st_mm_output,
)
from microscopemetrics_schema.strategies.samples.homogeneous_field_strategies import (
    st_mm_homogeneous_thin_field_sample,
    st_mm_homogeneous_thick_field_sample,
)


@st.composite
def st_mm_field_illumination_input_data(
    draw,
    field_illumination_image=st.lists(st_mm_image(), min_size=1, max_size=3),
) -> mm_schema.FieldIlluminationInputData:
    return mm_schema.FieldIlluminationInputData(
        field_illumination_images=draw(field_illumination_image),
    )


@st.composite
def st_mm_field_illumination_input_parameters(
    draw,
    bit_depth=st.sampled_from([8, 10, 11, 12, 15, 16, 32]),
    saturation_threshold=st.floats(min_value=0.01, max_value=0.05),
    corner_fraction=st.floats(min_value=0.02, max_value=0.3),
    sigma=st.floats(min_value=2.0, max_value=4.0),
) -> mm_schema.FieldIlluminationInputParameters:
    return mm_schema.FieldIlluminationInputParameters(
        bit_depth=draw(bit_depth),
        saturation_threshold=draw(saturation_threshold),
        corner_fraction=draw(corner_fraction),
        sigma=draw(sigma),
    )


@st.composite
def st_mm_field_illumination_output_key_measurements(
    draw,
    mm_object=st_mm_metrics_object(),
) -> mm_schema.FieldIlluminationKeyMeasurements:
    mm_object = draw(mm_object)
    return mm_schema.FieldIlluminationKeyMeasurements(
        name=mm_object.name,
        description=mm_object.description,
    )


@st.composite
def st_mm_field_illumination_output(
    draw,
    output=st_mm_output(
        processing_entity=st.just("FieldIlluminationAnalysis"),
    ),
    key_measurements=st_mm_field_illumination_output_key_measurements(),
) -> mm_schema.FieldIlluminationOutput:
    mm_output = draw(output)
    return mm_schema.FieldIlluminationOutput(
        processing_application=mm_output.processing_application,
        processing_version=mm_output.processing_version,
        processing_entity=mm_output.processing_entity,
        processing_datetime=mm_output.processing_datetime,
        key_measurements=draw(key_measurements),
        processing_log=mm_output.processing_log,
        warnings=mm_output.warnings,
        errors=mm_output.errors,
        comment=mm_output.comment,
    )


@st.composite
def st_mm_field_illumination_unprocessed_dataset(
    draw,
    processed=st.just(False),
    input_data=st_mm_field_illumination_input_data(),
    sample=st.one_of(
        st_mm_homogeneous_thin_field_sample(),
        st_mm_homogeneous_thick_field_sample(),
    ),
    input_parameters=st_mm_field_illumination_input_parameters(),
) -> mm_schema.FieldIlluminationDataset:
    sample = draw(sample)
    input_parameters = draw(input_parameters)
    return draw(
        st_mm_dataset(
            target_class=mm_schema.FieldIlluminationDataset,
            processed=processed,
            input_data=input_data,
            sample=sample,
            input_parameters=input_parameters,
        )
    )


@st.composite
def st_mm_field_illumination_processed_dataset(
    draw,
    processed=st.just(True),
    input_data=st_mm_field_illumination_input_data(),
    output=st_mm_field_illumination_output(),
    sample=st.one_of(
        st_mm_homogeneous_thin_field_sample(),
        st_mm_homogeneous_thick_field_sample(),
    ),
    input_parameters=st_mm_field_illumination_input_parameters(),
) -> mm_schema.FieldIlluminationDataset:
    sample = draw(sample)
    input_parameters = draw(input_parameters)
    return draw(
        st_mm_dataset(
            target_class=mm_schema.FieldIlluminationDataset,
            processed=processed,
            input_data=input_data,
            output=output,
            sample=sample,
            input_parameters=input_parameters,
        )
    )

