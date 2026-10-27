"""BitRunLog visible listing snapshot, checked 2026-10-26.
Links that were not independently opened are tagged unverified; this is a directory of outbound URLs, not hosted game files.
"""
import re
from urllib.parse import urlparse
# name | destination | category | requirements | multiplayer
ROWS='''
Quake III Arena (q3js)|https://q3js.com/|action|instant|yes
Zelda II: The Adventure of Link (z2rs)|https://z2rs.com/|arcade|files|no
Call of Duty: Black Ops Zombies|https://vel.gg/bo1z|action|unverified|no
Call of Duty: Modern Warfare 2|https://ovz-game-production.up.railway.app/|action|offline|no
Command & Conquer: Generals Zero Hour|https://generals.wasm.ltd/|strategy|files|yes
Command & Conquer: Red Alert 2|https://chronodivide.com/|strategy|unverified|yes
Counter-Strike 1.6|https://csjs.live/|action|unverified|yes
Counter-Strike: Source Bunnyhop|https://bunnyhop.lol/|action|instant|yes
Counter-Strike: Source Surf|https://surfd.net/|action|instant|yes
Crash Bash Online|https://crashbash.app/|multiplayer|instant|yes
Diablo (diablo_web)|https://johnimril.github.io/diablo_web/|action|demo|no
Doom Multiplayer (Silent Space Marine)|https://silentspacemarine.com/|action|instant|yes
Grand Theft Auto III|https://wasmarcade.com/gta3|action|unverified|no
Grand Theft Auto V|https://gta.deloskiyt.pl/|action|unverified|no
Grand Theft Auto: Vice City|https://joncodeofficial.github.io/gta-vice-city-wasm/|action|files|no
Half-Life (pixelsuft)|https://pixelsuft.github.io/|action|unverified|no
Half-Life and Counter-Strike 1.6 (WebXash)|https://x8bitrain.github.io/|action|demo|no
Halo: Combat Evolved|https://mitchellhynes.com/|action|files|yes
Halo: Combat Evolved Mobile|https://hcemobile.com/|action|files|no
LEGO Island|https://isle.pizza/|arcade|unverified|no
Minecraft 1.8.8 (EaglercraftX)|https://wasmarcade.com/minecraft|creative|instant|no
Moon (Black Ops Zombies)|https://vel.gg/|action|unverified|no
Nacht der Untoten|https://zombies.bitcoinsapi.com/|action|instant|yes
NetQuake.io|https://www.netquake.io/|action|demo|no
Pro Evolution Soccer 6|https://pes6.optijuegos.net/|arcade|unverified|yes
Quake II (q2.pieter.com)|https://q2.pieter.com/|action|unverified|yes
Quake III Arena (q3.pieter.com)|https://q3.pieter.com/|action|unverified|no
QuakeWorld (q1.pieter.com)|https://q1.pieter.com/|action|unverified|yes
Return to Castle Wolfenstein|https://rtcw.pieter.com/|action|instant|yes
RuneScape Classic|https://runescapeclassic.gold/|strategy|instant|yes
Skate 3 (fan browser game)|https://skate.aaddpp.lol/|arcade|files|no
Star Wars Jedi Knight: Jedi Academy|https://jk.q3js.com/|action|files|yes
Super Mario 64 Multiplayer|https://olivers.tools/|multiplayer|unverified|yes
Super Mario Zombies|https://smz.fun/|action|instant|no
The Simpsons: Hit & Run|https://shar-wasm.cjoseph.workers.dev/|arcade|unverified|no
Urban Terror|https://ut.pieter.com/|action|unverified|no
WadCMD (Doom in browser)|https://wadcmd.com/|action|files|no
Claude of Duty: Vibe Slops II (froydinger mirror)|https://froydinger.github.io/|action|unverified|no
Claude of Duty: Vibe Slops II (GoofyAhhBro mirror)|https://goofyahhbro69420.github.io/|action|unverified|no
Diablo (diabloweb)|https://d07riv.github.io/|action|unverified|no
Kino der Toten (GoofyAhhBro mirror)|https://goofyahhbro69420.github.io/|action|unverified|no
Kino der Toten (theeagler mirror)|https://theeagler1234-alt.github.io/|action|unverified|no
Teleoperator|https://teleoperator.mindblown.ai/|strategy|unverified|no
Roadster Rally|https://roadster.game/|arcade|unverified|no
Tekken Dark Resurrection Web Online|https://tekkendr.live/|action|unverified|no
NFS Underground 2 Online|https://nfsunderground2.site/|arcade|unverified|no
Matt Portner's Pro Skimboarder|https://wavedash.com/|arcade|unverified|no
FIFA Street 2|https://fifastreet2.fun/|arcade|unverified|no
Budokai T3|https://dragonballbt3.online/|action|unverified|no
Super Mario Kart Remake|https://burnedpopcorn.github.io/|arcade|unverified|no
Super Smash Bros in Browser|https://smash.fun/|action|unverified|no
Voxel Warfare|https://voxel-warfare.mindblown.ai/|action|unverified|no
Pixel Martin: No Filter Fighters|https://pixelgame.io/|action|unverified|no
nothalo|https://nothalo.lol/|action|unverified|no
D2 Survivors|https://d2survivors.lol/|action|unverified|no
Riposte Frontline|https://www.playriposte.com/|action|unverified|no
NBA Street V3|https://nbarecomp.xellrecomp.party/|arcade|unverified|no
Taipei GTA|https://www.taipei-rush.app/|action|unverified|no
GrandV V2|https://v2.fiveplay.lol/|action|unverified|no
ALL-22 PRO Pokémon Football|https://all22pokemon.com/|arcade|unverified|no
Link's Arena|https://linksarena.pages.dev/|action|unverified|no
GTA2 in your browser|https://m1stermo.github.io/|action|unverified|no
Friday Fighters|https://fridayfighters.com/|action|unverified|no
FIFA 10 Online|https://fifa10.website/|arcade|unverified|no
d2o|https://d2o.quest/|action|unverified|no
FighterZ Tactics|https://dragonballtft.online/|strategy|unverified|no
Need for Speed Most Wanted Web Port|https://dezm0n.itch.io/|arcade|unverified|no
PES 2011 Web Port|https://pes11.optijuegos.net/|arcade|unverified|no
Midnight Club 3 DUB Edition|https://midnighhtclub3.online/|arcade|unverified|no
FIFA 14 Online|https://fifa14.online/|arcade|unverified|no
WWE SmackDown vs Raw 2011|https://wwe2011.online/|action|unverified|no
Silent Hill Origins|https://silenthillorigins.zeliaopen.space/|action|unverified|no
Road Rash|https://roadrash.pages.dev/|arcade|unverified|no
Boondocks Brawl|https://boondocksbrawl.com/|action|unverified|no
Guitar Hero Browser Edition|https://gh3.thediaryofchris.net/|arcade|unverified|no
derby|https://genex.games/|arcade|unverified|no
Super Monkey Ball|https://monkeyball-online.pages.dev/|arcade|unverified|no
Pokemon: 3D Arena preview|https://jackijianxa.itch.io/|action|unverified|no
Dragon Ball Z Budokai 2|https://budokai2onlline.cc/|action|unverified|no
Fallout Nevada & Sonora|https://fallout-nevada.ru/|strategy|unverified|no
KAREN WARFARE|https://karenwarfare.fun/|action|unverified|no
Naruto Shippuden Ultimate Ninja Impact|https://narutoimpact.online/|action|unverified|no
Mortal Kombat: Shaolin Monks|https://mortalkombatsm.online/|action|unverified|no
SmackDown! Here Comes the Pain|https://wwepain.online/|action|unverified|no
Burnout 3|https://burnout3.online/|arcade|unverified|no
Def Jam: Fight for NY|https://def-jam.online/|action|unverified|no
FIFA 12|https://fifa12.online/|arcade|unverified|no
Gran Turismo 4|https://granturismo4.online/|arcade|unverified|no
FIFA Street|https://fifastreet.online/|arcade|unverified|no
NIL Street: NFL Street 2|https://nilstreet.playthecombine.com/|arcade|unverified|no
Marvel vs Capcom 2|https://marvelvscapcom2.online/|action|unverified|no
Street Fighter Anniversary Collection|https://streetfighteranniversary.online/|action|unverified|no
Dragon Ball Z Budokai Tenkaichi 2|https://dragonballbt2.online/|action|unverified|no
Crash Bash Online (additional listing)|https://crashbash.app/|multiplayer|unverified|yes
Battle Stadium D.O.N|https://battlestadium.online/|action|unverified|no
FIFA 11 Online|https://fifa11.online/|arcade|unverified|no
FIFA 13 Online|https://fifa13.online/|arcade|unverified|no
Dragon Ball Z Budokai 3|https://dragonballbudokai3.online/|action|unverified|no
Tony Hawk's Underground 2|https://tonyhawksunderground2.online/|arcade|unverified|no
Mortal Kombat Armageddon|https://mka.lauta.site/|action|unverified|no
GTA Vice City (rabisco mirror)|https://gta.rabisco.net/|action|unverified|no
Downhill Domination|https://downhilldomination.online/|arcade|unverified|no
Resident Evil Outbreak|https://outbreakweb.com/|action|unverified|no
Tekken 5|https://tekken5.online/|action|unverified|no
F1 06|https://f12006.online/|arcade|unverified|no
Tekken 4|https://tekken4.online/|action|unverified|no
Cyberpunk 2077 (work in progress)|https://cyberpunk2077.lol/|action|unverified|no
Street Fighter III 3rd Strike|https://streetfighter3.online/|action|unverified|no
Madden NFL 08|https://maddennfl08.online/|arcade|unverified|no
WWE SmackDown vs Raw 2010|https://wwe2010.online/|action|unverified|no
NFL Street|https://nflstreet.online/|arcade|unverified|no
SSX 3|https://ssx3.online/|arcade|unverified|no
NBA Street V3 (alternative port)|https://nbastreet3.online/|arcade|unverified|no
WWE SmackDown vs Raw 2011 (alternative listing)|https://wwe2011.online/|action|unverified|no
ALL-22 SLUGGER Pokémon Baseball|https://all22pokemon.com/|arcade|unverified|no
The Warriors|https://thewarriors.online/|action|unverified|no
NBA 2K12|https://nba2k12.online/|arcade|unverified|no
Naruto Shippuden Ultimate Ninja 5|https://narutoshippuden5.online/|action|unverified|no
UFC Throwdown|https://ufc2.online/|action|unverified|no
PES 2012|https://pes12.online/|arcade|unverified|no
Resident Evil 4|https://residentevil4.online/|action|unverified|no
Rugby 08|https://mitchivin.github.io/|arcade|unverified|no
Tony Hawk's Pro Skater 3|https://tonyhawkpro3.online/|arcade|unverified|no
Spider-Man 2|https://spiderman2.online/|action|unverified|no
PES 2014|https://pes14.online/|arcade|unverified|no
Monster Hunter Freedom Unite|https://mhfu.online/|action|unverified|no
God of War Chains of Olympus|https://godofwarchains.online/|action|unverified|no
Ratchet & Clank Size Matters|https://ratchetclanksizematters.online/|action|unverified|no
Jak and Daxter The Lost Frontier|https://jakdaxterlostfrontier.online/|action|unverified|no
Crisis Core Final Fantasy VII|https://crisiscorefinalfantasy7.online/|action|unverified|no
Virtua Tennis 2|https://virtuatennis2.online/|arcade|unverified|no
God of War Ghost of Sparta|https://godofwarsparta.online/|action|unverified|no
Cricket 07 (Browser Edition)|https://cricket07.dhaiwat.com/|arcade|instant|yes
Need for Speed Underground 2 Revived|https://nfsu2.xyz/|arcade|instant|yes
OpenLara (Tomb Raider 1996)|https://xproger.info/projects/OpenLara/|action|demo|no
OpenTTD Online (Browser Edition)|https://openttdonline.com/|strategy|instant|no
Resident Evil Outbreak Web|https://outbreakweb.com/|action|instant|yes
WipEout Browser Rewrite|https://phoboslab.org/wipegame/|arcade|instant|no
Alley Cat Recompiled|https://petarov.github.io/alleycat.exe/|arcade|instant|no
Lugaru Web|https://loganwalkerdev.github.io/lugaru-web/|action|instant|no
Prince of Persia (PrinceJS)|https://princejs.com/|arcade|instant|no
SimCity Classic (micropolisJS)|https://www.graememcc.co.uk/micropolisJS/|strategy|instant|no
'''.strip().splitlines()

ARTS=['tank','orbit','tetris','cells','snake','blocks','train','alchemy','chess','hex']
def make_games():
    games=[];slugs=set()
    for i, row in enumerate(ROWS):
        title,url,cat,need,multi=row.split('|')
        slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')
        if slug in slugs:slug+='-'+str(i)
        slugs.add(slug)
        domain=urlparse(url).hostname or url
        mode={'instant':'Instant play (source label)','files':'Requires your own game files','demo':'Browser demo','offline':'Currently offline','unverified':'Browser link (not independently verified)'}[need]
        if multi=='yes':mode+=' · multiplayer'
        tags=[cat.title()]+(['Multiplayer'] if multi=='yes' else [])+(['Own game files needed'] if need=='files' else [])+(['Link unverified'] if need=='unverified' else [])
        description=(f'{title} is listed as a browser gaming destination on BitRunLog. '
                     +('The provider requires game files from a copy you own. ' if need=='files' else 'Its availability and requirements should be confirmed on the original site. ')
                     +'NEXPLAY links to the third-party destination and does not host its game files.')
        games.append(dict(slug=slug,title=title,cat=cat,url=url,site=domain,type=mode,device='Check provider',mood=cat.title(),time='Varies',description=description,reason='Included in the BitRunLog catalogue snapshot. Availability and rights are not guaranteed.',controls='See provider',tags=tags,art=ARTS[i%len(ARTS)],status=need,source='BitRunLog visible catalogue 2026-10-26'))
    games.sort(key=lambda g: (0 if g["slug"]=="cricket-07-browser-edition" else 1))
    return games
