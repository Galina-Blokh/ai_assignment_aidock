import logging
import grequests
from bs4 import BeautifulSoup
import config
import extract_one_recipe

# # log-file will be created in the same dir
logging.basicConfig(filename=config.LOG_FILE, level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_all_links_recipes(url_to_get):
    """The function receives url_to_get:str
     collects all recipes links from page with all recipes
     :returns recipes_links:list[str] """

    response = ''
    try:
        page = grequests.get(url_to_get)
        response = grequests.map([page], size=config.BATCHES)
    except:
        logging.warning("Can't collect `recipes_links` from a page")

    soup = [BeautifulSoup(res.text, 'html.parser') for res in response]
    recipes_links = [link.get('href') for link in soup[0].find_all('a') if
                     str(link.get('href')).startswith(config.LINK_PATTERN)]

    logging.info(f'Collected {len(recipes_links)} `recipes_links` from recipes page')
    return recipes_links


def extract_links_to_file(file_name=config.FILE_LINKS_NAME, url_to_write=config.URL):
    """
    Function receives a file_name:str
    extract links to file_name.txt file
    :return: path:str
    """
    output_links, path = extract_one_recipe.check_dir_path(file_name, 'w+')
    all_links = get_all_links_recipes(url_to_write)

    # writing down all links into txt file
    [output_links.write(link + '\n') for link in all_links]
    output_links.close()
    logging.info(f'Links were written into file {path} finished')
    return path


if __name__ == '__main__':
    pass
