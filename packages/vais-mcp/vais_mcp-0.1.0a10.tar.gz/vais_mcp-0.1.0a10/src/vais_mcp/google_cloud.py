from typing import List, Optional

from google import auth
from google.auth import impersonated_credentials
from google.oauth2 import service_account
from loguru import logger


def get_credentials(
    project_id: str,
    impersonate_service_account: Optional[str],
    use_mounted_sa_key: bool,
    container_sa_key_path: str,
    scopes: Optional[List[str]] = None,
    lifetime: Optional[int] = None,
) -> auth.credentials.Credentials:
    """Get the credentials based on settings."""
    logger.debug(
        "Getting credentials:"
        f"Project: {project_id}, "
        f"Impersonate SA: {impersonate_service_account}, "
        f"Use Mounted SA Key: {use_mounted_sa_key}, "
        f"Container SA Key Path: {container_sa_key_path}"
    )

    current_impersonate_sa = impersonate_service_account

    if current_impersonate_sa:
        logger.info(f"Impersonation is configured for SA: {current_impersonate_sa}")
        source_sa_path_for_impersonation = (
            container_sa_key_path if use_mounted_sa_key else None
        )
        if source_sa_path_for_impersonation:
            logger.info(
                f"Using SA key at {source_sa_path_for_impersonation} (mounted in container) as source for impersonation."
            )
        else:
            logger.info(
                "No local SA key path provided for impersonation source. Falling back to ADC for source credentials."
            )
        return get_impersonate_credentials(
            target_sa_email=current_impersonate_sa,
            source_sa_key_path=source_sa_path_for_impersonation,
            quota_project_id=project_id,
            scopes=scopes,
            lifetime=lifetime,
        )

    logger.info("No impersonation. Using direct credentials.")
    if use_mounted_sa_key:
        actual_key_path_in_container = container_sa_key_path
        logger.info(
            f"Using service account key from: {actual_key_path_in_container} (mounted in container)"
        )
        try:
            credentials = service_account.Credentials.from_service_account_file(
                actual_key_path_in_container,
                scopes=scopes
                if scopes
                else ["https://www.googleapis.com/auth/cloud-platform"],
            )
            if project_id and hasattr(credentials, "with_quota_project"):
                credentials = credentials.with_quota_project(project_id)
            logger.debug("Successfully loaded credentials from SA key file.")
            return credentials
        except FileNotFoundError as e:
            logger.error(
                f"Service account key file not found: {actual_key_path_in_container}. Ensure a SA key file is mounted and USE_MOUNTED_SA_KEY is true."
            )
            raise FileNotFoundError(
                f"Service account key file not found: {actual_key_path_in_container}. Ensure a SA key file is mounted and USE_MOUNTED_SA_KEY is true. Original error: {e}"
            ) from e
        except Exception as e:
            logger.error(
                f"Failed to load credentials from SA key file {actual_key_path_in_container}: {e}"
            )
            raise Exception(
                f"Failed to load credentials from SA key file {actual_key_path_in_container}. Original error: {e}"
            ) from e

    logger.info("USE_MOUNTED_SA_KEY is false. Falling back to default ADC.")
    return get_default_credentials(project_id)


def get_default_credentials(
    project_id: Optional[str] = None,
) -> auth.credentials.Credentials:
    """Get the default credentials (ADC)."""
    logger.debug(f"Getting default ADC. Quota project: {project_id}")
    try:
        if project_id is not None:
            credentials, _ = auth.default(quota_project_id=project_id)
        else:
            credentials, _ = auth.default()
        logger.debug("Successfully obtained default ADC.")
        return credentials
    except Exception as e:
        logger.error(f"Failed to get default ADC: {e}")
        raise Exception(f"Failed to obtain default ADC: {e}") from e


def get_impersonate_credentials(
    target_sa_email: str,
    source_sa_key_path: Optional[str] = None,
    quota_project_id: Optional[str] = None,
    scopes: Optional[List[str]] = None,
    lifetime: Optional[int] = None,
) -> impersonated_credentials.Credentials:
    """Get impersonated credentials."""
    logger.debug(
        f"Getting impersonated credentials for target SA: {target_sa_email}. "
        f"Source SA key path: {source_sa_key_path}, Quota project: {quota_project_id}"
    )

    if scopes is None:
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    if lifetime is None:
        lifetime = 3600

    source_credentials: auth.credentials.Credentials

    if source_sa_key_path:
        logger.info(f"Using source SA key from {source_sa_key_path} for impersonation.")
        try:
            source_credentials = service_account.Credentials.from_service_account_file(
                source_sa_key_path,
            )
            if quota_project_id and hasattr(source_credentials, "with_quota_project"):
                source_credentials = source_credentials.with_quota_project(
                    quota_project_id
                )
            logger.debug(
                "Successfully loaded source credentials from SA key file for impersonation."
            )
        except FileNotFoundError as e:
            logger.error(
                f"Source SA key file not found for impersonation: {source_sa_key_path}"
            )
            raise FileNotFoundError(
                f"Source SA key file not found for impersonation: {source_sa_key_path}. Original error: {e}"
            ) from e
        except Exception as e:
            logger.error(
                f"Failed to load source SA key {source_sa_key_path} for impersonation: {e}"
            )
            raise Exception(
                f"Failed to load source SA key {source_sa_key_path} for impersonation. Original error: {e}"
            ) from e
    else:
        logger.info(
            "No source SA key path provided for impersonation. Falling back to default ADC as source credentials."
        )
        try:
            if quota_project_id is not None:
                source_credentials, _ = auth.default(quota_project_id=quota_project_id)
            else:
                source_credentials, _ = auth.default()
            logger.debug(
                "Successfully obtained default ADC as source for impersonation."
            )
        except Exception as e:
            logger.error(f"Failed to get default ADC as source for impersonation: {e}")
            raise Exception(
                f"Failed to get default ADC as source for impersonation. Original error: {e}"
            ) from e

    logger.debug(f"Creating impersonated credentials for target: {target_sa_email}")
    try:
        target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=target_sa_email,
            target_scopes=scopes,
            lifetime=lifetime,
        )
        logger.info("Successfully created impersonated credentials.")
        return target_credentials
    except Exception as e:
        logger.error(
            f"Failed to create impersonated credentials for {target_sa_email}: {e}"
        )
        raise Exception(
            f"Failed to create impersonated credentials for {target_sa_email}. Original error: {e}"
        ) from e
