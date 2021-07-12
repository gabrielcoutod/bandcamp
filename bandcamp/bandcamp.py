import click


@click.group()
def cli():
    pass

@cli.command()
@click.argument('link')
@click.argument('album_dir')
def download(link, album_dir):
    '''
    Downloads an album and places the output in the album_dir directory.
    '''
    import bandcampdownloader
    bandcampdownloader.download(link, album_dir)

@cli.command()
@click.argument('link')
def play(link):
    '''
    PLays an album.
    '''
    import bandcampplayer
    bandcampplayer.play(link)

@cli.command()
@click.argument('search_string')
@click.option('-a', '--all_pages', is_flag=True, default=False)
def search(search_string, all_pages):
    '''
    Searches bandcamp for an album. if all_pages is set, will search all search pages
    '''
    import bandcampsearch
    bandcampsearch.search(search_string, all_pages)


if __name__ == '__main__':
    cli()