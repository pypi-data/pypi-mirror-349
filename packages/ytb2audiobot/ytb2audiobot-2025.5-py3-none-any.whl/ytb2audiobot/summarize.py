import json
import pathlib

import aiofiles
from ytb2audiobot.logger import logger
from ytb2audiobot.utils import run_command, format_time


async def read_json_async(file_path: pathlib.Path) -> dict:
    """Читает JSON-файл асинхронно."""
    try:
        async with aiofiles.open(file_path, mode='r') as f:
            content = await f.read()
            return json.loads(content)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f'❌ Error reading JSON. Summary: {e}')
        return {}


async def format_summary2timecodes(summary: dict) -> dict:
    if not summary or not isinstance(summary, dict):
        return {}

    chapters = summary.get("chapters", [])
    return {
        chapter.get("startTime", "unknown"): {
            "title": chapter.get("content", ""),
            "theses": [thesis.get("content", "") for thesis in chapter.get("theses", [])],
            "type": "summary",
        }
        for chapter in chapters if isinstance(chapter, dict)
    }


async def download_summary(movie_id: str, dir_path: str | pathlib.Path, language: str = 'en', skip: bool = False) -> dict:
    """Downloads and processes a movie summary.

    Args:
        movie_id (str): The movie's unique identifier.
        dir_path (Union[str, pathlib.Path]): Directory path for storing the summary.
        language (str, optional): Language code for the summary. Defaults to 'en'.
        skip (bool, optional): If True, skips downloading. Defaults to False.

    Returns:
        Dict[str, Any]: A dictionary of timecodes if successful, otherwise an empty dict.
    """
    if skip:
        return {}

    dir_path = pathlib.Path(dir_path)
    summarize_path = dir_path / f'{movie_id}-summary.json'

    # If summary file exists, read it
    if summarize_path.exists():
        try:
            return await format_summary2timecodes(await read_json_async(summarize_path))
        except Exception as e:
            logger.error(f'❌🧬 Error reading JSON summary: {e}')
            return {}

    # Construct and execute Node.js command

    command = f'ytb2summary --output-dir {dir_path.as_posix()} --language {language} {movie_id}'
    stdout, stderr, return_code = await run_command(command, timeout=20 * 60, throttle_delay=10)

    for line in stdout.splitlines():
        logger.debug(line)
    for line in stderr.splitlines():
        logger.error(line)

    if return_code != 0:
        logger.error(f"❌🧬 Error during summary download. Exit code: {return_code}")
        return {}

    if not summarize_path.exists():
        logger.error(f"❌🧬 Summary file not found: {summarize_path}")
        return {}

    # Read and process the summary file
    try:
        return await format_summary2timecodes(await read_json_async(summarize_path))
    except Exception as e:
        logger.error(f'❌🧬 Error reading JSON summary: {e}')
        return {}


def get_summary_txt_or_html(timecodes: dict, html_mode: bool = True) -> str:
    """Generates a formatted HTML summary from timecodes.

    Args:
        timecodes (Dict[int, Dict[str, Any]]): A dictionary where:
            - Keys are timestamps (int).
            - Values contain 'title' (str) and 'theses' (list of str).

    Returns:
        str: A formatted HTML summary.
    """
    summary = 'Summary'
    title = '{} - {}'
    if html_mode:
        summary = f'<b>{summary}</b>'
        title = f'<b>{title}</b>'

    return '\n'.join(
        [summary] +
        [''] +
        sum(
            [
                [title.format(format_time(time), timecode.get('title', 'Unknown Title'))] +
                [''] +
                [f' • {thesis}' for thesis in timecode.get('theses', [])] + ['']
                for time, timecode in timecodes.items()
            ],
            []
        )
    )