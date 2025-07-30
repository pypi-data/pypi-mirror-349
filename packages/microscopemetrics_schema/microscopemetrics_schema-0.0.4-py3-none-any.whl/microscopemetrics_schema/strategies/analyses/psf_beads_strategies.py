from hypothesis import strategies as st
from microscopemetrics_schema.datamodel import microscopemetrics_schema as mm_schema
from microscopemetrics_schema.strategies import (
    st_mm_metrics_object,
    st_mm_image,
    st_mm_dataset,
    st_mm_output,
)
from microscopemetrics_schema.strategies.samples.psf_beads_strategies import (
    st_mm_psf_beads_sample,
)


@st.composite
def st_mm_psf_beads_input_data(
    draw,
    psf_beads_images=st_mm_image(),
) -> mm_schema.PSFBeadsInputData:
    return mm_schema.PSFBeadsInputData(
        psf_beads_images=draw(psf_beads_images),
    )


@st.composite
def st_mm_psf_beads_input_parameters(
    draw,
    min_lateral_distance_factor=st.floats(min_value=15.0, max_value=25.0),
    sigma_z=st.floats(min_value=0.7, max_value=2.0),
    sigma_y=st.floats(min_value=0.7, max_value=2.0),
    sigma_x=st.floats(min_value=0.7, max_value=2.0),
    snr_threshold=st.just(10.0),
    fitting_r2_threshold=st.just(0.85),
    intensity_robust_z_score_threshold=st.just(2.0),
) -> mm_schema.PSFBeadsInputParameters:
    return mm_schema.PSFBeadsInputParameters(
        min_lateral_distance_factor=draw(min_lateral_distance_factor),
        sigma_z=draw(sigma_z),
        sigma_y=draw(sigma_y),
        sigma_x=draw(sigma_x),
        snr_threshold=draw(snr_threshold),
        fitting_r2_threshold=draw(fitting_r2_threshold),
        intensity_robust_z_score_threshold=draw(intensity_robust_z_score_threshold),
    )


@st.composite
def st_mm_psf_beads_output_key_measurements(
    draw,
    mm_object=st_mm_metrics_object(),
) -> mm_schema.PSFBeadsKeyMeasurements:
    mm_object = draw(mm_object)
    return mm_schema.PSFBeadsKeyMeasurements(
        name=mm_object.name,
        description=mm_object.description,
    )


@st.composite
def st_mm_psf_beads_output(
    draw,
    output=st_mm_output(
        processing_entity=st.just("PSFBeadsAnalysis"),
    ),
    key_measurements=st_mm_psf_beads_output_key_measurements(),
) -> mm_schema.PSFBeadsOutput:
    mm_output = draw(output)
    return mm_schema.PSFBeadsOutput(
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
def st_mm_psf_beads_unprocessed_dataset(
    draw,
    processed=st.just(False),
    input_data=st_mm_psf_beads_input_data(),
    sample=st_mm_psf_beads_sample(),
    input_parameters=st_mm_psf_beads_input_parameters(),
) -> mm_schema.PSFBeadsDataset:
    sample = draw(sample)
    input_parameters = draw(input_parameters)
    return draw(
        st_mm_dataset(
            target_class=mm_schema.PSFBeadsDataset,
            processed=processed,
            input_data=input_data,
            sample=sample,
            input_parameters=input_parameters,
        )
    )


@st.composite
def st_mm_psf_beads_processed_dataset(
    draw,
    processed=st.just(True),
    input_data=st_mm_psf_beads_input_data(),
    output=st_mm_psf_beads_output(),
    sample=st_mm_psf_beads_sample(),
    input_parameters=st_mm_psf_beads_input_parameters(),
) -> mm_schema.PSFBeadsDataset:
    sample = draw(sample)
    input_parameters = draw(input_parameters)
    return draw(
        st_mm_dataset(
            target_class=mm_schema.PSFBeadsDataset,
            processed=processed,
            input_data=input_data,
            output=output,
            sample=sample,
            input_parameters=input_parameters,
        )
    )