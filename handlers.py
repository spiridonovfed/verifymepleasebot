import os
from telegram.ext import CommandHandler, MessageHandler, Filters

from settings import WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID
import sqlighter


def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)


def forward_to_chat(update, context):
    """{ 
        'message_id': 5, 
        'date': 1605106546, 
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'}, 
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = update.message.from_user.id
    if not sqlighter.check_in_ban_list(user_id):
        update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    else:
        print("This user is banned")
        context.bot.sendMessage(chat_id=update.message.chat.id,
                                text='You are banned! Admins cannot see you messages.',
                                reply_to_message_id=update.message.message_id)


def forward_to_user(update, context):
    """{
        'message_id': 10, 'date': 1605106662, 
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659, 
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'}, 
            'forward_date': 1605106658, 
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        }, 
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = update.message.reply_to_message.forward_from.id
    context.bot.copy_message(
        message_id=update.message.message_id,
        chat_id=user_id,
        from_chat_id=update.message.chat_id
    )


def ban_user(update, context):
    user_id = update.message.reply_to_message.forward_from.id
    user_username = update.message.reply_to_message.forward_from.username
    print(f"User {user_username} with id {user_id} was banned")
    sqlighter.insert_banned_user(user_id, user_username)
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text='This user is banned now. '
                                 'The user is notified about it and you will not see his or hers further messages.',
                            reply_to_message_id=update.message.message_id)
    context.bot.sendMessage(chat_id=update.message.reply_to_message.forward_from.id,
                            text='You are banned! Admins cannot see you messages.')


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply & Filters.regex('Ban!'), ban_user))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    return dp
