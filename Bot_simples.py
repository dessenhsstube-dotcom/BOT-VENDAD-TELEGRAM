
import telebot
from telebot import types
import os
import logging
import time # Necessário para o Polling

# Configuração de Logs
# (A Discloud já lê logs automaticamente, mas isto ajuda na organização)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --------------------------------------------------------------------------
# VARIÁVEIS DE AMBIENTE
# --------------------------------------------------------------------------

# Estas variáveis serão lidas do painel da Discloud
BOT_TOKEN = os.getenv("BOT_TOKEN") 
LINK_SUPORTE = os.getenv("LINK_SUPORTE", "https://t.me/seu_username_de_suporte") 
LINK_CANAL_PREVIAS = os.getenv("LINK_CANAL_PREVIAS", "https://t.me/+e_6gNgrikp5lNDkx") 

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN não está definido. O bot não iniciará.")
    exit()

# Inicialização do Bot
try:
    bot = telebot.TeleBot(BOT_TOKEN)
    logging.info("Bot de Vendas Simples inicializado com sucesso.")
except Exception as e:
    logging.error(f"Falha na inicialização do Bot: {e}")
    exit()

# --------------------------------------------------------------------------
# HANDLER PRINCIPAL (/start)
# --------------------------------------------------------------------------

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """Handler para /start e /help que envia a mensagem de boas-vindas com links."""
    
    # Cria o teclado com botões inline
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Botão para o Canal de Prévias
    # O valor do LINK_CANAL_PREVIAS é lido da variável de ambiente
    btn_previa = types.InlineKeyboardButton("🔥 GRUPO DE PRÉVIAS", url=LINK_CANAL_PREVIAS)
    
    # Botão para o Suporte (onde o pagamento será combinado)
    # O valor do LINK_SUPORTE é lido da variável de ambiente
    btn_suporte = types.InlineKeyboardButton("💳 COMPRAR / TIRAR DÚVIDAS", url=LINK_SUPORTE)
    
    markup.add(btn_previa, btn_suporte)

    welcome_text = (
        f"👑 *Bem-vindo(a) ao Acesso VIP!*\n\n"
        f"Confira nosso conteúdo exclusivo no Grupo de Prévias abaixo e fale com o suporte para garantir o seu acesso vitalício.\n\n"
        f"👇 *Fale conosco para realizar o pagamento (PIX ou outro método):*"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode="Markdown", 
    )

# --------------------------------------------------------------------------
# INICIAÇÃO DO POLLING
# --------------------------------------------------------------------------

def run_bot():
    """Inicia o bot no modo Polling (ideal para Discloud Free)."""
    try:
        logging.info("Iniciando Bot no modo Polling...")
        # O modo Polling funciona perfeitamente no Discloud Free, pois não exige servidor Web
        # none_stop=True garante que ele tente se reconectar
        bot.polling(none_stop=True, interval=0) 
    except Exception as e:
        logging.error(f"Erro no Polling: {e}. Reiniciando em 5 segundos...")
        time.sleep(5)
        run_bot()

if __name__ == "__main__":
    run_bot()
