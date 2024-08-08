import discord
from discord.ext import commands

# 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽기 위한 인텐트
intents.members = True           # 멤버 정보 읽기를 위한 인텐트

# 봇 초기화
bot = commands.Bot(command_prefix='!!', intents=intents)

# 유저 정보를 저장할 딕셔너리
user_info = {}

# 정보 수집 채널 ID
INFO_CHANNEL_ID = 1267445852809592842  # 여기에 정보를 받을 채널 ID를 입력하세요

# 공지 채널 ID
ANNOUNCE_CHANNEL_ID = 1269337375159619667  # 여기에 정보를 보낼 채널 ID를 입력하세요

@bot.event
async def on_message(message):
    # 봇 자신의 메시지는 무시
    if message.author == bot.user:
        return

    # 특정 채널에서 메시지를 받는 경우
    if message.channel.id == INFO_CHANNEL_ID:
        # 메시지를 특정 형식으로 파싱 (닉네임, 나이, 성별, 입장 경로)
        try:
            lines = message.content.splitlines()
            if len(lines) == 4:
                nickname = lines[0].split(":", 1)[1].strip()
                age = lines[1].split(":", 1)[1].strip()
                gender = lines[2].split(":", 1)[1].strip()
                entry_path = lines[3].split(":", 1)[1].strip()

                # 유저 정보 저장
                user_info[message.author.id] = {
                    "nickname": nickname,
                    "age": age,
                    "gender": gender,
                    "entry_path": entry_path
                }

                # 다른 채널로 메시지 보내기
                announce_channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
                if announce_channel:
                    await announce_channel.send(f"{message.author.mention}님의 정보가 저장되었습니다!")
        except Exception as e:
            await message.channel.send("정보를 저장하는데 실패했습니다. 올바른 형식으로 입력해주세요.")

    await bot.process_commands(message)

@bot.command(name='유저정보')
async def user_info_command(ctx, member: discord.Member):
    # 유저 정보 불러오기
    info = user_info.get(member.id)
    if info:
        response = (
            f"**닉네임:** {info['nickname']}\n"
            f"**나이:** {info['age']}\n"
            f"**성별:** {info['gender']}\n"
            f"**입장 경로:** {info['entry_path']}"
        )
        await ctx.send(response)
    else:
        await ctx.send(f"{member.mention}님의 정보를 찾을 수 없습니다.")

@bot.command(name='유저삭제')
async def delete_user_info(ctx, member: discord.Member):
    # 유저 정보 삭제
    if member.id in user_info:
        del user_info[member.id]
        await ctx.send(f"{member.mention}님의 정보가 삭제되었습니다.")
    else:
        await ctx.send(f"{member.mention}님의 정보를 찾을 수 없습니다.")

# 봇 실행
bot.run('MTI3MDYyNDg3MjU5NDE0NTM1MA.GMEO7m.bFYO6BKaQZn7etPKyMw_0V84sI7RfT6sw3O_TQ')
