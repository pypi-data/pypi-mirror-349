from lat_lon_parser import parse
from loguru import logger


def batch_query(method, id_list, batch_size=50, id_param="id__in", **kwargs):
    """
    Execute a query in batches to avoid Request-URI Too Long errors.

    Args:
        method: The pynetbox query method to call (e.g., nb.dcim.interfaces.filter)
        id_list: List of IDs to split into batches
        batch_size: Maximum number of IDs per batch
        id_param: Parameter name for the ID filter (default: 'id__in')
        **kwargs: Additional filter parameters to pass to the query method

    Returns:
        List of results from all batches combined
    """
    results = []
    total_batches = (len(id_list) + batch_size - 1) // batch_size

    for i in range(0, len(id_list), batch_size):
        batch = id_list[i : i + batch_size]
        logger.debug(f"Processing batch {(i // batch_size) + 1}/{total_batches} with {len(batch)} items")

        # Create params dict with the batch of IDs
        batch_params = {id_param: batch}
        # Add any additional filter parameters
        batch_params.update(kwargs)

        # Execute the query and extend the results
        batch_results = list(method(**batch_params))
        results.extend(batch_results)

    logger.debug(f"Query completed with {len(results)} total results")
    return results


def build_tenant_name(client_id, name):
    if client_id and name:
        return f"{client_id} - {name}"[0:100].strip()
    elif client_id:
        return f"{client_id}"
    else:
        return f"{name}"[0:100].strip()


def sanitize_lat_lon(lat_or_lon: str) -> float:
    """
    Gets latitude or longitude string and returns float with 6 decimal places
    This format is required in Netbox
    """
    if not lat_or_lon:
        return None

    try:
        result = parse(lat_or_lon)
    except ValueError:
        return None

    if result:
        return round(result, 6)
    else:
        return None
