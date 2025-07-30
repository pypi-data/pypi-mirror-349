from hypothesis import strategies as st

from ..datamodel import microscopemetrics_schema as mm_schema


# Common
@st.composite
def st_mm_data_reference(
    draw,
    data_uri=st.uuids(),
    omero_host=st.from_regex(r"omero[0-9]{1,2}.example.org", fullmatch=True),
    omero_port=st.integers(min_value=4063, max_value=4064),
    omero_object_type=st.sampled_from(["IMAGE", "DATASET", "PROJECT"]),
    omero_object_id=st.integers(min_value=1),
) -> mm_schema.DataReference:
    return mm_schema.DataReference(
        data_uri=draw(data_uri),
        omero_host=draw(omero_host),
        omero_port=draw(omero_port),
        omero_object_type=draw(omero_object_type),
        omero_object_id=draw(omero_object_id),
    )


@st.composite
def st_mm_metrics_object(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256
    ),
    data_reference=st_mm_data_reference(),
) -> mm_schema.MetricsObject:
    return mm_schema.MetricsObject(
        name=draw(name),
        description=draw(description),
        data_reference=draw(data_reference),
    )


@st.composite
def st_mm_microscope(
    draw,
    metrics_object=st_mm_metrics_object(),
    microscope_type=st.sampled_from(["WIDEFIELD", "CONFOCAL", "STED", "SIM3D", "OTHER"]),
    manufacturer=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    model=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    serial_number=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    data_reference=st_mm_data_reference(),
) -> mm_schema.Microscope:
    metrics_object = draw(metrics_object)
    return mm_schema.Microscope(
        name=metrics_object.name,
        description=metrics_object.description,
        data_reference=draw(data_reference),
        microscope_type=draw(microscope_type),
        manufacturer=draw(manufacturer),
        model=draw(model),
        serial_number=draw(serial_number),
    )


@st.composite
def st_mm_experimenter(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    orcid=st.from_regex(r"[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}", fullmatch=True),
) -> mm_schema.Experimenter:
    return mm_schema.Experimenter(
        name=draw(name),
        orcid=draw(orcid),
    )


@st.composite
def st_mm_protocol(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256
    ),
    version=st.from_regex(r"[0-9]\.[0-9]\.[0-9]{3}", fullmatch=True),
    authors=st.lists(
        st_mm_experimenter(),
        min_size=1,
        max_size=5,
        unique_by=lambda experimenter: experimenter.orcid,
    ),
    url=st.uuids(),
) -> mm_schema.Protocol:
    return mm_schema.Protocol(
        name=draw(name),
        description=draw(description),
        version=draw(version),
        authors=draw(authors),
        url=draw(url),
    )


@st.composite
def st_mm_sample(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256
    ),
    preparation_protocol=st_mm_protocol(),
    manufacturer=st.text(min_size=1, max_size=32),
) -> mm_schema.Sample:
    return mm_schema.Sample(
        name=draw(name),
        description=draw(description),
        preparation_protocol=draw(preparation_protocol),
        manufacturer=draw(manufacturer),
    )


@st.composite
def st_mm_comment(
    draw,
    datetime=st.datetimes(),
    author=st_mm_experimenter(),
    text=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256
    ),
    comment_type=st.sampled_from(["ACQUISITION", "PROCESSING", "OTHER"]),
) -> mm_schema.Comment:
    return mm_schema.Comment(
        datetime=draw(datetime),
        author=draw(author),
        comment_type=draw(comment_type),
        text=draw(text),
    )


@st.composite
def st_mm_input_data(
    draw,
    input=st.just({"some_data": 42}),  # Input data must contain something
) -> mm_schema.MetricsInputData:
    return mm_schema.MetricsInputData(**draw(input))

@st.composite
def st_mm_input_parameters(
    draw,
    input=st.just({}),
) -> mm_schema.MetricsInputParameters:
    return mm_schema.MetricsInputParameters(**draw(input))

@st.composite
def st_mm_key_measurement(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256
    ),
) -> mm_schema.KeyMeasurements:
    return mm_schema.KeyMeasurements(
        name=draw(name),
        description=draw(description),
    )

@st.composite
def st_mm_output(
    draw,
    processing_application=st.just("MicroscopeMetrics"),
    processing_version=st.just("0.1.0"),
    processing_entity=st.just("MicroscopeMetricsAnalysis"),
    processing_datetime=st.datetimes(),
    processing_log=st.text(),
    key_measurement=st_mm_key_measurement(),
    warnings=st.lists(st.text(), max_size=5),
    errors=st.lists(st.text(), max_size=5),
    comment=st_mm_comment(),
) -> mm_schema.MetricsOutput:
    return mm_schema.MetricsOutput(
        processing_application=draw(processing_application),
        processing_version=draw(processing_version),
        processing_entity=draw(processing_entity),
        processing_datetime=draw(processing_datetime),
        processing_log=draw(processing_log),
        key_measurements=draw(key_measurement),
        warnings=draw(warnings),
        errors=draw(errors),
        comment=draw(comment),
    )


@st.composite
def st_mm_dataset(
    draw,
    target_class=None,
    metrics_object=st_mm_metrics_object(),
    microscope=st_mm_microscope(),
    experimenter=st_mm_experimenter(),
    acquisition_datetime=st.datetimes(),
    processed=st.booleans(),
    input_data=st_mm_input_data(),
    output=st_mm_output(),
    **kwargs,
) -> mm_schema.MetricsDataset:
    metrics_object = draw(metrics_object)
    processed = draw(processed)
    output = draw(output) if processed else None
    
    if target_class is None:
        return mm_schema.MetricsDataset(
            name=metrics_object.name,
            description=metrics_object.description,
            data_reference=metrics_object.data_reference,
            microscope=draw(microscope),
            experimenter=draw(experimenter),
            acquisition_datetime=draw(acquisition_datetime),
            processed=processed,
            input_data=draw(input_data),
            output=output,
        )
    else:
        return target_class(
            name=metrics_object.name,
            description=metrics_object.description,
            data_reference=metrics_object.data_reference,
            microscope=draw(microscope),
            experimenter=draw(experimenter),
            acquisition_datetime=draw(acquisition_datetime),
            processed=processed,
            input_data=draw(input_data),
            output=output,
            **kwargs,
        )


# Data sources
@st.composite
def st_mm_image(
    draw,
    metrics_object=st_mm_metrics_object(),
    voxel_size_xy_micron=st.floats(min_value=0.1, max_value=1.0),
    voxel_size_z_micron=st.floats(min_value=0.3, max_value=3.0),
    shape=st.tuples(
        st.integers(min_value=1, max_value=20),  # T
        st.integers(min_value=1, max_value=100),  # Z
        st.integers(min_value=256, max_value=1024),  # Y
        st.integers(min_value=256, max_value=1024),  # X
        st.integers(min_value=1, max_value=5),  # C
    ),
    acquisition_datetime=st.datetimes(),
    data=None,
) -> mm_schema.Image:
    metrics_object = draw(metrics_object)

    if data is None:
        shape = draw(shape)
    else:
        try:
            shape = data.shape
        except AttributeError:
            shape = draw(shape)
        except Exception as e:
            raise e

    voxel_size_xy_micron = draw(voxel_size_xy_micron)

    return mm_schema.Image(
        name=metrics_object.name,
        description=metrics_object.description,
        data_reference=metrics_object.data_reference,
        voxel_size_x_micron=voxel_size_xy_micron,
        voxel_size_y_micron=voxel_size_xy_micron,
        voxel_size_z_micron=draw(voxel_size_z_micron),
        shape_t=shape[0],
        shape_z=shape[1],
        shape_y=shape[2],
        shape_x=shape[3],
        shape_c=shape[4],
        array_data=data,
        acquisition_datetime=draw(acquisition_datetime),
    )


@st.composite
def st_mm_color(
    draw,
    r=st.integers(min_value=0, max_value=255),
    g=st.integers(min_value=0, max_value=255),
    b=st.integers(min_value=0, max_value=255),
    alpha=st.integers(min_value=0, max_value=255),
) -> mm_schema.Color:
    return mm_schema.Color(r=draw(r), g=draw(g), b=draw(b), alpha=draw(alpha))


@st.composite
def st_mm_point(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256),
    z=st.floats(min_value=0.0, max_value=30.0),
    c=st.integers(min_value=0, max_value=5),
    t=st.integers(min_value=0, max_value=5),
    fill_color=st_mm_color(),
    stroke_color=st_mm_color(),
    stroke_width=st.integers(min_value=1, max_value=5),
    x=st.floats(min_value=0.0, max_value=1024.0),
    y=st.floats(min_value=0.0, max_value=1024.0),
) -> mm_schema.Point:
    return mm_schema.Point(
        name=draw(name),
        description=draw(description),
        z=draw(z),
        c=draw(c),
        t=draw(t),
        fill_color=draw(fill_color),
        stroke_color=draw(stroke_color),
        stroke_width=draw(stroke_width),
        x=draw(x),
        y=draw(y),
    )


@st.composite
def st_mm_line(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256),
    z=st.floats(min_value=0.0, max_value=30.0),
    c=st.integers(min_value=0, max_value=5),
    t=st.integers(min_value=0, max_value=5),
    fill_color=st_mm_color(),
    stroke_color=st_mm_color(),
    stroke_width=st.integers(min_value=1, max_value=5),
    x1=st.floats(min_value=0.0, max_value=1024.0),
    y1=st.floats(min_value=0.0, max_value=1024.0),
    x2=st.floats(min_value=0.0, max_value=1024.0),
    y2=st.floats(min_value=0.0, max_value=1024.0),
) -> mm_schema.Line:
    return mm_schema.Line(
        name=draw(name),
        description=draw(description),
        z=draw(z),
        c=draw(c),
        t=draw(t),
        fill_color=draw(fill_color),
        stroke_color=draw(stroke_color),
        stroke_width=draw(stroke_width),
        x1=draw(x1),
        y1=draw(y1),
        x2=draw(x2),
        y2=draw(y2),
    )


@st.composite
def st_mm_rectangle(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256),
    z=st.floats(min_value=0.0, max_value=30.0),
    c=st.integers(min_value=0, max_value=5),
    t=st.integers(min_value=0, max_value=5),
    fill_color=st_mm_color(),
    stroke_color=st_mm_color(),
    stroke_width=st.integers(min_value=1, max_value=5),
    x=st.floats(min_value=0.0, max_value=1024.0),
    y=st.floats(min_value=0.0, max_value=1024.0),
    w=st.floats(min_value=0.0, max_value=1024.0),
    h=st.floats(min_value=0.0, max_value=1024.0),
) -> mm_schema.Rectangle:
    return mm_schema.Rectangle(
        name=draw(name),
        description=draw(description),
        z=draw(z),
        c=draw(c),
        t=draw(t),
        fill_color=draw(fill_color),
        stroke_color=draw(stroke_color),
        stroke_width=draw(stroke_width),
        x=draw(x),
        y=draw(y),
        w=draw(w),
        h=draw(h),
    )


@st.composite
def st_mm_ellipse(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256),
    z=st.floats(min_value=0.0, max_value=30.0),
    c=st.integers(min_value=0, max_value=5),
    t=st.integers(min_value=0, max_value=5),
    fill_color=st_mm_color(),
    stroke_color=st_mm_color(),
    stroke_width=st.integers(min_value=1, max_value=5),
    x=st.floats(min_value=0.0, max_value=1024.0),
    y=st.floats(min_value=0.0, max_value=1024.0),
    w=st.floats(min_value=0.0, max_value=1024.0),
    h=st.floats(min_value=0.0, max_value=1024.0),
) -> mm_schema.Ellipse:
    return mm_schema.Ellipse(
        name=draw(name),
        description=draw(description),
        z=draw(z),
        c=draw(c),
        t=draw(t),
        fill_color=draw(fill_color),
        stroke_color=draw(stroke_color),
        stroke_width=draw(stroke_width),
        x=draw(x),
        y=draw(y),
        w=draw(w),
        h=draw(h),
    )


@st.composite
def st_mm_vertex(
    draw,
    x=st.floats(min_value=0.0, max_value=1024.0),
    y=st.floats(min_value=0.0, max_value=1024.0),
) -> mm_schema.Vertex:
    return mm_schema.Vertex(x=draw(x), y=draw(y))


@st.composite
def st_mm_polygon(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256),
    z=st.floats(min_value=0.0, max_value=30.0),
    c=st.integers(min_value=0, max_value=5),
    t=st.integers(min_value=0, max_value=5),
    fill_color=st_mm_color(),
    stroke_color=st_mm_color(),
    stroke_width=st.integers(min_value=1, max_value=5),
    vertexes=st.lists(
        st_mm_vertex(), min_size=3, max_size=10
    ),
    is_open=st.booleans(),
) -> mm_schema.Polygon:
    return mm_schema.Polygon(
        name=draw(name),
        description=draw(description),
        z=draw(z),
        c=draw(c),
        t=draw(t),
        fill_color=draw(fill_color),
        stroke_color=draw(stroke_color),
        stroke_width=draw(stroke_width),
        vertexes=draw(vertexes),
        is_open=draw(is_open),
    )


@st.composite
def st_mm_shape(
    draw,
    name=st.text(
        alphabet=st.characters(codec="latin-1"), min_size=1, max_size=32
    ),
    description=st.text(alphabet=st.characters(codec="latin-1"), min_size=1, max_size=256),
    z=st.floats(min_value=0.0, max_value=30.0),
    c=st.integers(min_value=0, max_value=5),
    t=st.integers(min_value=0, max_value=5),
    fill_color=st_mm_color(),
    stroke_color=st_mm_color(),
    stroke_width=st.integers(min_value=1, max_value=5),
) -> mm_schema.Shape:
    params = {
        "name": name,
        "description": description,
        "z": z,
        "c": c,
        "t": t,
        "fill_color": fill_color,
        "stroke_color": stroke_color,
        "stroke_width": stroke_width,
    }

    shape = st.one_of(
        [
            st_mm_point(**params),
            st_mm_line(**params),
            st_mm_rectangle(**params),
            st_mm_ellipse(**params),
            st_mm_polygon(**params),
        ]
    )

    return draw(shape)


@st.composite
def st_mm_roi(
    draw,
    metrics_object=st_mm_metrics_object(),
    images=st.lists(st_mm_image(), min_size=1, max_size=2),
    shapes=st.lists(
        st_mm_shape(), min_size=1, max_size=5, unique_by=lambda shape: shape.name
    ),
) -> mm_schema.Roi:
    shapes = draw(shapes)
    metrics_object = draw(metrics_object)
    images = draw(images)
    image_links = [image.data_reference for image in images]
    return mm_schema.Roi(
        name=metrics_object.name,
        description=metrics_object.description,
        data_reference=metrics_object.data_reference,
        linked_references=image_links,
        points=[shape for shape in shapes if isinstance(shape, mm_schema.Point)],
        lines=[shape for shape in shapes if isinstance(shape, mm_schema.Line)],
        rectangles=[shape for shape in shapes if isinstance(shape, mm_schema.Rectangle)],
        ellipses=[shape for shape in shapes if isinstance(shape, mm_schema.Ellipse)],
        polygons=[shape for shape in shapes if isinstance(shape, mm_schema.Polygon)],
    )
