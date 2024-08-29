from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from .messages import *
from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import sync_to_async
from user.models import CustomUser, TelegramProfile
from collections import OrderedDict
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from post.models import Post, Tag

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# In-memory session management
MAX_USERS = 100
users = OrderedDict()
user_posts = {}
@sync_to_async
def create_or_update_user_profile(user_id, username, first_name, last_name, phone_number, email):
    user, created = CustomUser.objects.get_or_create(username=user_id,phone_number=phone_number)
    profile = TelegramProfile.objects.update_or_create(
        user=user,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email
        }
    )
    return user, profile


async def lobby(msg: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔥 Подать объявление", callback_data="post_ad"))
    keyboard.add(InlineKeyboardButton("⭐️ Мои объявления", callback_data="my_ads"))
    keyboard.add(InlineKeyboardButton("👨‍💻 Тех. Поддержка", callback_data="support"))
    
    await msg.reply(
    "Добро пожаловать в Nobox!\n"
    "Ищем квартиру? Или что-то размещаешь? 😏\n\n"
    "📑 Объявлений пока: 0\n"
    "👩‍💻 На проверке: 0\n"
    "💫 Просмотров всего: 0",
    reply_markup=keyboard
)
    
    
@sync_to_async
def user_exists(user_id):
    return CustomUser.objects.filter(username=user_id).exists()




@dp.message_handler(commands=['start'])
async def start_registration(message: types.Message):
    user_id = message.from_user.id
    global user_posts
    if await user_exists(user_id):
        await message.answer(WELCOME_BACK_MESSAGE+ f"\nСлушаю тебя, {message.from_user.first_name} 🙋‍♀️\n\n")
        await lobby(message)
        user_posts[user_id] = None
            
        
        return
        
    

    users[user_id] = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'step': 'phone'
    }
    
    btn = types.KeyboardButton("Отправить", request_contact=True)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    await message.answer(ASK_PHONE, reply_markup=kb)

@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    user_id = message.from_user.id
    if user_id in users:
        phone_number = message.contact.phone_number
        users[user_id]['phone'] = phone_number
        users[user_id]['step'] = 'email'
        await message.answer(ASK_EMAIL)


from post.models import Tag

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

@sync_to_async
def select_tags(message: types.Message):
    tags = Tag.objects.all()
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(tag.name, callback_data=f"tag_{tag.id}") for tag in tags]
    keyboard.add(*buttons)
    
    # Add the "Подтвердить" button
    confirm_button = InlineKeyboardButton("Подтвердить", callback_data="confirm_tags")
    keyboard.add(confirm_button)
    
    return keyboard

@dp.callback_query_handler(lambda c: c.data == 'confirm_tags')
async def confirm_tags(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Update the user's step to "photo"
    user_posts[user_id]['step'] = 'photo'
    
    # Remove the inline keyboard and send the next instruction
    await callback_query.message.edit_text("Отправьте фотографию (1 шт):", reply_markup=None)
    
    # Answer the callback query
    await callback_query.answer()


@dp.message_handler(commands=['debug'])
async def start_registration(message: types.Message):
            keyboard = await select_tags(message)
            await message.reply('Выберите теги из списка', reply_markup =keyboard)


@dp.message_handler(content_types=['text'])
async def handle_email(message: types.Message):
    user_id = message.from_user.id
    if user_id in users and users[user_id].get('step') == 'email':
        email = message.text
        users[user_id]['email'] = email
        users[user_id]['step'] = 'done'
        # Complete user registration
        user_data = users.pop(user_id)
        await create_or_update_user_profile(
            user_id=user_id,
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone_number=user_data['phone'],
            email=user_data['email']
        )
        
        await message.answer(REGISTRATION_COMPLETED_MESSAGE)
        await lobby(message)
    if user_id in user_posts:
        step = user_posts[user_id]['step']
        
        if step == 'price':
            user_posts[user_id]['price'] = message.text
            user_posts[user_id]['step'] = 'description'
            await message.answer("Введите описание:")
        
        elif step == 'description':
            user_posts[user_id]['description'] = message.text
            user_posts[user_id]['step'] = 'tags'
            keyboard = await select_tags(message)
            await message.reply('Выберите теги из списка', reply_markup =keyboard)                
    

# In-memory storage for post data


@dp.callback_query_handler(lambda c: c.data == 'post_ad')
async def start_post_creation(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in user_posts and user_posts[user_id] is not None:
        await callback_query.answer("Введи цену!")
        return
    else:
        user_posts[user_id] = {
        'price': None,
        'description': None,
        'tags': [],
        'photo': None,
        'step': 'price'
    }
    await bot.send_message(user_id, "Введите цену:")
    await bot.answer_callback_query(callback_query.id)

from django.core.exceptions import ObjectDoesNotExist

@dp.message_handler(content_types=['photo'])
async def handle_photo_message(message: types.Message):
    global user_posts
    user_id = message.from_user.id
    if user_id in user_posts and user_posts[user_id].get('step') == 'photo':
        user_posts[user_id]['photo'] = message.photo[-1].file_id
        # Prepare post data to save to the model
        user_posts[user_id]["step"]="confirm"
        the_post = user_posts[user_id]
        tags = await sync_to_async(lambda: ', '.join(Tag.objects.filter(id__in=user_posts[user_id]["tags"]).values_list('name', flat=True)))()
        post_info = f"Описание: {the_post['description']}\nЦена: {the_post['price']}\nТеги: {tags}"
        post_it = InlineKeyboardMarkup().add(InlineKeyboardButton("Подтвердить",callback_data="post_it"))
        await bot.send_photo(
    chat_id=message.chat.id, 
    photo=the_post["photo"], 
    caption=post_info, 
    reply_markup=post_it
)
        
        
@dp.callback_query_handler(lambda c: c.data == "post_it")
async def post_it_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_posts.get(user_id) and user_posts[user_id]['step'] == "confirm":
        post_data = user_posts.pop(user_id)
        try:
            user = await sync_to_async(CustomUser.objects.get)(username=user_id)
        except ObjectDoesNotExist:
            await message.answer("Ошибка: пользователь не найден.")
            return

        # Create the post
        post = await sync_to_async(Post.objects.create)(
            author=user,
            price=post_data['price'],
            description=post_data['description'],
            picture=post_data['photo']
        )

        # Set tags for the post
        tags = await sync_to_async(Tag.objects.filter)(id__in=post_data["tags"])
        await sync_to_async(post.tags.set)(tags)

        await callback_query.message.answer("Объявление создано! 🎉")
        await lobby(callback_query.message)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        
        
        
@dp.callback_query_handler(lambda c: c.data == 'support')
async def process_support(callback_query: types.CallbackQuery):
    support_message = "Обратитесь сюда @NoboxSupport\nИли @lnternetwarrior(Главный модер)"
    await bot.answer_callback_query(callback_query.id, text=support_message, show_alert=True)
    
    
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Dictionary to store tag selections for each user



@dp.callback_query_handler(lambda c: c.data.startswith('tag_'))
async def handle_tag_selection(callback: types.CallbackQuery):
    user_id = callback["from"]["id"]
    data = int(callback.data[4:])
    if data in user_posts[user_id]['tags']:
        user_posts[user_id]['tags'].remove(data)
        await callback.answer("Удалено!")
        return
    user_posts[user_id]['tags'].append(data)
    await callback.answer("Добавлено!")
    
    


class Command(BaseCommand):
    help = "Start Telegram bot"

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)