import asyncio
import inspect
import math
import pathlib
import pprint
import re
from itertools import islice
from string import Template

import yt_dlp
from aiogram import Bot
from aiogram.types import FSInputFile, BufferedInputFile, Message
from ytbtimecodes.timecodes import extract_timecodes, timedelta_from_seconds, standardize_time_format

from ytb2audiobot import config
from ytb2audiobot.audio_duration import get_duration
from ytb2audiobot.audio_mixer import mix_audio_m4a
from ytb2audiobot.config import YT_DLP_OPTIONS_DEFAULT, SEGMENT_REBALANCE_TO_FIT_TIMECODES
from ytb2audiobot.segmentation import segments_verification, get_segments_by_duration, \
    add_paddings_to_segments, make_magic_tail, get_segments_by_timecodes_from_dict, rebalance_segments_long_timecodes
from ytb2audiobot.subtitles import get_subtitles_here, highlight_words_file_text
from ytb2audiobot.logger import logger
from ytb2audiobot.download import download_thumbnail_from_download, \
    make_split_audio_second, get_chapters, get_timecodes_dict, filter_timecodes_within_bounds, \
    get_timecodes_formatted_text, download_audio_from_download, empty
from ytb2audiobot.summarize import download_summary, get_summary_txt_or_html
from ytb2audiobot.translate import make_translate
from ytb2audiobot.utils import seconds2humanview, capital2lower, \
    predict_downloading_time, get_data_dir, get_big_youtube_move_id, trim_caption_to_telegram_send, get_file_size, \
    get_short_youtube_url, remove_files_starting_with_async, split_big_text_pretty


async def make_subtitles(
        bot: Bot,
        sender_id: int,
        url: str = '',
        word: str = '',
        reply_message_id: int | None = None,
        editable_message_id: int | None = None):
    info_message = await bot.edit_message_text(
        chat_id=sender_id,
        message_id=editable_message_id,
        text = '⏳ Preparing…'
    ) if editable_message_id else await bot.send_message(
        chat_id=sender_id,
        reply_to_message_id=reply_message_id,
        text = '⏳ Preparing…')

    info_message = await info_message.edit_text('⏳ Fetching subtitles…')

    if not (movie_id := get_big_youtube_move_id(url)):
        await info_message.edit_text('❌ Unable to extract a valid YouTube movie ID from the provided URL.')
        return

    text = await get_subtitles_here(url, word)

    caption = f'✏️ Subtitles\n\n{get_short_youtube_url(movie_id)}'
    if word:
        caption += f'\n\n'
        caption += f'🔎 Search word: {word}' if text else '🔦 Nothing Found! 😉'

    caption = caption + '\n\n' + text

    if len(caption) < config.TELEGRAM_MAX_MESSAGE_TEXT_SIZE:
        await bot.send_message(chat_id=sender_id, text=caption, parse_mode='HTML')
    else:
        await bot.send_document(
            chat_id=sender_id,
            caption=caption[:190].strip() + '\n...',
            document=BufferedInputFile(
                filename=f'subtitles-{movie_id}.txt',
                file=highlight_words_file_text(text, word).encode('utf-8')))
    await info_message.delete()


def get_yt_dlp_options(override_options=None):
    if override_options is None:
        override_options = {}

    options = YT_DLP_OPTIONS_DEFAULT

    options.update(override_options)

    rows = []

    for key, value in options.items():
        if isinstance(value, bool):
            if value:
                rows.append(f'--{key}')
            else:
                continue
        else:
            rows.append(f'--{key} {value}')

    return ' '.join(rows)

async def retry_job_downloading(bot: Bot,
        sender_id: int,
        reply_to_message_id: int | None = None,
        message_text: str = '',
        info_message_id: int | None = None,
        configurations=None):


    start_time = asyncio.get_event_loop().time()
    end_time = start_time + config.RETRY_JOB_MAX_RETRY_DURATION

    while asyncio.get_event_loop().time() < end_time:
        try:
            await job_downloading(bot, sender_id, reply_to_message_id, message_text, info_message_id, configurations)
        except Exception as e:
            logger.error(f"Error during download attempt: {e}")

        await asyncio.sleep(config.RETRY_JOB_ATTEMPT_INTERVAL)


async def fetch_yt_info(movie_id: str, ydl_opts = None):
    default_ydl_opts = {
        'logtostderr': False,  # Avoids logging to stderr, logs to the logger instead
        'quiet': True,  # Suppresses default output,
        'nocheckcertificate': True,
        'no_warnings': True,
        'skip_download': True,}

    # Use provided ydl_opts or fall back to default options
    ydl_opts = ydl_opts or default_ydl_opts

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    yt_info = await asyncio.to_thread(ydl.extract_info, f"https://www.youtube.com/watch?v={movie_id}", download=False)
    return yt_info

async def magic_sleep_against_flood(index: int, total_item_count: int):
    if index != 0 and index != total_item_count - 1:
        sleep_duration = math.floor(8 * math.log10(total_item_count+ 1))
        logger.debug(f'💤😴 Sleeping for {sleep_duration} seconds.')
        await asyncio.sleep(sleep_duration)

async def job_downloading(
        bot: Bot,
        sender_id: int,
        reply_to_message_id: int | None = None,
        message_text: str = '',
        info_message_id: int | None = None,
        configurations=None):
    if configurations is None:
        configurations = {}

    movie_id = get_big_youtube_move_id(message_text)
    if not movie_id:
        return

    mid = movie_id + ' 🔹'
    logger.debug(f'🌀 {mid} START-JOB: configurations: {configurations}')

    # Inverted logic refactor
    info_message = await bot.edit_message_text(
        chat_id=sender_id,
        message_id=info_message_id,
        text='⏳ Preparing…'
    ) if info_message_id else await bot.send_message(
        chat_id=sender_id,
        text='⏳ Preparing…',
        reply_to_message_id=reply_to_message_id
    )

    try:
        yt_info = await fetch_yt_info(movie_id,  {
            'logtostderr': False,  # Avoids logging to stderr, logs to the logger instead
            'quiet': True,  # Suppresses default output,
            'nocheckcertificate': True,
            'no_warnings': True,
            'skip_download': True,})
    except Exception as e:
        logger.error(f'❌ {mid} Unable to extract YT-DLP info. \n\n{e}')
        await info_message.edit_text('❌ Unable to extract YT-DLP info for this movie.')
        return

    #logger.info(yt_info)

    if yt_info.get('is_live'):
        logger.info('❌🎬💃 This movie is now live and unavailable for download. Try...')
        #return

    if not yt_info.get('title') or not yt_info.get('duration'):
        await info_message.edit_text('❌🎬💔 No title or duration information available for this video. Please try again later.  Exit.')
        return


    if not yt_info.get('filesize_approx', ''):
        logger.info('❌🛰 This movie is currently live, but it may be in the process of being updated. Try...')
        #return

    if not any(format_item.get('filesize') is not None for format_item in yt_info.get('formats', [])):
        logger.info('❌🎬🤔 The audio file for this video is unavailable due to an unknown reason. Try...')
        #return

    action = configurations.get('action', '')

    title = yt_info.get('title', '')
    description = yt_info.get('description', '')
    author = yt_info.get('uploader', '')
    duration = yt_info.get('duration')
    language = yt_info.get('language', '')

    yt_dlp_options = get_yt_dlp_options()

    bitrate = config.AUDIO_QUALITY_BITRATE

    data_dir = get_data_dir()
    audio_path = data_dir / f'{movie_id}-{bitrate}.m4a'
    thumbnail_path = data_dir / f'{movie_id}-thumbnail.jpg'
    audio_path_translate_original = data_dir / f'{movie_id}-transl-ru-{bitrate}-original.m4a'
    audio_path_translate_final = data_dir / f'{movie_id}-transl-ru-{bitrate}.m4a'

    # Output items
    reply_output = reply_to_message_id if config.REPLY_TO_ORIGINAL else None

    caption_head_output = config.CAPTION_HEAD_TEMPLATE.safe_substitute(
        movieid=movie_id,
        title=capital2lower(title),
        author=capital2lower(author))
    caption_head_additional_output = ''

    predict_time_text = seconds2humanview(predict_downloading_time(yt_info.get('duration')))

    summary_skip_download = True

    if action == config.ACTION_NAME_FORCE_REDOWNLOAD:
        logger.debug(f'🐘 {mid} Force Re-Download')
        await  remove_files_starting_with_async(data_dir, f'{movie_id}')

    elif action == config.ACTION_NAME_BITRATE_CHANGE:
        if (new_bitrate := configurations.get('bitrate')) in config.BITRATE_VALUES:
            bitrate = new_bitrate
        yt_dlp_options = get_yt_dlp_options({'audio-quality': bitrate})

    elif action == config.ACTION_NAME_SLICE:
        start_time = str(configurations.get('slice_start_time'))
        end_time = str(configurations.get('slice_end_time'))

        start_time_hhmmss = standardize_time_format(timedelta_from_seconds(start_time))
        end_time_hhmmss = standardize_time_format(timedelta_from_seconds(end_time))

        yt_dlp_options += f' --postprocessor-args \"-ss {start_time_hhmmss} -t {end_time_hhmmss}\"'

        caption_head_additional_output += '\n\n'
        caption_head_additional_output += config.CAPTION_SLICE.substitute(
            start_time=standardize_time_format(timedelta_from_seconds(str(configurations.get('slice_start_time')))),
            end_time=standardize_time_format(timedelta_from_seconds(str(configurations.get('slice_end_time')))))

    elif action == config.ACTION_NAME_TRANSLATE:
        if language == 'ru':
            await info_message.edit_text('⏳🌎 This movie is still in Russian. Standard download…')
            action = ''
        else:
            caption_head_output = f'🌎 Translation\n\n{caption_head_output}'
            # todo: add time handling
            predict_time_text = 'unknown [🌎 Translation is starting. It may take a lot of time…]'

    elif action == config.ACTION_NAME_SUMMARIZE:
        logger.debug(f'🧬 {mid} Action == SUMMARIZE!')

        info_message = await info_message.edit_text(f'⏳🧬 Summarize processing…')
        await asyncio.sleep(config.DELAY_LESSE_SECOND)

        try:
            tasks = [
                asyncio.create_task(
                    download_summary(movie_id=movie_id, language=language, dir_path=data_dir))]

            result = await asyncio.wait_for(
                timeout=config.KILL_JOB_DOWNLOAD_TIMEOUT_SEC,
                fut=asyncio.gather(*tasks))
        except asyncio.TimeoutError:
            logger.error(f'❌🧬 {mid} TimeoutError occurred during Single Summery().')
            await info_message.edit_text('❌🧬 TimeoutError occurred during Single Summery().')
            return
        except Exception as err:
            logger.error(f'❌🧬 {mid} Error occurred during Single Summery().\n\n{err}')
            await info_message.edit_text('❌🧬 Error occurred during Single Summery().')
            return

        timecodes_with_summary = result[0]

        if not timecodes_with_summary:
            await info_message.edit_text('🧬💔 Failed to create the summary. Please try again later.')
            return

        caption_summary = Template(caption_head_output).safe_substitute(
            partition='',
            duration=standardize_time_format(timedelta_from_seconds(duration + 1)),
            content=get_summary_txt_or_html(timecodes_with_summary),
            additional='')

        if len(caption_summary) < config.TELEGRAM_MAX_CAPTION_TEXT_SIZE:
            await bot.send_message(chat_id=sender_id, text=caption_summary, disable_web_page_preview=True)
        else:
            caption_summary = Template(caption_head_output).safe_substitute(
                partition='',
                duration=standardize_time_format(timedelta_from_seconds(duration + 1)),
                content=get_summary_txt_or_html(dict(islice(timecodes_with_summary.items(), 1))),
                additional='')

            caption_summary = caption_summary[:(config.TELEGRAM_MAX_CAPTION_TEXT_SIZE - 8)].strip() + '\n...'

            file_text = get_summary_txt_or_html(timecodes_with_summary, html_mode=False)

            await bot.send_document(
                chat_id=sender_id,
                caption=caption_summary,
                document=BufferedInputFile(filename=f'summary-{movie_id}.txt', file=file_text.encode('utf-8')))

        await info_message.delete()
        return

    info_message = await info_message.edit_text(f'⏳ Downloading ~ {predict_time_text}…')

    timecodes_raw = extract_timecodes(description)

    timecodes = get_timecodes_dict(timecodes_raw)

    chapters = get_chapters(yt_info.get('chapters', []))
    timecodes.update(chapters)

    if not timecodes:
        summary_skip_download = False

    # todo add depend on predict

    # Run tasks with timeout
    async def handle_download():
        try:
            _tasks = [
                asyncio.create_task(
                    download_audio_from_download(movie_id=movie_id, output_path=audio_path, options=yt_dlp_options)),
                asyncio.create_task(
                    download_thumbnail_from_download(movie_id=movie_id, output_path=thumbnail_path)),
                asyncio.create_task(
                    empty()),
                asyncio.create_task(
                    download_summary(movie_id=movie_id, language=language, dir_path=data_dir, skip=summary_skip_download))]

            if action == config.ACTION_NAME_TRANSLATE:
                _tasks[2] = (asyncio.create_task(
                    make_translate(movie_id=movie_id, output_path=audio_path_translate_original,
                                   timeout=config.KILL_JOB_DOWNLOAD_TIMEOUT_SEC)))
            _result = await asyncio.wait_for(
                timeout=config.KILL_JOB_DOWNLOAD_TIMEOUT_SEC,
                fut=asyncio.gather(*_tasks))
            return _result
        except asyncio.TimeoutError:
            logger.error(f'❌ {mid} TimeoutError occurred during download_processing().')
            await info_message.edit_text('❌ TimeoutError occurred during download_processing().')
            return None, None
        except Exception as err:
            logger.error(f'❌ {mid} Error occurred during download_processing().\n\n{err}')
            await info_message.edit_text('❌ Error occurred during download_processing().')
            return None, None

    audio_path, thumbnail_path, audio_path_translate_original, summary = await handle_download()

    if audio_path is None:
        logger.error(f'❌ {mid} audio_path is None after downloading. Exiting.')
        await info_message.edit_text('❌ Error: audio_path is None after downloading. Exiting.')
        return

    audio_path = pathlib.Path(audio_path)
    if not audio_path.exists():
        logger.error(f'❌ {mid} audio_path does not exist after downloading. Exiting.')
        await info_message.edit_text('❌ Error: audio_path does not exist after downloading. Exiting.')
        return

    if thumbnail_path is not None:
        thumbnail_path = pathlib.Path(thumbnail_path)
        if not thumbnail_path.exists():
            thumbnail_path = None

    if action == config.ACTION_NAME_TRANSLATE:
        if audio_path_translate_original is None:
            logger.error(f'❌ {mid} audio_path_translate_original is None after downloading. Exiting.')
            await info_message.edit_text('❌ Error: audio_path_translate_original is None after downloading. Exiting.')
            return

        if configurations.get('overlay') == 0.0:
            audio_path = audio_path_translate_original
        else:
            audio_path_translate_final = await asyncio.wait_for(
                mix_audio_m4a(audio_path, audio_path_translate_original, audio_path_translate_final, configurations.get('overlay'), bitrate),
                timeout=config.KILL_JOB_DOWNLOAD_TIMEOUT_SEC)

            if not audio_path_translate_final or not audio_path_translate_final.exists():
                logger.error(f'❌ {mid} audio_path_translate_final does not exist after downloading. Exiting.')
                await info_message.edit_text('❌ Error: audio_path_translate_final does not exist after downloading. Exiting.')
                return

            audio_path = audio_path_translate_final

    if summary:
        timecodes = summary

    segments = [{'path': audio_path, 'start': 0, 'end': duration, 'title': ''}]

    if action == config.ACTION_NAME_SPLIT_BY_DURATION:
        split_duration_minutes = int(configurations.get('split_duration_minutes', 0))
        if split_duration_minutes > 0:
            segments = get_segments_by_duration(
                total_duration=duration,
                segment_duration=60 * split_duration_minutes)

    elif action == config.ACTION_NAME_SPLIT_BY_TIMECODES:
        segments = get_segments_by_timecodes_from_dict(timecodes=timecodes, total_duration=duration)

    elif duration > config.SEGMENT_AUDIO_DURATION_SPLIT_THRESHOLD_SEC:
        segments = get_segments_by_duration(
            total_duration=duration,
            segment_duration=config.SEGMENT_AUDIO_DURATION_SEC)

    segments = add_paddings_to_segments(segments, config.SEGMENT_DURATION_PADDING_SEC)

    audio_file_size = await get_file_size(audio_path)

    max_segment_duration = int(0.89 * duration * config.TELEGRAM_MAX_FILE_SIZE_BYTES / audio_file_size)

    segments = make_magic_tail(segments, max_segment_duration)

    segments = segments_verification(segments, max_segment_duration)

    # Check Rebalance by Timecodes
    if SEGMENT_REBALANCE_TO_FIT_TIMECODES:
        segments = rebalance_segments_long_timecodes(
            segments,
            config.TELEGRAM_MAX_CAPTION_TEXT_SIZE - len(caption_head_output),
            timecodes,
            config.SEGMENT_AUDIO_DURATION_SEC)

        segments = add_paddings_to_segments(segments, config.SEGMENT_DURATION_PADDING_SEC)

    if not segments:
        logger.error(f'❌ {mid} No audio segments found after processing. This could be an internal error.')
        await info_message.edit_text(f'❌ Error: No audio segments found after processing. This could be an internal error.')
        return

    try:
        segments = await make_split_audio_second(audio_path, segments)
    except Exception as e:
        logger.error(f'❌ {mid} Error occurred while splitting audio into segments: {e}')
        await info_message.edit_text(f'❌ Error: Failed to split audio into segments.')
    if not segments:
        logger.error(f'❌ {mid} No audio segments found after splitting.')
        await info_message.edit_text(f'❌ Error: No audio segments found after processing.')
        return

    await info_message.edit_text('⌛🚀 Uploading to Telegram…')
    for idx, segment in enumerate(segments):
        logger.info(f'💚 {mid} Uploading audio file: {segment.get("audio_path")}')
        segment_start = segment.get('start')
        segment_end = segment.get('end')
        filtered_timecodes_dict = filter_timecodes_within_bounds(
            timecodes=timecodes, start_time=segment_start + config.SEGMENT_DURATION_PADDING_SEC, end_time=segment_end - config.SEGMENT_DURATION_PADDING_SEC - 1)
        timecodes_text = get_timecodes_formatted_text(filtered_timecodes_dict, segment_start)

        if segment.get('title'):
            caption_head_additional_output += config.ADDITIONAL_CHAPTER_BLOCK.substitute(
                time_shift=standardize_time_format(timedelta_from_seconds(segment.get('start'))),
                title=segment.get('title'))
            timecodes_text = ''

        segment_path = pathlib.Path(segment.get('path'))

        duration_measure = await get_duration(segment_path)
        duration = duration_measure if duration_measure is not None else segment_end - segment_start

        caption_output = Template(caption_head_output).safe_substitute(
            partition='' if len(segments) == 1 else f'[Part {idx + 1} of {len(segments)}]',
            duration=standardize_time_format(timedelta_from_seconds(duration + 1)),
            content=timecodes_text,
            additional=caption_head_additional_output)

        # todo English filename EX https://www.youtube.com/watch?v=gYeyOZTgf2g
        fname_suffix = segment_path.name
        fname_prefix = '' if len(segments) == 1 else f'p{idx + 1}_of{len(segments)}-'
        fname_title_size = config.TG_MAX_FILENAME_LEN - len(fname_prefix) - len(fname_suffix)
        fname_title = title[:fname_title_size]+'-' if fname_title_size > 6 else ''

        await bot.send_audio(
            chat_id=sender_id,
            audio=FSInputFile(
                path=segment.get('path'),
                filename=fname_prefix + fname_title + fname_suffix),
            duration=duration,
            thumbnail=FSInputFile(path=thumbnail_path) if thumbnail_path is not None else None,
            caption=caption_output if len(caption_output) < config.TELEGRAM_MAX_CAPTION_TEXT_SIZE else trim_caption_to_telegram_send(caption_output),
            reply_to_message_id=reply_output,
            parse_mode='HTML')

        reply_output = None

        # Sleep to avoid flood in Telegram API
        await magic_sleep_against_flood(idx, len(segments))

    await info_message.delete()
    logger.info(f'💚✅ {mid} Done!')
