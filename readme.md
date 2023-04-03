## WikiScrapper For UFC Fighters

### Command Line - Arguments Input Commands

wiki_scrapper : First & Main Input command line Argument <br>
ops : Get Fighter Opponents <br>
ops+info : Get Fighter Opponents with Info <br>
info: Get Fighter Info <br>
{fighter_url} : Fighter url on wiki <br>
{file_name}: Name of file to generate after scrapped data

#### Get Fighter Opponents

command example to get fighter opponents of khabib from wiki:
=> wiki_scrapper ops {fighter_url} {file_name}

wiki_scrapper ops+info https://en.wikipedia.org/wiki/Khabib_Nurmagomedov ops_info_khabib
