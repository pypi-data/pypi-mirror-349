import uuid
import math

from chunk_metadata_adapter import (
    ChunkMetadataBuilder,
    ChunkStatus,
)

TOL = 1e-6


def test_extended_metrics_round_trip():
    """Ensure new metric fields are preserved through conversions."""
    builder = ChunkMetadataBuilder(project="MetricsProject")
    source_id = str(uuid.uuid4())

    # Build semantic chunk with explicit metrics
    semantic_chunk = builder.build_semantic_chunk(
        text="Metrics example",
        language="text",
        type="Message",
        source_id=source_id,
        coverage=0.9,
        cohesion=0.8,
        boundary_prev=0.7,
        boundary_next=0.6,
    )

    assert math.isclose(semantic_chunk.metrics.coverage, 0.9, abs_tol=TOL)
    assert math.isclose(semantic_chunk.metrics.cohesion, 0.8, abs_tol=TOL)
    assert math.isclose(semantic_chunk.metrics.boundary_prev, 0.7, abs_tol=TOL)
    assert math.isclose(semantic_chunk.metrics.boundary_next, 0.6, abs_tol=TOL)

    # Convert to flat then back
    flat_dict = builder.semantic_to_flat(semantic_chunk)
    restored_chunk = builder.flat_to_semantic(flat_dict)

    assert math.isclose(restored_chunk.metrics.coverage, 0.9, abs_tol=TOL)
    assert math.isclose(restored_chunk.metrics.cohesion, 0.8, abs_tol=TOL)
    assert math.isclose(restored_chunk.metrics.boundary_prev, 0.7, abs_tol=TOL)
    assert math.isclose(restored_chunk.metrics.boundary_next, 0.6, abs_tol=TOL)


def test_status_case_insensitive():
    """Verify that status strings are parsed case-insensitively."""
    builder = ChunkMetadataBuilder()
    chunk_upper = builder.build_semantic_chunk(
        text="Status TEST",
        language="text",
        type="Log",
        status="RAW"  # uppercase string
    )
    assert chunk_upper.status == ChunkStatus.RAW

    # Direct enum construction should also work
    assert ChunkStatus("CLEANED") == ChunkStatus.CLEANED 