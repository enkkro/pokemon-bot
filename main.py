from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup

TOKEN = 'MTM2NjQwNjQ3ODYwODQ2NjA0MA.G9cBUr.gEumdg8tTzmKHVQyTqNf34Vtr5dPqprViBfe4w'  # Ton token Discord ici
CHANNEL_ID = 1215440877816647721  # ID de ton salon Discord

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

known_products = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    check_preorders.start()

@tasks.loop(minutes=1)
async def check_preorders():
    channel = bot.get_channel(CHANNEL_ID)

    # Scraper Cultura
    cultura_url = "https://www.cultura.com/jeux-jouets/jeux-de-cartes/pokemon.html"
    response_cultura = requests.get(cultura_url)
    soup_cultura = BeautifulSoup(response_cultura.text, "html.parser")
    cultura_products = soup_cultura.find_all('a', class_="product-item-link")

    for product in cultura_products:
        title = product.get_text(strip=True)
        link = product['href']
        if "précommande" in title.lower() or "pré-commande" in title.lower():
            if title not in known_products:
                known_products.append(title)
                embed = discord.Embed(
                    title="Nouvelle Précommande Pokémon TCG sur Cultura",
                    description=f"**{title}**\n[Voir le produit]({link})",
                    color=discord.Color.blue()
                )
                await channel.send(embed=embed)

    # Scraper Fnac
    fnac_url = "https://www.fnac.com/SearchResult/ResultList.aspx?SCat=0%211&Search=Pokemon+cartes+sous-blister"
    response_fnac = requests.get(fnac_url)
    soup_fnac = BeautifulSoup(response_fnac.text, "html.parser")
    fnac_products = soup_fnac.find_all('a', class_="Article-desc")

    for product in fnac_products:
        title = product.get_text(strip=True)
        link = product['href']
        full_link = f"https://www.fnac.com{link}"

        if "précommande" in title.lower() or "pré-commande" in title.lower():
            if title not in known_products:
                known_products.append(title)
                embed = discord.Embed(
                    title="Nouvelle Précommande Pokémon TCG sur Fnac",
                    description=f"**{title}**\n[Voir le produit]({full_link})",
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)

    # Scraper Micromania
    micromania_url = "https://www.micromania.fr/search.html?query=pokemon%20cartes"
    response_micro = requests.get(micromania_url)
    soup_micro = BeautifulSoup(response_micro.text, "html.parser")
    micro_products = soup_micro.find_all('a', class_="product-item-link")

    for product in micro_products:
        title = product.get_text(strip=True)
        link = product['href']
        full_link = f"https://www.micromania.fr{link}"

        if "précommande" in title.lower() or "pré-commande" in title.lower():
            if title not in known_products:
                known_products.append(title)
                embed = discord.Embed(
                    title="Nouvelle Précommande Pokémon TCG sur Micromania",
                    description=f"**{title}**\n[Voir le produit]({full_link})",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)

    # Scraper Amazon
    amazon_url = "https://www.amazon.fr/s?k=cartes+pokemon+précommande"
    response_amazon = requests.get(amazon_url, headers=headers)
    soup_amazon = BeautifulSoup(response_amazon.text, "html.parser")
    amazon_products = soup_amazon.find_all('span', class_="a-size-medium a-color-base a-text-normal")

    for product in amazon_products:
        title = product.get_text(strip=True)
        link_element = product.find_parent('a')
        if link_element:
            link = "https://www.amazon.fr" + link_element['href']

            if "précommande" in title.lower() or "pré-commande" in title.lower():
                if title not in known_products:
                    known_products.append(title)
                    embed = discord.Embed(
                        title="Nouvelle Précommande Pokémon TCG sur Amazon",
                        description=f"**{title}**\n[Voir le produit]({link})",
                        color=discord.Color.orange()
                    )
                    await channel.send(embed=embed)

keep_alive()
bot.run(TOKEN)
