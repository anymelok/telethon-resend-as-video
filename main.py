from telethon import TelegramClient, events
import yt_dlp
import asyncio
from config import settings
import os

URL_PATTERN = r"(?i)https?:\/\/(?P<site_name>[^/?]+)"

client = TelegramClient('Mi9Lite_Server', settings.API_ID, settings.API_HASH)


@client.on(events.NewMessage(outgoing=True, pattern=URL_PATTERN))
async def message_handler(event):
    site_name = event.pattern_match.group('site_name').lower()
    print(f'Detected URL. Site name: {site_name}')

    service = 'Other'
    if 'reddit' in site_name or 'redd.it' in site_name:
        service = 'Reddit'

    if service == 'Reddit':
        await event.delete()
        print('Message deleted!')
        await download_and_send(client, event)


async def download_and_send(client, event):
    '''
    Downloads file from event.raw_text
    and sends file in the same chat
    '''
    filename = await download_video(event.raw_text)
    entity = await client.get_entity(event.chat_id)
    print('Video downloaded. Sending...')

    await client.send_file(entity, filename, progress_callback=progress_callback)
    print('\nVideo sent!')

    print('Cleaning up...')
    remove_file(filename)


def remove_file(filename):
    '''
    Gets full path to a file and removes it
    '''
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path_to_file = os.path.join(script_dir, filename)

    try:
        os.remove(full_path_to_file)
        print(f"Successfully removed: {full_path_to_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def progress_callback(current, total):
    '''
    Print progress in console
    '''
    percentage = (current / total) * 100
    print(f"\rUploaded: {percentage:.2f}%", end='')


async def download_video(url: str):
    '''
    Downloads a video from url
    returns filename
    '''
    ytdl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
    }

    def download():
        print("yt-dlp: Starting information extraction...")
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdlp:
            info = ytdlp.extract_info(url, download=True)
            return ytdlp.prepare_filename(info)

    loop = asyncio.get_event_loop()
    filename = await loop.run_in_executor(None, download)
    return filename


async def main():
    await client.start()
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
