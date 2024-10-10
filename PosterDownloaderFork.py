from impawards import Crawler
import argparse
import logging
import shutil
import os
 
def get_year_range():
    while True:
        try:
            start_year = int(input("Original Project by FdelMazo. Forked by MarcoCasanova00 - Enter the start year: "))
            end_year = int(input("Enter the end year: "))
            if start_year > end_year:
                print("Start year must be less than or equal to end year. Try again.")
            else:
                return start_year, end_year
        except ValueError:
            print("Please enter valid years.")
 
def select_link(possible_links, flags):
    if len(possible_links) == 0:
        logging.warning("No movies found")
        return [], []
 
    while True:
        if len(possible_links) == 1 or flags.get('no_confirm'):
            title, movie_link = possible_links[0]
            confirm = input(f"Only one movie found: {title}. Do you want to select it? (y/n): ").lower()
            if confirm == 'y':
                return [title], [movie_link]
            else:
                return [], []
        else:
            for i, (title, link) in enumerate(possible_links, 1):
                print(f"\t{i:<3} -  {title}")
 
            logging.debug("Press return to stop ")
            selection = input("\nWhich Movies? [Range, e.g. 1-3 or 1,3,5]: ").lower()
 
            if not selection:
                logging.warning("User canceled action")
                del possible_links[:]
                return [], []
 
            if '-' in selection:
                try:
                    start, end = map(int, selection.split('-'))
                    if 0 < start <= end <= len(possible_links):
                        titles = [possible_links[i-1][0] for i in range(start, end + 1)]
                        movie_links = [possible_links[i-1][1] for i in range(start, end + 1)]
                        break
                    else:
                        print(f"Invalid range. Please select numbers between 1 and {len(possible_links)}.")
                except ValueError:
                    print("Invalid input. Please enter a valid range like 1-3.")
            else:
                try:
                    indices = [int(x) for x in selection.split(',') if 0 < int(x) <= len(possible_links)]
                    if indices:
                        titles = [possible_links[i-1][0] for i in indices]
                        movie_links = [possible_links[i-1][1] for i in indices]
                        break
                    else:
                        print(f"Please enter valid numbers between 1 and {len(possible_links)}.")
                except ValueError:
                    print("Invalid input. Please enter valid numbers or ranges like 1-3 or 1,3,5.")
 
    return titles, movie_links
 
def poster_downloader(search=None, flags={}):
    while True:
        start_year, end_year = get_year_range()
        for year in range(start_year, end_year + 1):
            search = input(f"\nWrite a movie to search for in {year}: ")
            if not search:
                continue
            search = search.lower().strip().split(' ')
            search_terms = search
            logging.debug(f"Searching for {' '.join(search_terms).title()} in {year}")
            crawler = Crawler()
            possible_links = crawler.crawl(year, search_terms)
            titles, movie_links = select_link(possible_links, flags)
            if not movie_links:
                continue
 
            for title, movie_link in zip(titles, movie_links):
                logging.info(f"Found {title} at {movie_link}")
                images = crawler.get_images(year, movie_link)
                if not images:
                    logging.warning(f"No images found for {title}")
                    continue
 
                logging.debug(f"Processing {len(images)} images for {title}")
                best_images = []
                for img in images:
                    best_images.extend(crawler.get_highest_resolution(year, img, flags.get('all')))
 
                if not best_images:
                    continue
 
                logging.debug(f"Downloaded a total of {len(best_images)} images for {title}")
                files = []
                for img in best_images:
                    filename = crawler.download_img(year, img, flags.get('dry_run'))
                    if filename: 
                        files.append(filename)
 
                if files:
                    move_files(files, title.replace(':', ' '), flags.get('dry_run'))
 
        break
 
def move_files(files, movie_name, dry_run):
    dir = f"Posters/{movie_name}"
    if not dry_run:
        os.makedirs("Posters", exist_ok=True)
        logging.warning("Posters directory created")
        os.makedirs(dir, exist_ok=True)
        logging.warning(f"{dir} directory created")
        for file in files:
            try:
                shutil.move(file, dir)
                logging.warning(f"Moved {file} to {dir}")
            except Exception as e:
                logging.error(f'Error {e}')
                pass
    else:
        logging.warning("DRY RUN: Should create Posters directory")
        logging.warning(f"DRY RUN: Should create {dir} directory")
        for file in files:
            logging.warning(f"DRY RUN: Should move {file} to {dir}")
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command_line_movie', help='Movies can be called from the CLA', nargs='?', action='store', default=None)
    parser.add_argument('-f', '--file', help='Batch download from a txt file')
    parser.add_argument('-y', '--no-confirm', help='No confirmation required from you', action='append_const', const=("no_confirm", True), dest='flags')
    parser.add_argument('-a', '--all', help='Download every poster, instead of only the highest resolution available', action='append_const', const=("all", True), dest='flags')
    parser.add_argument('--dry-run', help='Only show what would be done without modifying files', action='append_const', const=("dry_run", True), dest='flags')
    parser.add_argument('-l', '--log', help='Log everything to PosterDownloader.log', action='store_true')
 
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', help='Verbose/Debug logging', action='store_const', const=logging.DEBUG, dest='loglevel')
    group.add_argument('-q', '--quiet', help='Only log file modifications', action='store_const', const=logging.WARN, dest='loglevel')
 
    args = parser.parse_args()
    flags = dict(args.flags) if args.flags else {}
    superformat = '%(levelname)s: %(message)s - %(funcName)s() at %(filename)s.%(lineno)d'
    if args.log:
        console = logging.StreamHandler()
        console.setLevel(args.loglevel or logging.INFO)
        console.setFormatter(logging.Formatter(superformat))
        logging.basicConfig(level=logging.DEBUG, format=superformat, filename='PosterDownloader.log')
        logging.getLogger('').addHandler(console)
    elif args.loglevel:
        logging.basicConfig(level=args.loglevel, format=superformat)
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
 
    if args.file:
        txt = open(args.file)
        for i, movie in enumerate(txt):
            if not movie: break
            try:
                files, movie_name = poster_downloader(movie, flags)
                if files and movie_name: move_files(files, movie_name, flags.get('dry_run'))
            except KeyboardInterrupt:
                logging.error('KeyboardInterrupt')
                continue
        txt.close()
    else:
        try:
            files, movie_name = poster_downloader(args.command_line_movie, flags)
            if files and movie_name: move_files(files, movie_name, flags.get('dry_run'))
        except KeyboardInterrupt:
            logging.error('KeyboardInterrupt')
            pass
 
main()            
