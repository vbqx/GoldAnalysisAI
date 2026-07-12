"""Run lifecycle — config, context, and archive replay.

Preferred imports::

    from src.run import RunConfig, get_run_config, load_bundle, archive_run

Legacy paths ``src.core.run_config``, ``src.core.run_context``, and
``src.data.run_archive`` remain as thin re-exports for compatibility.
"""

from src.run.archive import (
    allocate_run_id,
    archive_label,
    archive_run,
    export_archive_zip,
    import_archive_zip,
    inspect_run_archive,
    list_archives,
    load_archive_5m_bars,
    load_bundle,
)
from src.run.config import (
    RunConfig,
    apply_run_config,
    coerce_run_config,
    default_panel_run_config,
    run_config_for_mode,
    run_config_from_env,
    run_config_widget_state,
)
from src.run.context import (
    agent_mode,
    get_run_config,
    llm_narrative_enabled,
    reset_run_config,
    run_config_scope,
    set_run_config,
)

__all__ = [
    "RunConfig",
    "agent_mode",
    "allocate_run_id",
    "apply_run_config",
    "archive_label",
    "archive_run",
    "export_archive_zip",
    "import_archive_zip",
    "coerce_run_config",
    "default_panel_run_config",
    "get_run_config",
    "inspect_run_archive",
    "list_archives",
    "llm_narrative_enabled",
    "load_archive_5m_bars",
    "load_bundle",
    "reset_run_config",
    "run_config_for_mode",
    "run_config_from_env",
    "run_config_scope",
    "run_config_widget_state",
    "set_run_config",
]
