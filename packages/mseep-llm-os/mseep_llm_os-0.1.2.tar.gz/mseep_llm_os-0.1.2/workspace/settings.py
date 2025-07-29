from pathlib import Path

from phi.workspace.settings import WorkspaceSettings

#
# -*- Define workspace settings using a WorkspaceSettings object
# these values can also be set using environment variables or a .env file
#
ws_settings = WorkspaceSettings(
    # Workspace name: used for naming resources
    ws_name="lyraios",
    # Path to the workspace root
    ws_root=Path(__file__).parent.parent.resolve(),
    # -*- Dev settings
    dev_env="dev",
    # -*- Dev Apps
    dev_app_enabled=True,
    dev_db_enabled=True,
    dev_api_enabled=True,
    # -*- Production settings
    prd_env="prd",
    # -*- Production Apps
    prd_app_enabled=True,
    prd_db_enabled=True,
    prd_api_enabled=True,
    # Name of the image to build/push/use
    image_name="lyraios"
)
