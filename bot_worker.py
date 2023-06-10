import telebot
import math

def xor(a):
    res = 0
    for i in a:
        res ^= i
    return res


def prod(a):
    res = 1
    for i in a:
        res *= i
    return res


def valid_eval(f):
    f = str(f)
    if not (len(f) >= 2 and all([(lambda x: str(x) == "1" or str(x) == "0")(x) for x in f]) and math.log2(len(f)).is_integer()):
        raise Exception("Некорректный вектор. Количество символов должно быть степенью двойки (2 для одной переменной, 4 для двух, 8, 16 и пр.)")


def truth_table(f):
    f = str(f)
    cols = math.ceil(math.log2(len(f)))
    rows = len(f)
    table = []
    for i in range(rows):
        v = [int(r) for r in bin(i)[2:].zfill(cols)]
        dirty_row = [j for j in list(zip([v], [[int(f[i])]]))][0]
        r = []
        for item in dirty_row:
            r.extend(item)
        table.append(r)
    return table


def is_P0(eval):
    return eval[0] == "0"


def is_P1(eval):
    return eval[-1] == "1"


def is_L(eval):
    table_orig = truth_table(eval)
    table = [[]]
    for i in table_orig:
        if i[:-1].count(1) == 1:
            table.append(i)
    table = table[1:]
    a = [0] * (len(table[0][:-1]) + 1)
    a[0] = table_orig[0][-1]
    for i in range(0, len(table[0][:-1])):
        a[len(table[0][:-1]) - i] = a[0] ^ table[i][-1]
    new_eval = [a[0]] * len(eval)
    for i in range(1, len(table_orig)):
        for j in range(len(table_orig[i][:-1])):
            new_eval[i] ^= table_orig[i][j] * a[j + 1]
    eval = str(eval)
    str_new_eval = ""
    for i in new_eval:
        str_new_eval += str(i)
    new_eval = str_new_eval
    if new_eval == eval:
        return True
    else:
        return False


def is_S(eval):
    new_eval = str(eval[::-1]).replace("1", "*").replace("0", "1").replace("*", "0")
    if eval == new_eval:
        return True
    else:
        return False


def is_M(eval):
    eval = str(eval)
    table = truth_table(eval)
    if "1" in eval:
        starter = eval.index("1")
    else:
        starter = 0
    table = table[starter:]
    for i in range(len(table)):
        for j in range(i + 1, len(table)):
            checker = [x <= y for x in table[i][:-1] for y in table[j][:-1]]
            if all(checker):
                comparable = True
            else:
                comparable = False
            if comparable:
                if table[i][-1] > table[j][-1]:
                    return False
    return True

def belongs_msg(b):
    if b: return "принадлежит ✅"
    else: return "не принадлежит ❌"

bot = telebot.TeleBot(open("api.txt").readline(), parse_mode=None, skip_pending=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Уверен, что вы всегда хотели узнать, к каким классам <a href='https://ru.wikipedia.org/wiki/Пост,_Эмиль_Леон'>Поста</a> принадлежит булева функция. Теперь вы можете это делать хоть каждую секунду, не выходя из Телеграма 🤩 Введите eval (вектор) вашей прекрасной функции, а я скажу, чему она там принадлежит. Чтобы подробнее узнать об этом и другом, введите команду /help",
                 parse_mode="HTML")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "<b>Как пользоваться ботом</b>\n\n1️⃣ Введите вектор функции, например, <pre>11001010</pre>\n\n2️⃣ Бот в ответ пришлет таблицу истинности и краткую информацию о принадлежности функции каждому <a href='https://ru.wikipedia.org/wiki/Предполные_классы'>классу Поста</a>\n\n\n<b>Описание классов <a href='https://ru.wikipedia.org/wiki/Пост,_Эмиль_Леон'>Поста</a></b>\n\n💫 <b>P0</b> - функции, сохраняющие 0. Т. е. f(0, 0, ... 0) = 0.\n🪄 <b>P1</b> - функции, сохраняющие 1. Т. е. f(1, 1, ... 1) = 1.\n🐍 <b>L</b> - <a href='https://ru.wikipedia.org/wiki/Линейная_булева_функция'>линейные функции</a>, т.е. в <a href='https://en.wikipedia.org/wiki/Algebraic_normal_form'>алгебраической нормальной форме (АНФ)</a> отсутствуют произведения переменных.\n♾️ <b>S</b> - <a href='https://ru.wikipedia.org/wiki/Самодвойственная_функция'>самодвойственные функции</a>, т. е. f = f*.\n💯 <b>M</b> - <a href='https://ru.wikipedia.org/wiki/Монотонная_булева_функция'>монотонные функции</a>, т. е. для любых двух сравнимых наборов an и bn таких, что a ≼ b, имеет место равенство f(an) ≤ f(bn).",
                 parse_mode="HTML")



@bot.message_handler(func=lambda message: True)
def ask(message):
    try:
        f = str(message.text)
        valid_eval(f)
        table = truth_table(f)
        str_table = ""
        for i in range(len(table)):
            for j in range(len(table[0])):
                str_table += str(table[i][j]) + " "
            str_table += "\n"
        if len(str_table) > 4096:
            bot.send_message(message.chat.id, "Таблица слишком большая. Телеграм не поддерживает отправку более 4096 символов")
        else:
            bot.send_message(message.chat.id, f"Таблица истинности:\n\n{str_table}")
        bot.send_message(message.chat.id, f"Принадлежность функций классам:\n\n<b>P0:</b> {belongs_msg(is_P0(f))}\n<b>P1:</b> {belongs_msg(is_P1(f))}\n<b>L:</b> {belongs_msg(is_L(f))}\n<b>S:</b> {belongs_msg(is_S(f))}\n<b>M:</b> {belongs_msg(is_M(f))}", parse_mode="HTML")

    except Exception as e:
        bot.send_message(message.chat.id, f"❗️ Извините, произошла ошибка: \n\n{e}")


bot.infinity_polling()
