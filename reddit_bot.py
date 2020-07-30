import praw
import sys
try:
    import config
except:
    print('config.py not found in the current directory. It must have your username, password, client_id, and client_secret.')
    sys.exit()

def bot_login():
    return praw.Reddit(username=config.username,
                password=config.password,
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent='r/listentothis scraper')

def run_bot(r, limit=50, category='hot'):
    title_list =  []
    if category == 'hot':
        for post in r.subreddit('listentothis').hot(limit=limit):
            title_list.append(post.title)
    elif category == 'new':
        for post in r.subreddit('listentothis').new(limit=limit):
            title_list.append(post.title)
    return title_list

def parse_list(title_list):
    parsed_list = []
    for title in title_list:
        try:
            if '--' in title:
                first, second = title.split('--', maxsplit=1)
            elif '-' in title:
                first, second = title.split('-', maxsplit=1)
            else:
                print('No standard delimiter.')
                continue
        except ValueError:
            print('FAILED: ', title)
            continue

        artist = first.rstrip()
        song = second.lstrip()[:second.index('[')-1].rstrip()
        genre_list = second[second.index('[')+1:second.index(']')].split('/')
        for i,g in enumerate(genre_list):
            genre_list[i] = g.lstrip().rstrip().lower()

        parsed_list.append({'artist': artist,
                            'song': song,
                            'genres': genre_list
                            })
    return parsed_list


def fix_genres(data):
    data = data if isinstance(data, list) else data['genres']
    for i, genre in enumerate(data):
        if ' ' in genre:
            data[i] = genre.replace(' ', '-')

        if ' & ' in genre:
            data[i] = genre.replace(' & ', '-n-')
        elif ' and ' in genre:
            data[i] = genre.replace(' and ', '-n-')
        elif '&' in genre:
            data[i] = genre.replace('&', '-n-')


def main_script(limit=50, category='hot'):
    r = bot_login()
    title_list = run_bot(r, limit, category)
    parsed_list = parse_list(title_list)
    for data in parsed_list:
        fix_genres(data)
    return parsed_list


if __name__ == '__main__':
    main_script()