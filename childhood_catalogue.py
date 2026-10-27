"""Additional researched retro titles. External providers host all playable content.
For commercial classic games, link to a bring-your-own-ROM launcher, not copyrighted ROMs.
"""
from urllib.parse import urlparse
import re

RETRO_CLASSICS = [
 ('Contra','1988','Action','NES / Famicom'),
 ('Super Mario Bros.','1985','Platformer','NES / Famicom'),
 ('Battle City','1985','Two-player tanks','NES / Famicom'),
 ('Road Fighter','1984','Racing','Famicom / Arcade'),
 ('Circus Charlie','1984','Platformer','Famicom / Arcade'),
 ('Adventure Island','1986','Platformer','NES / Famicom'),
 ('Duck Hunt','1984','Light-gun','NES'),
 ('Excitebike','1984','Racing','NES'),
 ('Bomberman','1985','Two-player maze','NES / Famicom'),
 ('Kung-Fu Master','1984','Beat em up','Arcade / NES'),
 ('Ice Climber','1985','Platformer','NES'),
 ('Pooyan','1982','Arcade','Arcade / Famicom'),
 ('Popeye','1982','Platformer','Arcade / Famicom'),
 ('Mappy','1983','Arcade','Arcade / Famicom'),
 ('Galaga','1981','Space shooter','Arcade / NES'),
 ('Pac-Man','1980','Arcade','Arcade / NES'),
 ('Balloon Fight','1984','Arcade','NES'),
 ('Tetris (NES)','1989','Puzzle','NES'),
 ('Dr. Mario','1990','Puzzle','NES'),
 ('Double Dragon II: The Revenge','1988','Beat em up','NES'),
 ('Ninja Gaiden (NES)','1988','Action','NES'),
 ('Teenage Mutant Ninja Turtles III: The Manhattan Project','1991','Beat em up','NES'),
 ('Chip n Dale Rescue Rangers','1990','Platformer','NES'),
 ('Darkwing Duck','1992','Platformer','NES'),
 ('Tiny Toon Adventures','1991','Platformer','NES'),
 ('Snow Bros.','1990','Platformer','Arcade / NES'),
 ('Jackal','1986','Military action','Arcade / NES'),
 ('1942','1984','Flying shooter','Arcade / NES'),
 ('Gradius','1985','Space shooter','Arcade / NES'),
 ('Castlevania','1986','Action','NES'),
 ('The Legend of Zelda','1986','Adventure','NES'),
 ('Mega Man 2','1988','Platformer','NES'),
 ('Super C','1988','Action','NES'),
 ('Super Mario Bros. 3','1988','Platformer','NES'),
 ('Kirbys Adventure','1993','Platformer','NES'),
 ('Lode Runner','1983','Puzzle platformer','Famicom / PC'),
 ('Dig Dug','1982','Arcade','Arcade / Famicom'),
 ('Donkey Kong','1981','Platformer','Arcade / NES'),
 ('Elevator Action','1983','Arcade','Arcade / Famicom'),
 ('B-Wings','1984','Flying shooter','Arcade / Famicom'),
 ('Urban Champion','1984','Fighting','NES'),
 ('Clu Clu Land','1984','Puzzle','NES'),
 ('Tennis (NES)','1984','Sports','NES'),
 ('Track & Field','1983','Sports','Arcade / NES'),
 ('Super Spike VBall','1988','Sports','NES'),
 ('DuckTales','1989','Platformer','NES'),
 ('Felix the Cat','1992','Platformer','NES'),
 ('The Jungle Book (NES)','1994','Platformer','NES'),
 ('Aladdin (NES)','1995','Platformer','NES'),
 ('Dragon Warrior','1986','RPG','NES'),
]

# Direct browser destinations supplied by developers or public online platforms.
# Status intentionally conservative: manual play testing still needed.
DIRECT = [
 ('SUPERHOT Original Prototype','https://superhotgame.com/superhot-prototype/','action','Official browser prototype','SUPERHOT team'),
 ('Jedi Academy Web Demo','https://jka.virtastic.app/','action','Browser demo; full game needs assets','Virtastic'),
 ('WebWars (Hedgewars)','https://webwars.link/','multiplayer','Browser multiplayer game','WebWars'),
 ('Freeciv Web','https://play.freeciv.org/','strategy','Browser strategy game','Freeciv'),
 ('Freedoom Browser','https://pokopie.com/en/games/freedoom-online','action','Browser open-source game','Pokopie'),
 ('Filthy Kitchen NES','https://dustmop.itch.io/filthy-kitchen','arcade','Developer browser game','dustmop'),
 ('Retropia NES','https://nes.scardua.net/run/retropia','arcade','Developer browser game','Retropia'),
 ('Super Moxio Bros','https://tinybookshelf.itch.io/super-moxio-bros','arcade','Developer browser game','TinyBookshelf'),
 ('Super Tilt Bro NES','https://sgadrat.itch.io/super-tilt-bro','multiplayer','Developer browser game; check controls','sgadrat'),
 ('Famidash NES','https://kandowontu.itch.io/famidash','arcade','Developer game; check browser mode','kandowontu'),
 ('Nova the Squirrel','https://atlasignal.com/games/platform/nes','arcade','Listed on open-license browser collection','atlaSignal'),
 ('Thwaite NES','https://atlasignal.com/games/platform/nes','arcade','Listed on open-license browser collection','atlaSignal'),
]

def slugify(x): return re.sub(r'[^a-z0-9]+','-',x.lower()).strip('-')
def additional_games(existing):
    slugs={g['slug'] for g in existing}
    known={(g['title'].lower(),g['url'].rstrip('/').lower()) for g in existing}
    out=[]
    for title,year,genre,platform in RETRO_CLASSICS:
        slug='childhood-'+slugify(title)
        if slug in slugs: continue
        slugs.add(slug)
        url='https://wasmarcade.games/rom-player/'
        out.append(dict(slug=slug,title=title,cat='childhood',url=url,site='WASM Arcade (bring your own ROM)',type='Own legal game ROM required',device='Desktop & mobile, check emulator compatibility',mood='Nostalgia',time='Varies',description=f'{title} ({year}) is a classic {genre.lower()} game remembered from {platform} systems and multicart consoles. Load a legally obtained compatible game file into a browser emulator to play. NEXPLAY does not supply copyrighted ROMs.',reason=f'A nostalgic {genre.lower()} game from the classic TV-console era. Original files are not included.',controls='Keyboard / gamepad / emulator controls',tags=['Childhood Reloaded',genre,platform,'Own ROM required'],art='tetris',status='files',source='Historical game reference; launcher WASM Arcade browser ROM player',year=year,platform=platform,play_label='Load own ROM',collection='childhood'))
    for title,url,cat,mode,site in DIRECT:
        slug='retro-'+slugify(title)
        if slug in slugs or any(g['url'].rstrip('/').lower()==url.rstrip('/').lower() and g['title'].lower()==title.lower() for g in existing):continue
        slugs.add(slug)
        is_retro=('NES' in title or 'Retropia' in title or 'Moxio' in title)
        out.append(dict(slug=slug,title=title,cat='childhood' if is_retro else cat,url=url,site=site,type=mode,device='Check provider',mood='Nostalgia' if is_retro else cat.title(),time='Varies',description=f'{title} is a browser-accessible game destination. This listing links to the developer or browser service directly. Check game controls, availability and any original-file requirements at the provider.',reason='An additional unusual web-playable title found during NEXPLAY game research.',controls='Check provider',tags=['Childhood Reloaded','Browser retro','Developer game'] if is_retro else [cat.title(),'Browser game','New discovery'],art='blocks',status='demo' if 'demo' in mode.lower() else 'unverified',source='Public developer/browser destination; not manually gameplay-tested',play_label='Play now',collection='childhood' if is_retro else 'discover'))
    return out
