import os
from tiktok_downloader import snaptik
from moviepy import editor
from config import bot, bot_name


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(chat_id=message.chat.id, 
                    text=('👋 Hello, I will help you download',
                          ' videos from <b>TikTok</b>.\n\n',
                          '/help - instructions for using the bot.'), 
                    parse_mode='html')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(chat_id=message.chat.id, 
                    text=('❓ To download a video',
                          ' from <b>TikTok</b>, just <b>send</b> me video link.\n\n',
                          '<b>The link must start with:</b>\n🔗 https://vm.tiktok.com/...\n',
                          '🔗 http://vm.tiktok.com/...\n\n',
                          '❓ To convert <b>video</b> to <b>audio</b> send me: <b>/c link</b>'), 
                    parse_mode='html')


if not os.path.exists('videos'):
    os.makedirs('videos')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.type == "private":
        if message.text.startswith('https://vm.tiktok.com') or message.text.startswith('http://vm.tiktok.com'):
            video_url = message.text

            try:
                bot.send_message(chat_id=message.chat.id, text='⏳ Please wait...')

                snaptik(f"{video_url[:31]}").get_media()[0].download(f"./videos/result_{message.from_user.id}.mp4")
                path = f'./videos/result_{message.from_user.id}.mp4'
                
                with open(f'./videos/result_{message.from_user.id}.mp4', 'wb') as file:
                    bot.send_video(
                    chat_id=message.chat.id,
                    data=file,
                    caption=f'{video_url[:31]}\n\nDownloaded from {bot_name}'
                    )
                os.remove(path)

            except:
                bot.send_message(chat_id=message.chat.id, text=f'❌ Upload error, wrong link, video deleted or I can\'t find it.')
                
        elif message.text[:2] == "/c":
            if message.text[3:].startswith('https://vm.tiktok.com') or message.text.startswith('http://vm.tiktok.com'):
                video_url = message.text[3:]

                try:
                    bot.send_message(chat_id=message.chat.id, text='⏳ Please wait while I convert your video to audio...')

                    snaptik().get_media(f"{video_url[:31]}")[0].download(f"./videos/result_{message.from_user.id}.mp4")
                    path1 = f'./videos/result_{message.from_user.id}.mp3'
                    path2 = f'./videos/result_{message.from_user.id}.mp4'

                    video = editor.VideoFileClip(path2)
                    
                    with video:
                        audio = video.audio
                        audio.write_audiofile(path1)

                        bot.send_audio(message.chat.id, 
                                        audio=open(path1, 'rb'), 
                                        caption=f'{video_url[:31]}\n\nConverted from {bot_name}')

                    os.remove(path2)
                    os.remove(path1)
                
                except:
                    bot.send_message(chat_id=message.chat.id, text=f'❌ Upload error, wrong link, video deleted or I can\'t find it.')
                
        else:
            bot.send_message(chat_id=message.chat.id, 
                            text='😕 I didn\'t understand you, send me a link to a video from Tik Tok <b>TikTok</b>.', 
                            parse_mode='html')

if __name__ == "__main__":
    bot.polling(non_stop=True)